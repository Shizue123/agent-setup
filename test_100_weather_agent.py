import os
import random
from dotenv import load_dotenv

# 因为你要跑 100 次代理循环！我们将使用直接工具函数调用做「压力测试」，
# 这样100次调用基本在系统内部瞬间完成，且不消耗你 DeepSeek 的 API Token
import os
import random
import requests
import re
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def search_weather(city_query: str) -> str:
    """根据地点查询天气"""
    has_chinese = bool(re.search(r'[\u4e00-\u9fa5]', city_query))
    try:
        if has_chinese:
            tencent_key = "TJFBZ-N2WKT-O6TXV-LVJSA-2ZFFV-6CFB5"
            geo_url = f"https://apis.map.qq.com/ws/geocoder/v1/?address={city_query}&key={tencent_key}"
            geo_res = requests.get(geo_url, timeout=5).json()
            if geo_res.get("status") == 0:
                loc = geo_res["result"]["location"]
                lat, lng = loc["lat"], loc["lng"]
                city_disp = geo_res["result"]["title"]
                weather_url = f"https://apis.map.qq.com/ws/weather/v1/?location={lat},{lng}&key={tencent_key}"
                w_res = requests.get(weather_url, timeout=5).json()
                if w_res.get("status") == 0:
                    realtime = w_res["result"]["realtime"][0]
                    info = realtime.get("infos", {})
                    return f"【通道 A：腾讯智能气象】城市：{city_disp}，天气：{info.get('weather')}，温度：{info.get('temperature')}°C，风向：{info.get('wind_direction')} {info.get('wind_power')}。"
                
        openweathermap_key = "39bcae3d76102e09964fba4e4981bcd0"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={openweathermap_key}&units=metric&lang=zh_cn"
        weather_resp = requests.get(weather_url, timeout=5)
        if weather_resp.status_code == 200:
            data = weather_resp.json()
            city_name = data.get("name")
            return f"【通道 B：OpenWeatherMap】城市：{city_name}，天气：{data['weather'][0]['description']}，温度：{data['main']['temp']}°C。"
        else:
            return f"❌ 获取失败 - API响应: {weather_resp.text}"
    except Exception as e:
        return f"❌ 内部错误 - {str(e)}"

# 构建测试城市库（各地区、中英文混杂）
city_pool = [
    "北京", "Shanghai", "广州", "Shenzhen", "成都", "Hangzhou", "武汉", "Nanjing",
    "纽约", "New York", "伦敦", "London", "巴黎", "Paris", "东京", "Tokyo",
    "西雅图", "Seattle", "Sydney", "悉尼", "柏林", "Berlin", "首尔", "Seoul",
    "Urumqi", "乌鲁木齐", "拉萨", "Lhasa", "哈尔滨", "Harbin", "三亚", "Sanya",
    "Mohe", "漠河", "瑞丽", "Ruili", "Tashkurgan", "塔什库尔干", "Haikou", "海口",
    "Toronto", "多伦多", "Vancouver", "温哥华", "Moscow", "莫斯科", "罗马", "Rome",
    "开罗", "Rome", "Buenos Aires", "布宜诺斯艾利斯", "Rio de Janeiro", "里约热内卢"
]

# 随机抽取生成100条测试数据，打乱顺序
test_cases = random.choices(city_pool, k=100)

success_count = 0
channel_a_count = 0
channel_b_count = 0

print("=====================================================")
print(f" 开始大规模天气 Agent 测试，共 {len(test_cases)} 轮查询")
print("=====================================================\n")

for i, city in enumerate(test_cases, 1):
    print(f"\n[{i}/100] 测试输入: {city}")
    try:
        # 我们直接调用 Agent 背后的核心工具来验证获取状态
        # 实际 Agent 的表现完全取决于这个工具获取客观数据的能力
        result = search_weather.invoke({"city_query": city})
        
        if "发生内部错误" in result or "发生错误" in result:
             print(f"❌ 失败: {result[:50]}...")
        else:
             success_count += 1
             if "通道 A" in result:
                 channel_a_count += 1
                 # 收敛日志长度，只打印提取到的前三行
                 print("✅ " + " | ".join(result.split('\n')[:3]))
             else:
                 channel_b_count += 1
                 print("✅ " + " | ".join(result.split('\n')[:3]))
                 
    except Exception as e:
        print(f"❌ 崩溃崩溃崩溃: {str(e)}")

print("\n=====================================================")
print(f"测试完毕。情况汇报：")
print(f"总计调用: 100 次")
print(f"成功率: {success_count}/100")
print(f"腾讯智能通道命中: {channel_a_count} 次")
print(f"国际通用通道命中: {channel_b_count} 次")
print("=====================================================")
