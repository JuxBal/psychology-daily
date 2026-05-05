import os
import json
import requests
from datetime import datetime, timezone

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def generate_daily_news():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # 精心设计的提示词：要求最新、权威、杜绝营销号
    system_prompt = """
你是一个专业的心理学新闻编辑，每天从权威渠道收集当日或近两日的重要心理学新闻。
要求：
1. 只使用以下权威来源：国际顶刊官网（如Nature, Science, JAMA Psychiatry, Lancet Psychiatry, PNAS, Psychological Science等）、知名大学/研究机构新闻稿、APA美国心理学会官网、中国心理学会官网、国家卫健委等官方机构公告。
2. 绝对禁止使用知乎、微信公众号、个人博客、营销号、自媒体等非权威来源。
3. 每条新闻用中文撰写，包含：标题（简洁准确）、一句话摘要（不超过60字）、原文链接（必须是直接可访问的URL）、来源机构名称。
4. 分成“中国”和“世界”两部分，中国部分聚焦国内政策、本土研究；世界部分聚焦国际研究、行业动态。
5. 输出一个JSON对象，格式如下：
{
  "news": [
    {
      "region": "china",
      "title": "...",
      "summary": "...",
      "source": "来源机构",
      "link": "https://...",
      "important": false
    }
  ]
}
注意：如果某条新闻特别重要（如重大政策、重要讣告），将important设为true。
请确保所有链接真实有效。
"""
    
    user_prompt = f"请收集并生成今日（{today}）的心理学日报，至少包含3条中国新闻和3条世界新闻。"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,   # 低温度保证准确性
        "stream": False
    }
    
    # 如果API支持联网搜索，启用对应参数（以官方文档为准）
    # payload["search"] = True  # 请查阅DeepSeek最新文档
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 解析JSON（DeepSeek可能返回带格式的json code block）
        # 提取第一个{...}对象
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end > start:
            json_str = content[start:end]
            news_data = json.loads(json_str)
        else:
            raise ValueError("无法解析JSON")
        
        # 添加更新日期
        news_data["updateDate"] = today
        
        # 写入news.json
        with open("news.json", "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功生成 {len(news_data.get('news', []))} 条新闻")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        # 失败时保留旧的news.json不变
        exit(1)

if __name__ == "__main__":
    generate_daily_news()
