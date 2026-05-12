# 青龙面板变量自助提交与管理系统

这是一个基于 **Flask** 开发的轻量级 Web 助手。它为用户提供了一个直观的图形化界面，用于自助提交环境变量、查询实时运行状态以及管理历史账号，极大地减轻了面板管理员的人工维护压力。

## ✨ 核心特性

- **📧 邮箱备注体系**：强制要求用户使用邮箱作为唯一标识（备注），方便用户记忆并实现名下所有账号的一键反查。
- **🔄 智能覆盖更新**：
  - 系统内置正则匹配逻辑，可自动识别京东等脚本中的 `pt_pin`。
  - 同账号过期时执行 **PUT (更新)**，新账号则执行 **POST (新增)**，彻底解决重复提交导致的变量覆盖问题。
- **🔍 状态实时反查**：用户通过邮箱即可反查青龙面板中对应的所有变量，并直观展示运行状态（✅ 正常运行 / ❌ 已禁用）。
- **🗑️ 自助删除功能**：支持用户在网页端安全地移除自己名下的无效变量。
- **💾 浏览器本地记忆**：利用 `localStorage` 技术，自动填充用户上次提交的变量名、备注和 Token，提升二次操作效率。
- **🚀 国内部署加速**：Dockerfile 已针对国内网络优化，预设清华大学 PyPI 镜像源，确保 10 秒内完成容器构建。

## 🛠️ 技术架构

- **后端**: [Python 3.9](https://www.python.org/) + [Flask 3.0](https://flask.palletsprojects.com/)
- **前端**: 原生 HTML5 + CSS3 + JavaScript (ES6)
- **部署**: [Docker](https://www.docker.com/) + Docker Compose

## 🚀 快速部署

### 1. 克隆仓库

```bash
git clone https://github.com/2468309202/ql-panel.git
cd ql-panel
```
---

### 2. 配置环境变量

在项目根目录新建 `.env` 文件，填入你的青龙面板信息：
```env
# 青龙面板后端地址（若在同一台服务器，建议填写内网 IP）
QL_URL=http://127.0.0.1:5700

# 青龙面板 -> 系统设置 -> 应用设置 -> 新建应用
# （必须勾选：环境变量权限）
CLIENT_ID=你的应用ID
CLIENT_SECRET=你的应用密钥
```
### 3. Docker-compose部署 一键启动
```bash
#复制docker-compose.yml文件 
docker-compose up -d
```
## 🚀 快速开始

```bash
docker run -d \
-p 8080:8080 \
-e QL_URL=http://127.0.0.1:5700 \
-e CLIENT_ID=你的ID \
-e CLIENT_SECRET=你的SECRET \
manyue667/ql-panel:v1.0
```

```text
📂 目录结构
├── app.py              # Flask 后端核心逻辑（包含 API 转发与智能判断）
├── Dockerfile          # 镜像构建脚本（已集成国内换源）
├── docker-compose.yml  # 容器编排配置
├── requirements.txt    # 项目依赖库清单
├── .env                # 敏感配置文件（需自行创建）
├── static/
│   ├── style.css       # 响应式 UI 布局
│   └── js/
│       └── main.js     # 前端交互逻辑、格式校验与本地存储
└── templates/
    └── index.html      # Jinja2 网页模板
```
⚠️ 注意事项
端口放行：请确保服务器安全组已开放 8080 端口。若端口冲突，请修改 docker-compose.yml 中的映射端口。

格式校验：为了数据规范，系统默认开启了严格的邮箱格式检查，提交时备注栏必须填写正确格式的邮箱。

数据隐私：本系统仅作为青龙官方 API 的中转代理，不提供任何持久化数据库存储，所有数据均即时同步至你的青龙面板。

🤝 贡献与反馈
如果您在使用中遇到任何问题或有改进建议，欢迎提交 Issues 或 Pull Request
