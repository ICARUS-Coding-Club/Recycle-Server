import pandas as pd
import os
import glob

# 폴더 내의 모든 CSV 파일 가져오기
folder_path = 'C:\\Users\\kmg00\\Desktop\\데이터 변'
file_pattern = os.path.join(folder_path, 'd_*.csv')

all_files = glob.glob(file_pattern)

# 모든 CSV 파일을 읽어서 하나의 DataFrame으로 병합
all_dataframes = []
for file in all_files:
    df = pd.read_csv(file, encoding='cp949')  # 여기서 필요한 인코딩을 설정하세요.
    all_dataframes.append(df)

merged_dataframe = pd.concat(all_dataframes, axis=0)

# 병합된 결과를 새로운 CSV 파일로 저장
merged_dataframe.to_csv('C:\\Users\\kmg00\\Desktop\\데이터 변\\분리수거쓰레기.csv', index=False)
