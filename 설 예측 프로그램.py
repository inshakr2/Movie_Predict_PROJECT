# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:27:11 2020

@author: ChangYeol
"""

def seol_2020():
                    ##### import section #####
                    
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import pickle 
    from sklearn.tree import DecisionTreeClassifier as DTC
    from sklearn.cluster import KMeans
    from sklearn.ensemble import RandomForestClassifier
    import nltk
    
                    ##### data load section #####

    file = open('c:/movie_project/data/movie_z.csv','rb')
    m = pickle.load(file)
    file.close()
        # release 컬럼을 datatime으로 변환       
    m['release'] = pd.to_datetime(m['release'])
    
    file = open('c:/movie_project/data/s_movie_z.csv','rb')
    s = pickle.load(file)
    file.close()
    
    file = open('c:/movie_project/data/t_movie_z.csv','rb')
    t = pickle.load(file)
    file.close()
    
    file = open('c:/movie_project/data/seol_movie.csv','rb')
    s_m = pickle.load(file)
    file.close()
    
    file = open('c:/movie_project/data/thanks_movie.csv','rb')
    t_m = pickle.load(file)
    file.close()
        # 추석 / 설날 날짜 가져오기
    s_day = pd.read_csv('c:/data/s_day.txt',header=None)
    t_day = pd.read_csv('c:/data/t_day.txt',header=None)
    
    s_day = pd.to_datetime(s_day[0])
    t_day = pd.to_datetime(t_day[0])
    

                    #### 2020_seol Predict #####    
    
    ### 1. training data Z                    
    tr_data = m.iloc[:,[2,3,35]]
    tr_data = pd.concat([tr_data,m.loc[:,'SF':'판타지']],axis=1)
    tr_data = pd.concat([tr_data,pd.get_dummies(tr_data['s_score'], prefix='score')],axis=1)
    tr_data = tr_data.drop('s_score',axis=1)
    
    
    
    ### 2. Decision Tree
    model5 = DTC(max_depth=10)
    model5.fit(tr_data,m['s_label'])
    exp = model5.predict(tr_data)
    m['temp_exp'] = exp
    
    seol_exp1 = m.loc[m['temp_exp'] == 1, 'movie']  # Decision_Tree predict
    
    ### 3. RandomForest
    model6= RandomForestClassifier(n_estimators=1000, oob_score=True, random_state=0)
    model6.fit(tr_data,m['s_label'])
    exp = model6.predict(tr_data)
    m['temp_exp'] = exp
    
    seol_exp2 = m.loc[m['temp_exp'] == 1, 'movie']  # RandomForest predict
    
    ### 4. Naive Bayes
    temp_x = list()
    for i in range(0,len(m)):
        temp_x.append((tr_data.iloc[i,2:],m.iloc[i,7]))
    model7 = nltk.NaiveBayesClassifier.train(temp_x)
#    model7.show_most_informative_features()
    
    temp_tr = [dict(tr_data.iloc[i,2:]) for i in range(0,len(tr_data))]
    temp_lb = [model7.classify(temp_tr[i]) for i in range(0,len(temp_tr))]
    
    m['temp_exp'] = temp_lb
    seol_exp3 = m.loc[m['t_exp'] == 1,'movie']      # Naive_Bayes predict
    
    
                        #### 2019_thanks predict #####

    result_s = pd.DataFrame(columns=['Method','Expectation'],
                        index=[0,1,2])

    result_s.at[0,'Method'] = 'Decision_Tree'
    result_s.at[0,'Expectation'] = list(seol_exp1)
    
    result_s.at[1,'Method'] = 'Random_Forest'
    result_s.at[1,'Expectation'] = list(seol_exp2)
    
    result_s.at[2,'Method'] = 'Naive_Bayes'
    result_s.at[2,'Expectation'] = list(seol_exp3)
    
    ### save point ###
    
    file = open('c:/movie_project/predict/seol_result.csv','wb')  
    pickle.dump(result_s,file)
    file.close()
    
    file = open('c:/movie_project/predict/seol_result.csv','rb')
    result_s = pickle.load(file)
    file.close()  


                    ##### predict PRINT #####
                    
    total_s = list()
    [total_s.append(j) for i in result_s['Expectation'] for j in i]
    total_s = pd.Series(total_s).unique()
    
    print('예측한 영화는\n',total_s)


seol_2020()
