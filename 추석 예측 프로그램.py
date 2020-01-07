# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:44:50 2020

@author: ChangYeol
"""

def thanks_2019():
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
    

                    #### 2019_thanks Model #####
    
    ### 1. training data 정제
    tr_data = m.iloc[:,[2,3,33]]
    tr_data = pd.concat([tr_data,m.loc[:,'SF':'판타지']],axis=1)
    tr_data = pd.concat([tr_data,pd.get_dummies(tr_data['t_score'], prefix='score')],axis=1)
    tr_data = tr_data.drop('t_score',axis=1)
       
    
    ### 2. Decision Tree
    model = DTC(max_depth=20)
    model.fit(tr_data,m['t_label'])
    exp = model.predict(tr_data)
    m['temp_exp'] = exp
    
    thanks_exp1 = m.loc[m['temp_exp'] == 1, 'movie']  # 예측영화
    thanks_corr1 = thanks_exp1[m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,])] # 맞춘영화
    thanks_acc1 = sum(m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,]))/len(thanks_exp1) # 정확도
    #model.feature_importances_
    
    ### 3. RandomForest
    model2= RandomForestClassifier(n_estimators=1000, oob_score=True, random_state=0)
    model2.fit(tr_data,m['t_label'])
    exp = model2.predict(tr_data)
    m['temp_exp'] = exp
    
    thanks_exp2 = m.loc[m['temp_exp'] == 1, 'movie']  # 예측영화
    thanks_corr2 = thanks_exp2[m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,])] # 맞춘영화
    thanks_acc2 = sum(m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,]))/len(thanks_exp2) # 정확도
    
    ### 4. Naive Bayes
    temp_x = list()
    for i in range(0,len(m)):
        temp_x.append((tr_data.iloc[i,2:],m.iloc[i,8]))
    model3 = nltk.NaiveBayesClassifier.train(temp_x)
    #model3.show_most_informative_features()
    
    temp_tr = [dict(tr_data.iloc[i,2:]) for i in range(0,len(tr_data))]
    temp_lb = [model3.classify(temp_tr[i]) for i in range(0,len(temp_tr))]
    m['temp_exp'] = temp_lb
    
    thanks_exp3 = m.loc[m['temp_exp'] == 1,'movie']  # 이번 추석 예측
    thanks_corr3 = thanks_exp3[m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,])]  # 맞춘 영화
    thanks_acc3 = sum(m.loc[m['temp_exp'] == 1, 'movie'].isin(t['temp'].iloc[7,]))/len(thanks_exp3)  # 정확도
    
    # KMeans 실패 (X)
#    model4 = KMeans(n_clusters = 2)
#    model4.fit(tr_data)
#    colormatp = np.array(['crimson','coral',])
#    centers = pd.DataFrame(model4.cluster_centers_)
#    
#    plt.figure(figsize=(14,7))
#    plt.scatter(tr_data.iloc[:,0],tr_data.iloc[:,1], c=colormatp[model3.labels_], s=10)
#    plt.scatter(centers.iloc[:,0], centers.iloc[:,1], s=60, marker='D', c='g')




                    #### 2019_thanks predict #####
    result_t = pd.DataFrame(columns=['Method','Expectation','Correct_Answer','Accuracy'],
                            index=[0,1,2])
    result_t.at[0,'Method'] = 'Decision_Tree'
    result_t.at[0,'Expectation'] = list(thanks_exp1)
    result_t.at[0,'Correct_Answer'] = list(thanks_corr1)
    result_t.at[0,'Accuracy'] = thanks_acc1
    
    result_t.at[1,'Method'] = 'Rnadom_Forest'
    result_t.at[1,'Expectation'] = list(thanks_exp2)
    result_t.at[1,'Correct_Answer'] = list(thanks_corr2)
    result_t.at[1,'Accuracy'] = thanks_acc2
    
    result_t.at[2,'Method'] = 'Naive_Bayes'
    result_t.at[2,'Expectation'] = list(thanks_exp3)
    result_t.at[2,'Correct_Answer'] = list(thanks_corr3)
    result_t.at[2,'Accuracy'] = thanks_acc3
    
    ### save point ###
    
    file = open('c:/movie_project/predict/thanks_result.csv','wb')  
    pickle.dump(result_t,file)
    file.close()
    
    file = open('c:/movie_project/predict/thanks_result.csv','rb')
    result_t = pickle.load(file)
    file.close()
    
    
                        ##### predict PRINT #####
                        
    total_t = list()
    [total_t.append(j) for i in result_t['Expectation'] for j in i]
    total_t = pd.Series(total_t).unique()
    
    idx = pd.Series(total_t).isin(t['temp'].iloc[7,])
    total_exp_t = pd.Series(total_t)[idx]
    total_acc_t = len(total_exp_t) / len(total_t)
    
    
    
    print('모든 모델이 예측한 영화는',total_t)
    print('\n\n그 중에 맞춘 영화는',list(total_exp_t))
    print('\n\n\n정확도는',total_acc_t)
    
#    len(t.iloc[7,1]) # 2019 추석에 나온 영화 수
#    len(total_t) # 총 예측 수
#    len(total_exp_t) # 총 맞춘 수
#    len(total_exp_t) / len(total_t) # 정확도                        
    
    
thanks_2019()


















  
    
    
    
    
    