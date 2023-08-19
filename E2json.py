import pandas as pd
import json
import warnings

# 경고 메시지 무시 설정
warnings.simplefilter(action='ignore', category=UserWarning)

# 파일 경로 설정
excel = r'C:\Users\kmg00\Desktop\생활쓰레기종합배출정보.xlsx'
json_f = r'C:\Users\kmg00\Desktop\Rdata\생활쓰레기종합배출정보.json'

# 액셀 파일을 pandas DataFrame으로 읽기
df = pd.read_excel(excel)

# DataFrame을 JSON 형태로 변환
data = df.to_dict(orient='records')

# 데이터를 JSON 파일로 저장
try:
    with open(json_f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error while saving to {json_f}: {e}")

print('성공')
