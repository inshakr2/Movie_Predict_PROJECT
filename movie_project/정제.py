# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:34:17 2020

@author: ChangYeol
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import pickle   
from selenium import webdriver
                    ##### 원본 데이터 Load #####

M = pd.read_csv('c:/movie_project/data/origin/movie.csv', encoding='cp949')
S = pd.read_csv('c:/movie_project/data/origin/seol.csv', encoding='cp949')
T = pd.read_csv('c:/movie_project/data/origin/thanks.csv', encoding='cp949')
s_day = pd.read_csv('c:/data/pro/s_day.txt',header=None)
t_day = pd.read_csv('c:/data/pro/t_day.txt',header=None)

s_day = pd.to_datetime(s_day[0])
t_day = pd.to_datetime(t_day[0])


                    ##### 1차 정제 #####
S = S.drop('Unnamed: 0', axis=1)
T = T.drop('Unnamed: 0', axis=1)

T.temp = T.temp.str.strip()
T.temp = T.temp.str.split(' ')

S.temp = S.temp.str.strip()
S.temp = S.temp.str.split(' ')

                    ##### 추석 변수에 2019 추석 추가 #####

driver = webdriver.Chrome("c:/movie_project/data/chromedriver.exe")
driver.implicitly_wait(3)
driver.get('https://ko.wikipedia.org/wiki/%EC%B6%94%EC%84%9D%ED%8A%B9%EC%84%A0%EC%98%81%ED%99%94')

driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/div[32]/span/a').click()
driver.implicitly_wait(2)
temp = [i.text for i in driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/div[32]/div[2]/ul/li/a')]
temp = pd.Series(temp)
temp = [re.sub(' ','',i) for i in temp]

T.at['7','cnt'] = 2019
T.at['7','temp'] = temp

                    ###### 추석 / 설 특선 영화로 뽑혔던 영화들에 label 추가 #####
# COPY
m = M[:]
s = S[:]
t = T[:]
m['release'] = pd.to_datetime(m['release'])

# s_label : 설날에 나온 영화 label
# t_label : 추석에 나온 영화 label
m.movie = [re.sub(' ','',i) for i in m.movie]

smovie = [j for i in s.temp for j in i]
tmovie = [j for i in t.temp for j in i]

m['s_label'] = 0
m['t_label'] = 0
for i in range(0,800):
    if pd.Series(m.iloc[i,1]).isin(smovie)[0]:
        m['s_label'][i] = 1
    elif pd.Series(m.iloc[i,1]).isin(tmovie)[0]:
        m['t_label'][i] = 1
    else:
        pass

m['s_label'].value_counts()
m['t_label'].value_counts()


# b_label : 추석과 설 모두 나온 영화 label
stmovie = list(np.intersect1d(np.array(smovie),np.array(tmovie)))

m['b_label'] = np.nan
for i in range(0,800):
    if pd.Series(m.iloc[i,1]).isin(stmovie)[0]:
        m['b_label'][i] = 1
    else :
        m['b_label'][i] = 0
m['b_label'].value_counts()



                    ##### genre one - hot coding #####
                    
x = [i.replace(' ','').split(',') for i in list(m['genre'])]
x1 = pd.DataFrame(x)
x1_unique = pd.concat([x1[0],x1[1],x1[2]])
genre_u = x1_unique[x1_unique.notnull()].unique()

x1_0 = pd.get_dummies(x1[0])
x1_1 = pd.get_dummies(x1[1])
x1_2 = pd.get_dummies(x1[2])

x_temp = x1_0.add(x1_2, fill_value=0)
x_temp = x_temp.add(x1_1, fill_value=0)
set(x_temp.columns) == set(genre_u)

m = pd.concat([m,x_temp],axis=1)


                    ##### spectator 열에 data 수정 #####
                    # scraping 과정에서 엉뚱한 data가 삽입됨
m.iloc[537,3] = 1855515
m['spectator'] = m['spectator'].astype(int)
m.info()


        ### 명절 영화들 중에 각 년도별로 상영 날짜로 부터 개봉 날짜까지의 거리 계산 ###
s_m = m.loc[m['s_label'] == 1,:]
t_m = m.loc[m['t_label'] == 1,:]
s_m = s_m.drop('Unnamed: 0', axis=1)
t_m = t_m.drop('Unnamed: 0', axis=1)
s_m['release']
s_m['release_d'] = 0
for i in range(0,len(s_m)):
    mov = s_m['movie'].iloc[i,]
    for j in range(0,len(s)):
        if s['temp'][j].count(mov) >= 1:
            mov_year = s_day[j].year
            mov_day = (s_day[j] - s_m['release'].iloc[i,]).days
            s_m['release_d'].iloc[i,] = mov_day

s_m = s_m.loc[s_m['movie'] != '집으로가는길',] # 중복 제거

t_m['release_d'] = 0
for i in range(0,len(t_m)):
    mov = t_m['movie'].iloc[i,]
    for j in range(0,len(t)):
        if t['temp'].iloc[j,].count(mov) >= 1:
            mov_year = t_day[j].year
            mov_day = (t_day[j] - t_m['release'].iloc[i,]).days
            t_m['release_d'].iloc[i,] = mov_day
t_m = t_m.loc[t_m['release_d'] >= 0 ,] # 스파이 중복이름 제거, 이름 중복되서 그냥 구간으로

# 특선 영화들의 날짜 거리로 부터 label을 부여
# s_m score
per = np.percentile(s_m['release_d'],[0,25,50,75,100])
minimum = per[0]
maximum = per[4]
Q1 = per[1]
Q2 = per[2]
Q3 = per[3]
temp = ['Bad' if (i < Q1) or (i > Q3) else 'Good' if (i  > (Q1 + Q2)/2) and (i < (Q2 + Q3)/2) else 'Normal' for i in s_m['release_d']]
s_m = pd.concat([s_m,pd.DataFrame({'score':temp})],axis=1)
s_m.info()

# t_m score
per = np.percentile(t_m['release_d'],[0,25,50,75,100])
minimum = per[0]
maximum = per[4]
Q1 = per[1]
Q2 = per[2]
Q3 = per[3]
temp = ['Bad' if (i < Q1) or (i > Q3) else 'Good' if (i  > (Q1 + Q2)/2) and (i < (Q2 + Q3)/2) else 'Normal' for i in t_m['release_d']]
t_m = pd.concat([t_m,pd.DataFrame({'score':temp})],axis=1)
t_m.info()



## 원시 데이터에 label 달기 작업
# 1. 2019 추석으로 부터 개봉날짜 까지의 거리 열 추가 (2019-09-13)
m['rel_td'] = (pd.to_datetime('2019-09-13') - m['release']).dt.days

# 2. 해당 열을 기반으로 label을 추가
per = np.percentile(t_m['release_d'],[0,25,50,75,100])
minimum = per[0]
maximum = per[4]
Q1 = per[1]
Q2 = per[2]
Q3 = per[3]
m['t_score'] = ['Bad' if (i < Q1) or (i > Q3) else 'Good' if (i  > (Q1 + Q2)/2) and (i < (Q2 + Q3)/2) else 'Normal' for i in m['rel_td']]


# 3. 2020 설로 부터 개봉 날짜 까지의 거리 열 추가 (2020-01-25)
m['rel_sd'] = (pd.to_datetime('2020-01-25') - m['release']).dt.days

# 4. 해당 열을 기반으로 label을 추가 
per = np.percentile(s_m['release_d'],[0,25,50,75,100])
minimum = per[0]
maximum = per[4]
Q1 = per[1]
Q2 = per[2]
Q3 = per[3]
m['s_score'] = ['Bad' if (i < Q1) or (i > Q3) else 'Good' if (i  > (Q1 + Q2)/2) and (i < (Q2 + Q3)/2) else 'Normal' for i in m['rel_sd']]






                    ##### 저장 ##### 
  
file = open('c:/movie_project/data/movie_z.csv','wb')  
pickle.dump(m,file)
file.close()

file = open('c:/movie_project/data/s_movie_z.csv','wb')  
pickle.dump(s,file)
file.close()

file = open('c:/movie_project/data/t_movie_z.csv','wb')  
pickle.dump(t,file)
file.close()

file = open('c:/movie_project/data/seol_movie.csv','wb')  
pickle.dump(s_m,file)
file.close()

file = open('c:/movie_project/data/thanks_movie.csv','wb')  
pickle.dump(t_m,file)
file.close()