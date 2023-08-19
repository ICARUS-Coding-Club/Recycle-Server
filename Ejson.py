import pandas as pd
import json

def excel_to_json(input_filename, json_output_filename):
    # Read Excel file as DataFrame
    df = pd.read_excel(input_filename)

    # Convert DataFrame to a list of dictionaries
    records = df.to_dict(orient='records')

    # Write the list of dictionaries to a file in JSON format
    with open(json_output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(records, json_file, ensure_ascii=False, indent=4)

# 예제 사용 방법:
excel_to_json(r'C:\Users\kmg00\Desktop\생활쓰레기종합배출정보.xlsx', r'C:\Users\kmg00\Desktop\Rdata\output.json')
