'''
 서울시 코로나19  데이터 수집 및 분석
   15. 모든 날짜 출력 ( 확진자가 없는 날짜로 포함 )
   16. NaN을 0으로 변경 및 모두 int로 변경 + '누적확진자수' 컬럼추가
'''
import pandas as pd
import numpy as np

# 저장된 파일 읽기
from matplotlib.fontconfig_pattern import family_escape

df = pd.read_csv("seoul_corona19_11_10_.csv", encoding="utf-8") # 한글처리

# 2.  '연번' 기준으로 오름차순 정렬
df = df.sort_values(by="연번", ascending=False)
print("2. '연번' 기준으로 오름차순 정렬 \n", df.head())


#3. 확진일에 빈도수 ==> 어느 날짜에 가장 많이 확진이 되었는지 확인 가능
# value_counts() : 빈도수값을 내림차순으로 정렬해서 반환
print("3. 확진일에 빈도수 \n", df["확진일"].value_counts())

#  4. '확진일자' 컬럼 추가 ==> 2020-11-10 형식
'''
   기존의 확진일은 문자이기 때문에 날짜로 변경해야 된다
   가.  11.10 ---> 11-10 변경
   나. 11-10 ---> 2020-11-10로 변경 ( 문자열 연결)
   다. 2020-11-10 문자열을 날짜로 변경 ( pd.to_datetime() 함수 )
   라. df["확진일자"] = 날짜
'''
# df["확진일자"]= pd.to_datetime("2020-"+df["확진일"].str.replace(".","-"))
# print("4. '확진일자' 컬럼 추가  \n", df.head())

kkk = df["확진일"].str.replace(".","-")
kkk = kkk.apply(lambda n:n[:-1])
df["확진일자"]= pd.to_datetime("2020-"+kkk)
print("4. '확진일자' 컬럼 추가  \n", df.head())

# 5. '확진일자' 컬럼 이용하여 '월'컬럼 추가
df["월"] = df["확진일자"].dt.month
print("5. '확진일자' 컬럼 이용하여 '월' 컬럼 추가  \n", df.head())

# 6. '확진일자' 컬럼 이용하여 '주'컬럼 추가
df["주"] = df["확진일자"].dt.isocalendar().week
print("6. '확진일자' 컬럼 이용하여 '주' 컬럼 추가  \n", df.head())

# 7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가 > 11-10 형식
'''
   1) 날짜 데이터 '확진일자' --> 문자 데이터로 변경하고
   2) 변경된 문자데이터에서 슬라이싱 
   ( Series에 적용하기 때문에 슬라이싱 기능의 함수 + apply 함수 )
   예> 2020-11-10 -->  11-10
'''
df["월-일"] = df["확진일자"].astype(str).apply(lambda n:n[-5:])
print("7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가  \n", df.head())
print("*" * 20)
######################################################################
print(df.head())
print(df.tail())

# 15. 모든 날짜 출력 ( 확진자가 없는 날짜로 포함 )
'''
    1)확진자 발생된 날짜 ~  확진자가 발생된 마지막 날짜 ==> df_days
      인덱스   확진일자
      0       2020-01-24
      1       2020-01-25
      ..
      
      3400    2020-11-10
    2) 확진 발생된 날짜  ==> df_daily_case
     인덱스        확진수
     2020-01-24    1
     2020-01-30    3
     ..
'''
# 전체날짜 만들기 --> iloc[행인덱스, 열의인데ㄱ스]
print(df.columns)
first_day = df.iloc[-1, 7] # 맨뒤 행의 8번째 컬럼값(확진일자 컬럼)
last_day = df.iloc[0,7]
print(first_day, last_day)
days = pd.date_range(first_day, last_day)
# print(days)
df_days = pd.DataFrame({"확진일자":days})
print("전체 날짜 \n", df_days)

# 확진일자별 빈도수
result = df["확진일자"].value_counts().sort_index()
df_daily_case = result.to_frame()
df_daily_case.columns=["확진수"]
# print(result, type(result))
# print(df_daily_case, type(df_daily_case))

# df_days ,df_daily_case 병합
all_day = pd.merge(df_days, df_daily_case,
                   left_on="확진일자",
                   right_on=df_daily_case.index,
                   how="left")
print("15. 모든 날짜 출력 ( 확진자가 없는 날짜로 포함 )\n", all_day)

# 16. NaN을 0으로 변경 및 모두 int로 변경 + '누적확진자수' 컬럼추가
all_day = all_day.fillna(0)
all_day["확진수"] = all_day["확진수"].astype(int)
all_day["누적확진자수"] = all_day["확진수"].cumsum()
print("16. '누적확진자수' 컬럼추가: \n", all_day)

# 17. 일자별 확진자수 및 누적확진자수 시각화
all_day["일자"] = all_day["확진일자"]\
          .astype(str).apply(lambda n:n[-5:])
all_day = all_day[["일자","확진수","누적확진자수"]]
cum_all_day = all_day.set_index("일자")
print(cum_all_day)

import matplotlib.pyplot as plt
plt.rc("font", family="AppleGothic") # 한글처리
plt.rc("ytick", labelsize=18)
plt.rc("xtick", labelsize=18)
plt.style.use("fivethirtyeight")
cum_all_day.plot(title="일자별 확진자수 및 누적확진자수 시각화", figsize=(9,6))
# plt.axhline(100, color="r", linestyle="--")
plt.show()
# help(plt.axhline)