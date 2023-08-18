import pandas as pd


def excel_to_json(input_filename, json_output_filename):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_filename)

    # Convert the DataFrame to JSON format (string)
    json_str = df.to_json(orient='split', index=False, force_ascii=False)

    # Write the JSON string to a file with UTF-8 encoding
    with open(json_output_filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)


# Example usage:
excel_to_json(r'C:\Users\kmg00\Desktop\생활쓰레기종합배출정보.xlsx', r'C:\Users\kmg00\Desktop\Rdata\output.json')
