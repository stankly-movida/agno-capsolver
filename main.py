import requests
import time
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool

# 请替换为您真实的 CapSolver API Key
CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

@tool
def solve_recaptcha_v2(website_url: str, website_key: str) -> str:
    """
    使用 CapSolver 解决 reCAPTCHA v2 验证码。

    参数:
        website_url: 带有验证码的网站 URL
        website_key: 验证码的 site key (data-sitekey 属性)

    返回:
        g-recaptcha-response 令牌
    """
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }

    response = requests.post("https://api.capsolver.com/createTask", json=payload)
    result = response.json()

    if result.get("errorId") != 0:
        return f"错误: {result.get('errorDescription')}"

    task_id = result.get("taskId")

    # 轮询结果
    for attempt in range(60):
        time.sleep(2)
        result = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id}
        ).json()

        if result.get("status") == "ready":
            return result["solution"]["gRecaptchaResponse"]
        if result.get("status") == "failed":
            return f"失败: {result.get('errorDescription')}"

    return "等待解决方案超时"

@tool
def solve_turnstile(website_url: str, website_key: str) -> str:
    """
    解决 Cloudflare Turnstile 验证。

    参数:
        website_url: 带有 Turnstile 的网站 URL
        website_key: Turnstile 组件的 site key

    返回:
        Turnstile 令牌
    """
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "AntiTurnstileTaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }

    response = requests.post("https://api.capsolver.com/createTask", json=payload)
    result = response.json()

    if result.get("errorId") != 0:
        return f"错误: {result.get('errorDescription')}"

    task_id = result.get("taskId")

    for _ in range(60):
        time.sleep(2)
        result = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id}
        ).json()

        if result.get("status") == "ready":
            return result["solution"]["token"]
        if result.get("status") == "failed":
            return f"失败: {result.get('errorDescription')}"

    return "超时"

@tool
def check_capsolver_balance() -> str:
    """
    检查当前 CapSolver 账户余额。

    返回:
        当前余额信息
    """
    response = requests.post(
        "https://api.capsolver.com/getBalance",
        json={"clientKey": CAPSOLVER_API_KEY}
    )
    result = response.json()

    if result.get("errorId") != 0:
        return f"错误: {result.get('errorDescription')}"

    return f"余额: ${result.get('balance', 0):.4f}"

# 创建网页爬虫智能体
web_scraper_agent = Agent(
    name="网页爬虫专家",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_recaptcha_v2, solve_turnstile, check_capsolver_balance],
    description="能够自动处理验证码挑战的专家级网页爬虫",
    instructions=[
        "你是一名具备验证码解决能力的网页抓取专家。",
        "遇到验证码时，识别其类型并使用相应的解决工具。",
        "对于 reCAPTCHA v2，使用 solve_recaptcha_v2 并提供 URL 和 site key。",
        "对于 Turnstile，使用 solve_turnstile 并提供 URL 和 site key。",
        "在开始大规模抓取任务前，务必先检查余额。"
    ],
    markdown=True
)

def main():
    print("=" * 60)
    print("Agno + CapSolver 集成演示")
    print("=" * 60)

    # 任务：解决一个 reCAPTCHA 挑战
    task = """
    我需要你解决一个 reCAPTCHA v2 挑战。

    网站 URL: https://www.google.com/recaptcha/api2/demo
    Site Key: 6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-

    请解决此验证码并报告令牌的前 50 个字符。
    在开始之前，请先检查我的 CapSolver 余额。
    """

    response = web_scraper_agent.run(task)
    print("\n智能体响应:")
    print(response.content)

if __name__ == "__main__":
    main()
