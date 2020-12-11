import pandas as pd
import numpy as np
'''
서울시 코로나19 데이터 수집 및 분석
2. '연번' 기준으로 오름차순 정렬
3. 확진일에 빈도수 -> 어느 날짜에 가장 많이 확진이 되었는지 확인 가능
4. '확진일자' 컬럼 추가 -> 2020-11-10 형식
5. '확진일자' 컬럼 이용하여 '월' 컬럼 추가
6. '확진일자' 컬럼 이용하여 '주' 컬럼 추가
7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가 -> 11-10 형식
8. 확진자 수가 가장 많은 날 출력
9. 확진자수가 가장 많은 날 발생이력
10. 일자별 확진자수 선그래프로 시각화
11. 월-일별 확진자수 선그래프로 시각화 + 갯수값 시각화
12. 월별 확진자수 막대그래프로 시각화 + 갯수값 시각화
13. 월-일별 확진자수중에서 최근 데이터 50개만 선그래프로 시각화 + 갯수값 시각화
14. "주"별 확진자수 막대그래프로 시각화
'''

#저장된 파일 읽기
df = pd.read_csv("seoul_corona19_11_10_.csv", encoding="utf-8") #한글처리

#2. '연번' 기준으로 오름차순 정렬
df = df.sort_values(by="연번", ascending=False)
print("2. '연번' 기준으로 오름차순 정렬 \n", df.head())

#3. 확진일에 빈도수 -> 어느 날짜에 가장 많이 확진이 되었는지 확인 가능
# value_counts() : 빈도수값을 내림차순으로 정렬해서 반환
print("3. 확진일에 빈도수 \n", df["확진일"].value_counts())

#4.'확진일자' 컬럼 추가 -> 2020-11-10 형식
'''
    기존의 확진일은 문자이기 때문에 날짜로 변경해야 된다.
    가. 11.10 -> 11-10로 변경
    나. 11-10 -> 2020-11-10로 변경 (문자열 연결)
    다. 2020-11-10 문자열을 날짜로 변경 (pd.to_datetime() 함수)
    라. df["확진일자"] = 날짜
'''

df["확진일자"] = pd.to_datetime("2020-"+df["확진일"].str.replace(".", "-"))
print("4. '확진일자' 컬럼 추가 \n", df.head())
'''
방법2
temp = df["확진일"].str.replace(".", "-")
temp = temp.apply(lambda n:n[:-1])
df["확진일자"] = pd.to_datetime("2020-"+temp)
print("4. '확진일자' 컬럼 추가 \n", df.head())
'''

#5. '확진일자' 컬럼 이용하여 '월' 컬럼 추가
df["월"] = df["확진일자"].dt.month
print("5. '확진일자' 컬럼 이용하여 '월' 컬럼 추가 \n", df.head())

#6. '확진일자' 컬럼 이용하여 '주' 컬럼 추가
df["주"] = df["확진일자"].dt.isocalendar().week
print("6. '확진일자' 컬럼 이용하여 '주' 컬럼 추가 \n", df.head())

#7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가 -> 11-10 형식
'''
    날짜 데이터 '확진일자' -> 문자 데이터로 변경하고
    변경된 문자데이터에서 슬라이싱 (Series에 적용하기 때문에 슬라이싱 기능의 함수 + apply 함수)
    ex. 2020-11-10 -> 11-10
'''
df["월-일"] = None
df["월-일"] = df["확진일자"].astype(str).apply(lambda n:n[-5:])
print("7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가 \n", df.head())


# 8. 확진자 수가 가장 많은 날 출력
'''
    '월-일' 컬럼값의 빈도수 이용
'''
day_count = df["월-일"].value_counts()
print(day_count)
max_day = day_count[day_count == day_count.max()]
print("8. 확진자수가 가장 많은 날 출력  \n", max_day)
print("8. 확진자수가 가장 많은 날 출력  \n", max_day.index[0])

max_day2 = df["월-일"].value_counts().index[0]
print("8. 확진자수가 가장 많은 날 출력  \n", max_day2)

# 9. 확진자수가 가장 많은 날 발생이력
max_day_df = df[df["월-일"] == max_day.index[0]]
print("9. 확진자수가 가장 많은 날 발생이력  \n", max_day_df)

'''
  시각화 방법 
  1) matplotlib 라이브러리 사용
    https://matplotlib.org/
  2) matplotlib + seaborn 라이브러리 사용
  3) matplotlib + pandas 사용 ( pandas에 matplotlib 기능 포함 )
    https://pandas.pydata.org/

    pip install matplotlib
    pip install seaborn
'''
import matplotlib.pyplot as plt

plt.rc("font", family="AppleGothic")  # 한글처리

# 10. 확진일자별 확진자수 선그래프로 시각화
# 인덱스(날짜)==> x 축으로  값: y축으로 설정
result = df["확진일자"].value_counts().sort_index()
print(result)
result.plot(title="일자별 확진자수", figsize=(9,6))
plt.axhline(100, color="r", linestyle="--")
plt.show()
help(plt.axhline)


# 11. 월-일별 확진자수 선그래프로 시각화 + 갯수값 시각화
result = df["월-일"].value_counts().sort_index()
print(result)
g=result.plot(title="월별 확진자수", figsize=(20,8))
# print(help(g.text))
############################
for i in range(len(result)):
    day_count = result.iloc[i]
    # print("갯수:", day_count)
    if day_count > 100:
        g.text(x=i, y=day_count, s=day_count, fontsize=14, color="r")
#################################
plt.axhline(100, color="r", linestyle="--")
plt.show()

# 12. 월별 확진자수 막대그래프로 시각화 + 갯수값 시각화
result = df["월"].value_counts().sort_index()
print(result)
g=result.plot.bar(title="월별 확진자수", figsize=(10,8))
for i in range(len(result)):
    day_count = result.iloc[i]
    g.text(x=i, y=day_count, s=day_count, fontsize=14, color="r")
plt.axhline(1500, color="r", linestyle="--")
plt.show()

# 13. 월-일별 확진자수중에서 최근 데이터 50개만 선그래프로 시각화 + 갯수값 시각화
result = df["월-일"].value_counts().sort_index()
print(result)
result = result[-50:]  # 50개만 슬라이싱
g = result.plot(title="월별 확진자수", figsize=(20, 8))
# print(help(g.text))
############################
for i in range(len(result)):
    day_count = result.iloc[i]
    g.text(x=i, y=day_count, s=day_count, fontsize=14, color="r")
#################################
plt.axhline(35, color="r", linestyle="--")
plt.show()

# 14. "주"별 확진자수 막대그래프로 시각화
result = df["주"].value_counts().sort_index()
print(result)
g = result.plot.bar(title="주별 확진자수", figsize=(10, 8))
for i in range(len(result)):
    day_count = result.iloc[i]
    g.text(x=i, y=day_count, s=day_count, fontsize=14, color="r")
plt.axhline(400, color="r", linestyle="--")
plt.show()

