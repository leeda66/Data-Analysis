'''
 서울시 코로나19  데이터 수집 및 분석
   19. 여행력 빈도수 및 시각화
'''
import pandas as pd
import numpy as np

# 저장된 파일 읽기
from matplotlib.fontconfig_pattern import family_escape

df = pd.read_csv("seoul_corona19_11_10_.csv", encoding="utf-8")  # 한글처리

# 2.  '연번' 기준으로 오름차순 정렬
df = df.sort_values(by="연번", ascending=False)
print("2. '연번' 기준으로 오름차순 정렬 \n", df.head())

# 3. 확진일에 빈도수 ==> 어느 날짜에 가장 많이 확진이 되었는지 확인 가능
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

kkk = df["확진일"].str.replace(".", "-")
kkk = kkk.apply(lambda n: n[:-1])
df["확진일자"] = pd.to_datetime("2020-" + kkk)
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
df["월-일"] = df["확진일자"].astype(str).apply(lambda n: n[-5:])
print("7. '확진일자' 컬럼 이용하여 '월-일' 컬럼 추가  \n", df.head())
print("*" * 20)
######################################################################
print(df.head())
# 19. 여행력 빈도수 및 시각화
contact_count = df['여행력'].value_counts().sort_values()
print("여행력 빈도수 확인 \n", contact_count)
print(df['여행력'].unique())
'''
  1) "-" ==> NaN 변경
  2) 공통명으로 변경

    '아랍에미리트','UAE' ==> 아랍에미리트
    '중국 청도','우한교민','우한 교민', '중국 우한시','중국' ==> 중국
    '프랑스, 스페인', '스페인, 프랑스' ==> 프랑스, 스페인
    체코,헝가리,오스트리아,이탈리아,프랑스,모로코,독일,스페인,영국,
    폴란드,터키,아일랜드 ==> 유럽

    브라질,아르헨티아,칠레,볼리비아,멕시코,페루 ==> 남미
'''
df['해외'] = df["여행력"]
print(df.head())
df.loc[df["해외"].str.contains("아랍에미리트|UAE"), "해외"] = "아랍에미리트"
df.loc[df["해외"].str.contains("중국|우한"), "해외"] = "중국"
df.loc[df["해외"].str.contains("체코|헝가리|오스트리아|이탈리아|프랑스|모로코|독일|스페인|영국|폴란드|터키|아일랜드"),
       "해외"] = "유럽"
df.loc[df["해외"].str.contains("브라질|아르헨티아|칠레|볼리비아|멕시코|페루"), "해외"] = "남미"

df['해외'] = df["해외"].str.replace("-", "NAN")
contact_count = df["해외"].value_counts()
print("여행력 빈도수 확인 \n", contact_count)
print(df['해외'].unique())

#상위 15개정도만 추출해서 시각화
tmp=df["해외"].value_counts()[1:16].sort_values()
print(tmp)
import matplotlib.pyplot as plt
plt.rc("font", family="AppleGothic") # 한글처리
g=tmp.plot.barh(title="해외 확진자수 현환", figsize=(10,8))
for i in range(len(tmp)):
    day_count = tmp.iloc[i]
    g.text(x=day_count, y=i, s=day_count, fontsize=14, color="r")
plt.show()