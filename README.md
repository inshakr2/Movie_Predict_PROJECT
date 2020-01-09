# 특선 영화 예측 모델

2012 ~ 2019 설 특선영화까지를 학습 데이터로 하여

2019 추석, 2020 설 특선영화를 예측하는 모델입니다.           __By. 유창열__




## 구축환경

기본적으로 Python을 기반으로 작성하였으며, Data Scaraping과 분석을 위한 시각화는 R을 이용하였습니다.

Python에서 사용한 핵심 모듈은 아래와 같습니다.

__1. sklearn__
  * DecisionTreeClassifier
  * KMeans
  * RandomForestClassifier
  
__2. nltk__
  * NaiveBayesClassifier

__3. pandas__

__4. numpy__




## 실행방법


    깃 허브에서 file을 모두 다운로드 받으시고, 

    movie_project file을 C drive 바로 밑에 둡니다.
    
    
    다음으로 함께 첨부되어 있는 py 파일을 Python에서 open 하시어 생성되어 있는 함수를 실행합니다.




## 결과 및 간단한 시각화

* __Predict 결과는 Result Folder의 txt file에 첨부하였습니다.__

* __설 영화 장르 분석 시각화__

![image](https://user-images.githubusercontent.com/59518805/71890073-e07eb380-3186-11ea-82c2-fe50d9c70c8e.png)

* __추석 영화 장르 분석 시각화__

![image](https://user-images.githubusercontent.com/59518805/71890271-42d7b400-3187-11ea-8df3-e79dceb44ce8.png)

* __모든 영화 관객수 별 평점과 등장한 감독 빈도수를 이용한 Wordcloud__

![image](https://user-images.githubusercontent.com/59518805/71890639-13757700-3188-11ea-979e-94e662b1f072.png)

## Version 2. 개선점

1. __관객수 feature__ 의 scale 작업


1. __개봉일 feature__ 의 기존 label 작업 수정
   > 사분위수를 기준으로 구간을 명목형으로 나눴던 것을 수치형으로 만들 수 있는 함수를 생성

![image](https://user-images.githubusercontent.com/59518805/71889335-4702d200-3185-11ea-9456-b464c008c04b.png)


## 한계

__1. data를 지속적으로 최신화하려 했으나 scraping에 Block.__
   > main data가 19.08.25 기준으로 고정되어 버렸습니다.
   >
   > 프로그램을 실행시키면 새로운 data를 다운로드할 수 있도록 programming 하려 하였으나 
   >
   > Block에 의해 계획에 차질이 생겼습니다.
   
__2. 그 해에 issue가 되거나 시리즈 영화가 개봉하였을 경우, 예외적으로 이상치에 해당하는 영화가 선정되는 경우가 있다.__


## Data 출처

[영화 by.naver](https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%97%AD%EB%8C%80+%EC%98%81%ED%99%94+%EC%88%9C%EC%9C%84&oquery=2020%EB%85%84+%EC%98%81%ED%99%94+%EC%88%9C%EC%9C%84&tqi=UmeBmlp0YiRss57CbjKssssst78-217013)
  > 모든 영화의 data를 수집한 Site 입니다. 
  
[역대 설 특선 영화 by.wiki](https://ko.wikipedia.org/wiki/%EC%84%A4%EB%82%A0%ED%8A%B9%EC%84%A0%EC%98%81%ED%99%94)

[역대 추석 특선 영화 by.wiki](https://ko.wikipedia.org/wiki/%EC%B6%94%EC%84%9D%ED%8A%B9%EC%84%A0%EC%98%81%ED%99%94)
  > 역대 추석 및 설 특선 영화를 수집한 Site 입니다.
