import os
import requests
import re
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 环境变量配置
QL_URL = os.environ.get('QL_URL', 'http://127.0.0.1:5700')
CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')

def get_token():
    url = f"{QL_URL}/open/auth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get('code') == 200:
            return res['data']['token']
    except Exception as e:
        print(f"获取Token失败: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')      # 新增：动态获取变量名称
    value = data.get('value')
    remarks = data.get('remarks')

    if not name or not value or not remarks:
        return jsonify({"code": 400, "msg": "变量名、变量值和备注均不能为空"})

    token = get_token()
    if not token:
        return jsonify({"code": 500, "msg": "无法连接青龙面板，请检查配置"})

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 查询是否已存在同名且同备注的变量，若有则更新，无则新增
    # === 将原本的 search_res 判断部分替换为以下内容 ===
    search_res = requests.get(f"{QL_URL}/open/envs?searchValue={remarks}", headers=headers).json()
    existing_id = None

    if search_res.get('code') == 200:
        for env in search_res['data']:
            if env.get('name') == name and env.get('remarks') == remarks:

                # 1. 针对京东 Cookie，智能提取 pt_pin 进行对比
                if 'pt_pin=' in value:
                    new_pin_match = re.search(r'pt_pin=([^;]+)', value)
                    old_pin_match = re.search(r'pt_pin=([^;]+)', env.get('value', ''))

                    if new_pin_match and old_pin_match:
                        # 如果 pt_pin 一样，说明是同一个号过期了，执行【覆盖更新】
                        if new_pin_match.group(1) == old_pin_match.group(1):
                            existing_id = env.get('id')
                            break
                        else:
                            # 不同的京东账号，跳过，去执行【新增】
                            continue

                # 2. 针对其他变量（比如快手、饿了么等不带 pt_pin 的）
                else:
                    # 如果提交的值一模一样，防重复提交
                    if env.get('value') == value:
                        existing_id = env.get('id')
                        break
                    # 如果值不一样，跳过，去执行【新增】，不顶掉旧的

    if existing_id:
        # 更新
        payload = {"value": value, "name": name, "remarks": remarks, "id": existing_id}
        res = requests.put(f"{QL_URL}/open/envs", json=payload, headers=headers).json()
        action_msg = "已更新旧账号！"
    else:
        # 新增
        payload = [{"value": value, "name": name, "remarks": remarks}]
        res = requests.post(f"{QL_URL}/open/envs", json=payload, headers=headers).json()
        action_msg = "已新增一个账号！"

    if res.get('code') == 200:
        return jsonify({"code": 200, "msg": action_msg})
    else:
        return jsonify({"code": 500, "msg": res.get('message', '提交失败')})
@app.route('/api/query', methods=['GET'])
def query():
    remarks = request.args.get('remarks')
    if not remarks:
        return jsonify({"code": 400, "msg": "请输入备注进行查询"})

    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{QL_URL}/open/envs?searchValue={remarks}", headers=headers).json()

    if res.get('code') == 200:
        result = []
        for env in res['data']:
            if env.get('remarks') == remarks:
                # 隐藏敏感值部分内容
                val = env.get('value')
                masked_val = val[:10] + '***' + val[-10:] if len(val) > 20 else '***'
                status_text = "🟢 正常" if env.get('status') == 0 else "🔴 禁用"
                result.append({
                    "name": env.get('name'),
                    "value": val,
                    "remarks": env.get('remarks'),
                    "status": status_text
                })
        return jsonify({"code": 200, "data": result})
    return jsonify({"code": 500, "msg": "查询失败"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)