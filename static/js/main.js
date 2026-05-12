// 1. 提示弹窗函数
function showToast(msg, isError = false) {
    const toast = document.getElementById("toast");
    toast.innerText = msg;
    toast.style.backgroundColor = isError ? "#EF4444" : "#333";
    toast.className = "show";
    setTimeout(() => { toast.className = toast.className.replace("show", ""); }, 3000);
}

// 2. 显示查询结果函数
function showResult(html) {
    const resArea = document.getElementById('resultArea');
    resArea.style.display = 'block';
    resArea.innerHTML = html;
}

// 3. 页面加载完毕后，自动读取缓存并查询
document.addEventListener('DOMContentLoaded', () => {
    const savedName = localStorage.getItem('ql_varName');
    const savedRemarks = localStorage.getItem('ql_remarks');
    const savedValue = localStorage.getItem('ql_value'); // 自动读取 Token 记忆

    if (savedName) document.getElementById('varName').value = savedName;
    if (savedRemarks) {
        document.getElementById('remarks').value = savedRemarks;
        // 如果有记住的备注，进页面自动触发一次查询展示状态
        queryEnv();
    }
    if (savedValue) document.getElementById('value').value = savedValue; // 自动填入 Token
});

// 4. 提交变量主函数
async function submitEnv() {
    const name = document.getElementById('varName').value.trim();
    const remarks = document.getElementById('remarks').value.trim();
    const value = document.getElementById('value').value.trim();

    // 判空拦截
    if (!name || !remarks || !value) {
        return showToast('请将表单填写完整', true);
    }

    // 专属备注的【邮箱格式】严格正则校验
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(remarks)) {
        return showToast('备注必须是正确的邮箱格式！', true);
    }

    try {
        const res = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, remarks, value })
        });
        const data = await res.json();

        if(data.code === 200) {
            showToast('🎉 ' + data.msg);

            // 提交成功后，把 名称、备注、Token 全部存入本地浏览器
            localStorage.setItem('ql_varName', name);
            localStorage.setItem('ql_remarks', remarks);
            localStorage.setItem('ql_value', value);

            // 这里不再清空 value 输入框，因为你要保留 Token
            // document.getElementById('value').value = '';

            // 提交完自动刷新一下查询结果
            queryEnv();
        } else {
            showToast(data.msg, true);
        }
    } catch (e) {
        showToast('网络请求失败', true);
    }
}

// 5. 查询变量状态函数
async function queryEnv() {
    const remarks = document.getElementById('remarks').value.trim();

    if (!remarks) return showToast('请输入备注后再进行查询', true);

    // 查询前也必须是邮箱格式
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(remarks)) {
        return showToast('请输入正确的邮箱格式进行查询', true);
    }

    try {
        const res = await fetch(`/api/query?remarks=${remarks}`);
        const data = await res.json();

        if (data.code === 200) {
            if (data.data.length === 0) {
                showResult('未找到该邮箱的变量记录。');
            } else {
                let html = '<div style="margin-bottom:10px;font-weight:bold;">您的变量状态：</div>';
                data.data.forEach(item => {
                    html += `
                    <div class="env-card">
                        <div><span>变量名:</span> ${item.name}</div>
                        <div><span>状态:</span> ${item.status}</div>
                        <div><span>值:</span> ${item.value}</div>
                    </div>`;
                });
                showResult(html);
            }
        } else {
            showToast(`查询失败: ${data.msg}`, true);
        }
    } catch (e) {
        showToast('网络请求失败', true);
    }
}