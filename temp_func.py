
>     def search_weather(city_query: str) -> str:
          """根据地点/城市名称查询最新的真实气象和天气状况。如果查询国内城市，请直接传入中文（如：北京）；如果是国外城市，请传入英文拼写。"""
          import re
          has_chinese = bool(re.search(r'[\u4e00-\u9fa5]', city_query))
          
          try:
              # ==========================================
              # 【通道 A：中国腾讯天气通道】
              # ==========================================
              if has_chinese:
                  print(f"\n  [Tools] 🧭 检测到中文【{city_query}】，优先走【腾讯天气大通道】...")
                  tencent_key = "TJFBZ-N2WKT-O6TXV-LVJSA-2ZFFV-6CFB5"
                  
                  # 第一步：腾讯地图地理编码，获取精确经纬度
                  geo_url = f"https://apis.map.qq.com/ws/geocoder/v1/?address={city_query}&key={tencent_key}"
                  geo_res = requests.get(geo_url, timeout=5).json()
                  
                  if geo_res.get("status") == 0:
                      loc = geo_res["result"]["location"]
                      lat, lng = loc["lat"], loc["lng"]
                      city_disp = geo_res["result"]["title"]
                      
                      # 第二步：腾讯位置服务 - 智能气象 API
                      weather_url = f"https://apis.map.qq.com/ws/weather/v1/?location={lat},{lng}&key={tencent_key}"
                      w_res = requests.get(weather_url, timeout=5).json()
                      
                      if w_res.get("status") == 0:
                          realtime = w_res["result"]["realtime"][0]
                          info = realtime.get("infos", {})
                          return (
                              f"【通道 A：腾讯智能气象】\n"
                              f"请求位置：{city_disp}\n"
                              f"天气：{info.get('weather')}\n"
                              f"温度：{info.get('temperature')}°C\n"
                              f"湿度：{info.get('humidity')}%\n"
                              f"风况：{info.get('wind_direction')} {info.get('wind_power')}"
                          )
                      else:
                          print(f"  [Router] ⚠️ 腾讯天气获取失败，转向国际兜底通道 (Fallback)...")
                  else:
                      print(f"  [Router] ⚠️ 腾讯地理位置解析无结果，转向国际兜底通道 (Fallback)...")
  
              # ==========================================
              # 【通道 B：国际通用通道 (OpenWeatherMap) 】
              # ==========================================
              print(f"\n  [Tools] 🌐 切换至【OpenWeatherMap 全球通用通道】...")
              # 修正了你提供的可用 Key
              openweathermap_key = "39bcae3d76102e09964fba4e4981bcd0"
              weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={openweathermap_key}&units=metric&lang=zh_cn"
              
              weather_resp = requests.get(weather_url, timeout=5)
              
              if weather_resp.status_code == 200:
                  data = weather_resp.json()
                  city_name = data.get("name")
                  temp = data["main"]["temp"]
                  feels_like = data["main"]["feels_like"]
                  desc = data["weather"][0]["description"]
                  wind = data["wind"]["speed"]
                  
                  return (
                      f"【通道 B：OpenWeatherMap 天气数据】\n"
                      f"城市：{city_name}\n"
                      f"天气：{desc}\n"
                      f"温度：{temp}°C (体感: {feels_like}°C)\n"
                      f"风速：{wind} m/s"
                  )
              else:
                  error_msg = weather_resp.text
                  print(f"  [Error] ❌ OpenWeatherMap API 请求失败: {error_msg}")
                  return f"系统提示：获取 {city_query} 天气时发生错误，返回信息：{error_msg}。"

