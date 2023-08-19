import openpyxl
import json
import warnings

#openpyxl 경고창 무시
warnings.simplefilter(action='ignore', category=UserWarning)

excel=r'C:\Users\kmg00\Desktop\생활쓰레기배출정보\d_대구.xlsx'
json_f=r'C:\Users\kmg00\Desktop\Rdata\생활쓰레기종합배출정보.json'
#액셀 열기
wb=openpyxl.load_workbook(excel,read_only=True)

#첫번째 시트 가지고 오기
sheet=wb.worksheets[0]

#맨 윗줄을 키갑스오 사용

key_list=[]
for col in range(1,sheet.max_column+1):
    key_list.append(sheet.cell(row=1,column=col).value)

#{}로 만들기
# 마지막 행을 참조
data = []
for row in range(2, sheet.max_row + 1):
    temp = {}
    for col in range(1, sheet.max_column + 1):
        val = sheet.cell(row=row, column=col).value
        temp[key_list[col-1]] = val

    data.append(temp)



#액셀 닫기
wb.close()

print(data)

#json으로 내보내기
try:
    with open(json_f, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error while saving to {json_f}: {e}")


print('성공')
