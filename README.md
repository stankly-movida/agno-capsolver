# Agno + CapSolver: 自主多智能体验证码自动化解决方案 🚀

[![GitHub stars](https://img.shields.io/github/stars/capsolver/agno-capsolver-integration?style=social)](https://github.com/capsolver/agno-capsolver-integration)
[![License: MIT](https://img.shields.io/badge/许可证-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno](https://img.shields.io/badge/框架-Agno-orange)](https://github.com/agno-agi/agno)

将 **CapSolver** 与 **Agno** 集成，构建高性能、隐私优先的自主智能体，轻松绕过各种验证码挑战。

---

## 🌟 项目概述

随着 AI 驱动的自动化在实际工作流中变得越来越实用，**Agno** 已成为构建自主多智能体系统的首选框架，其速度快且隐私优先。然而，在进行网页抓取或数据采集时，验证码（CAPTCHA）往往会阻碍这些智能体的运行。

**CapSolver** 通过让 Agno 智能体能够可靠地处理受验证码保护的页面，解决了这一难题，确保自动化流程不中断。两者结合，为真实世界的网站提供了可扩展、无需人工干预的自动化能力。

### 核心优势
- **无中断工作流**：智能体自主解决挑战，无需人工干预。
- **隐私优先**：利用 Agno 的自托管特性，完全掌控您的数据。
- **高性能**：Agno 的运行速度比传统智能体框架快高达 529 倍。
- **多类型支持**：支持 reCAPTCHA (v2/v3)、Cloudflare Turnstile、AWS WAF 等。

---

## 🛠️ 安装指南

```bash
pip install agno requests selenium aiohttp
```

---

## 🚀 快速上手

### 1. 定义验证码解决工具

为您的 Agno 智能体创建一个自定义工具来调用 CapSolver：

```python
import requests
from agno.tools import tool

CAPSOLVER_API_KEY = "您的_CAPSOLVER_API_KEY"

@tool
def solve_recaptcha_v2(website_url: str, website_key: str) -> str:
    """使用 CapSolver 解决 reCAPTCHA v2 挑战。"""
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }
    # ... (完整实现请参考 main.py)
```

### 2. 创建自主智能体

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    name="网页爬虫",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_recaptcha_v2],
    instructions=["遇到验证码时，请使用 solve_recaptcha_v2 工具。"],
    markdown=True
)

agent.run("解决 https://example.com/demo 上的验证码")
```

---

## 📂 项目结构

```text
agno-capsolver-zh/
├── examples/
│   ├── multi_agent_team.py    # 专门的智能体团队示例
│   └── token_submission.py    # Selenium/Requests 令牌注入示例
├── main.py                    # 核心实现与演示
├── requirements.txt           # 依赖项
└── README.md                  # 项目文档
```

---

## 💡 最佳实践

1. **错误处理**：在轮询结果时实现指数退避算法。
2. **余额管理**：使用 `check_capsolver_balance` 工具监控您的额度。
3. **异步支持**：在高并发环境下，使用 `aiohttp` 进行非阻塞的验证码解决。

---

## 🔗 相关链接

- [CapSolver 控制台](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=agno_zh)
- [Agno 官方文档](https://github.com/agno-agi/agno)
- [CapSolver API 文档](https://docs.capsolver.com/)

---

## 🎁 特别优惠

准备好开始了吗？[立即注册 CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=agno_zh) 并使用优惠码 **AGNO**，首充可获得额外 **6% 赠送**！

---

## 📄 开源协议

本项目采用 MIT 许可证。详情请参阅 `LICENSE` 文件。

---

<p align="center">
  由 CapSolver 社区倾情打造 ❤️
</p>
