from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools import tool
import requests
import time

CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

@tool
def solve_any_captcha(
    website_url: str,
    website_key: str,
    captcha_type: str = "ReCaptchaV2TaskProxyLess"
) -> str:
    """支持多种类型的通用验证码解决工具。"""
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": captcha_type,
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
            solution = result.get("solution", {})
            return solution.get("gRecaptchaResponse") or solution.get("token")
        if result.get("status") == "failed":
            return f"失败: {result.get('errorDescription')}"

    return "超时"

# 验证码专家智能体
captcha_agent = Agent(
    name="验证码专家",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_any_captcha],
    description="擅长识别和解决各种验证码类型",
    instructions=[
        "通过页面分析识别验证码类型",
        "使用正确的参数调用相应的解决工具",
        "清晰地报告成功或失败结果"
    ]
)

# 数据提取智能体
data_agent = Agent(
    name="数据提取专家",
    model=OpenAIChat(id="gpt-4o"),
    description="从网页中提取并处理数据",
    instructions=[
        "从 HTML 内容中提取结构化数据",
        "在需要时请求验证码解决服务",
        "验证并清洗提取的数据"
    ]
)

# 创建团队
scraping_team = Team(
    name="网页抓取团队",
    agents=[captcha_agent, data_agent],
    description="专门从事带验证码处理的网页抓取团队"
)

if __name__ == "__main__":
    # 示例用法
    print("多智能体团队已初始化，准备处理复杂的抓取任务。")
