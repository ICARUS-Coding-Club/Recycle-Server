# 필요한 라이브러리를 가져옵니다.
import pandas as pd
import glob

# merge_df라는 빈 DataFrame을 초기화합니다.
# 이 DataFrame은 각 Excel 파일의 데이터를 추가하기 위해 사용됩니다.
merge_df = pd.DataFrame()

# glob.glob를 사용하여 지정된 디렉터리에서 "d_*.xlsx"라는 이름 패턴과 일치하는 모든 Excel 파일을 가져옵니다
# 이는 d_1.xlsx, d_2.xlsx 등의 파일 세트가 있을 때 유용합니다.
for f in glob.glob(r'C:\Users\kmg00\Desktop\생활쓰레기배출정보\d_*.xlsx'):
    # 파일 목록의 각 Excel 파일을 df라는 DataFrame으로 읽습니다
    df = pd.read_excel(f)

    # df의 데이터를 merge_df에 추가합니다.
    # ignore_index=True는 인덱스가 재설정되도록 하므로
    # 병합된 DataFrame에서 중복 인덱스가 발생하지 않습니다.
    merge_df = merge_df.append(df, ignore_index=True)

# 병합된 DataFrame을 콘솔에 출력합니다.
print(merge_df)

# 병합된 DataFrame을 지정된 디렉터리에 Excel 파일로 저장합니다.
merge_df.to_excel(r'C:\Users\kmg00\Desktop\생활쓰레기종합배출정보.xlsx')

