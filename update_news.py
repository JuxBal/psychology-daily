import json
from datetime import datetime

# 这里只生成模拟数据，真实情况下你可以调用新闻API或RSS
today = datetime.now().strftime("%Y-%m-%d")
data = {
    "updateDate": today,
    "news": [
        {
            "region": "china",
            "title": "全国心理援助热线新增110个县",
            "summary": "2026年国家卫健委将新增110个县开设心理门诊，填补基层空白。",
            "source": "国家卫生健康委",
            "image": "",
            "important": True
        },
        {
            "region": "world",
            "title": "幸福感能预测半年后自控力",
            "summary": "《Social Psychological and Personality Science》研究发现积极情绪有利于自我控制。",
            "source": "SPSP",
            "image": "",
            "important": False
        }
    ]
}

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("news.json updated.")
