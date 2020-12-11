import pandas as pd
import numpy as np
'''
1. 사이트
https://www.seoul.go.kr/coronaV/coronaStatus.do
'''

#1. url 지정
url = "https://www.seoul.go.kr/coronaV/coronaStatus.do"

#2. pd.read_html 이용해서 url 사이트의 <table> 태그 필터링
table = pd.read_html(url)

#3. 4번째 확진자 정보가 저장된 테이블
df = table[3]
print("1. 확진자 정보:" ,df.shape)
print("2. 확진자 정보:" ,df.head())

#4. 파일에 저장: seoul_corona19_마지막확진일.csv
last_day = df.loc[0, "확진일"] #컬럼 뽑기
print("3. 마지막 확진일: ", last_day) #11.10 seoul_corona19_11.10.csv
#11.10 -> 11_10로 변경
last_day = last_day.replace(".", "_")
file_name = f"seoul_corona19_{last_day}.csv"

df.to_csv(file_name, index=False)

#저장된 파일 읽기
df = pd.read_csv(file_name, encoding="utf-8") #한글 처리