import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# API 요청을 위한 기본 정보 설정
base_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
API_KEY = os.getenv('API_KEY')  # 발급받은 서비스키
nx = '60'  # 서울의 X 좌표값
ny = '127'  # 서울의 Y 좌표값

# 현재 시각을 기준으로 발표일자와 발표시각 설정
now = datetime.now()
base_date = now.strftime('%Y%m%d')  # 발표일자 (YYYYMMDD)
base_time = now.strftime('%H%M')  # 발표시각 (HHMM)

# 요청 파라미터 설정
params = {
    'serviceKey': API_KEY,
    'dataType': 'JSON',  # 응답 형식 (XML 또는 JSON)
    'base_date': base_date,
    'base_time': base_time,
    'nx': nx,
    'ny': ny
}

try:
    # API 요청 보내기
    response = requests.get(base_url, params=params)
    data = response.json()

    # 원하는 데이터 추출 및 출력
    items = data['response']['body']['items']['item']
    weather_info = {}
    for item in items:
        category = item['category']  # 자료구분코드
        obs_value = item['obsrValue']  # 실황 값
        weather_info[category] = obs_value
    
    # 원하는 정보 출력
    print(f'서울의 날씨 정보 ({base_date} {base_time})')
    print('-' * 30)
    print(f"강수확률: {weather_info.get('RN1', '정보 없음')}%")
    print(f"습도: {weather_info.get('REH', '정보 없음')}%")
    print(f"하늘상태: {weather_info.get('SKY', '정보 없음')}")
    print(f"최저기온: {weather_info.get('T1H', '정보 없음')}°C")
    print(f"최고기온: {weather_info.get('RN1', '정보 없음')}°C")
    print(f"풍향: {weather_info.get('VEC', '정보 없음')}°")
    print(f"풍속: {weather_info.get('WSD', '정보 없음')} m/s")

except Exception as e:
    print(f'Error occurred: {e}')