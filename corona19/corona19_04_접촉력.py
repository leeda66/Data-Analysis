'''
 서울시 코로나19  데이터 수집 및 분석
   17. 접촉력 빈도수 및 시각화
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
# 17. 접촉력 빈도수 및 시각화
contact_count = df['접촉력'].value_counts()
print("접촉력 빈도수 확인 \n", contact_count)
print(df['접촉력'].unique())

# '대구 거주' 와 '대구 거주자', '대구 XXXX' =====> 대구 로 변경
print("변경전:", df.loc[df["접촉력"].str.contains("대구"), "접촉력"].unique())
df.loc[df["접촉력"].str.contains("대구"), "접촉력"] = "대구"
print("변경후:", df.loc[df["접촉력"].str.contains("대구"), "접촉력"].unique())

'''
   공통단어로 통일
   1) XXX 대구 XXXX ==> 대구
   2) XXX 교회 XXXX|기도|성경|성당 ==> 종교시설
   3) 의료원|요양|병원 ==> 의료시설
   4) 확인 중|확인중|감염경로 조사중 ===> 확인 중
'''
# print("변경전:", df.loc[df["접촉력"].str.contains("확인|요양"), "접촉력"].unique())
df.loc[df["접촉력"].str.contains("의료원|요양|병원"), "접촉력"] = "의료시설"
df.loc[df["접촉력"].str.contains("교회|기도|성경|성당"), "접촉력"] = "종교시설"
df.loc[df["접촉력"].str.contains("확인 중|확인중|감염경로 조사중"), "접촉력"] = "확인 중"
print(df['접촉력'].unique())
contact_count = df['접촉력'].value_counts()
print(contact_count.head(20))
contact_count = contact_count.head(20).sort_values()
# 접촉력 상위 20개 막대 그래프로 시각화
import matplotlib.pyplot as plt
plt.rc("font", family="AppleGothic") # 한글처리
g=contact_count.plot.barh(title="월별 확진자수", figsize=(10,8))
for i in range(len(contact_count)):
    day_count = contact_count.iloc[i]
    g.text(x=day_count, y=i, s=day_count, fontsize=14, color="r")
plt.axhline(800, color="r", linestyle="--")
plt.show()