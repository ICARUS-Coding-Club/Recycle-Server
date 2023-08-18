import pandas as pd


def excel_to_json(input_filename, json_output_filename):
    # Excel 파일을 DataFrame 형태로 읽기
    df = pd.read_excel(input_filename)

    # DataFrame을 JSON 형식의 문자열로 변환하기
    json_str = df.to_json(orient='split', index=False, force_ascii=False)

    # UTF-8 인코딩으로 JSON 문자열을 파일에 쓰기
    with open(json_output_filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


# 예제 사용 방법:
excel_to_json(r'C:\Users\kmg00\Desktop\생활쓰레기종합배출정보.xlsx', r'C:\Users\kmg00\Desktop\Rdata\output.json')
