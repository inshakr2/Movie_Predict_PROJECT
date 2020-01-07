library(rvest)

## Title, director, Spectator, point, genre, limit of 2012~2019 Top 100 Movie // by Naver
M <- NULL
for(i in 2012:2019){
  h <- read_html(paste0('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=',i,
                        '%EB%85%84%20%EC%98%81%ED%99%94%20%EC%88%9C%EC%9C%84'))
  u <- paste0('https://search.naver.com/search.naver',html_nodes(h,xpath='//*[@id="main_pack"]/div[2]/div/div[2]/div/div[1]/div[3]/div/ul/li/div[2]/a')%>%
                html_attr('href'))
  for(I in u){
    x <- read_html(I)
    y <- html_nodes(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[3]/span')%>%
      html_text()
    z <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[1]/dd[1]/em[1]')%>%
      html_text()
    n <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/h3/a/strong')%>%
      html_text()
    g <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[1]')%>%
      html_text()
    l <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[9]')%>%
      html_text()
    d <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[2]/span/a')%>%
      html_text()
    r <- html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[3]')%>%
      html_text()
    m <- data.frame(movie=ifelse(is.na(n),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/h3/a/strong')%>%
                                   html_text()), 
                    director=ifelse(is.na(d),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[2]/span/a')%>%
                                      html_text()),
                    spectator=paste0(y,' '), 
                    point=ifelse(is.na(z),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[1]/dd[1]/em[1]')%>%
                                   html_text()),
                    genre=ifelse(is.na(g),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[1]')%>%
                                   html_text()),
                    release=ifelse(is.na(r),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[3]')%>%
                                     html_text()),
                    limit=ifelse(is.na(l),'x',html_node(x,xpath='//*[@id="_au_movie_info"]/div[2]/dl[2]/dd[1]/span[9]')%>%
                                   html_text()),
                    stringsAsFactors = F)
    M <- rbind(M,m)
  }
}

## 추석특선영화 (2012 ~ 2018 by wikipedia)
html <- read_html('https://ko.wikipedia.org/wiki/%EC%B6%94%EC%84%9D%ED%8A%B9%EC%84%A0%EC%98%81%ED%99%94#2012%EB%85%84')
thanks <- c()
for(i in 25:31){
  movie <- html_nodes(html,xpath=paste0('//*[@id="mw-content-text"]/div/div[',i,']/div[2]'))%>%
    html_text()
  thanks <- c(thanks,movie)
}
thanks <- str_replace_all(thanks,' ','')
thanks <- str_extract_all(thanks,'\\《\\w.*\\》')
for(i in 1:7){
  thanks[[i]] <- gsub('《','',thanks[[i]])
  thanks[[i]] <- gsub('》','',thanks[[i]])
}
thanks[[3]] <- thanks[[3]][-12]


## 설날특선영화 (2013 ~ 2018 by wikipedia)
html <- read_html('https://ko.wikipedia.org/wiki/%EC%84%A4%EB%82%A0%ED%8A%B9%EC%84%A0%EC%98%81%ED%99%94')
seol <- c()
for(i in 30:35){
  movie <- html_nodes(html,xpath=paste0('//*[@id="mw-content-text"]/div/div[',i,']/div[2]'))%>%
    html_text()
  seol <- c(seol,movie)
}
seol <- str_replace_all(seol,' ','')
seol <- str_extract_all(seol,'\\《\\w.*\\》')
for(i in 1:6){
  seol[[i]] <- gsub('《','',seol[[i]])
  seol[[i]] <- gsub('》','',seol[[i]])
}


## 2019 설날특선영화 (by wikipedia)
seol_2019 <- c()
for(i in 2:19){
  movie <- html_nodes(html,xpath=paste0('//*[@id="mw-content-text"]/div/div[36]/div[2]/table[1]/tbody/tr[',i,']/td[1]/a'))%>%
    html_text()
  seol_2019 <- c(seol_2019,movie)
}

for(i in 2:9){
  movie <- html_nodes(html,xpath=paste0('//*[@id="mw-content-text"]/div/div[36]/div[2]/table[2]/tbody/tr[',i,']/td[1]/a'))%>%
    html_text()
  seol_2019 <- c(seol_2019,movie)
}

for(i in 2:24){
  movie <- html_nodes(html,xpath=paste0('//*[@id="mw-content-text"]/div/div[36]/div[2]/table[3]/tbody/tr[',i,']/td[1]/a'))%>%
    html_text()
  seol_2019 <- c(seol_2019,movie)
}
seol_2019 <- str_replace_all(seol_2019,' ','')
seol[[7]] <- seol_2019