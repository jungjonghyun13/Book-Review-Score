import selenium
from selenium import webdriver
import urllib
from urllib.parse import quote
import time
import random
import pandas as pd
from bs4 import BeautifulSoup as bs

class Sumanhui:   
    def __init__(self,s1,s2,d1,d2) :
        #교재,과목, 시작날짜, 끝날짜
        self.bookName =s1
        self.subjectName =s2
        
        self.startDate =d1
        self.endDate =d2
        
        #댓글수,조회수,언급수 총합 
        self.comSum=0 
        self.hitSum=0 
        self.refSum=0

    def crawlingData(self,s1,s2,d1,d2):
        res_list = []
        pgs=0
        #driver = webdriver.Chrome("C:\\Users\\yooso\\Downloads\\chromedriver_win32\\chromedriver")
        
        driver = webdriver.Chrome("C:\\cd\\chromedriver_win32\\chromedriver")
        driver.implicitly_wait(3)
        driver.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=10197921&search.menuid=2033&search.boardtype=L")
        time.sleep(30)

    #검색어를 ms949로 encoding
        s1=s1.encode('ms949')
        s1=str(s1).replace('x','25').replace('\\','%')
        s1=s1[1:]
        s2=s2.encode('ms949')
        s2=str(s2).replace('x','25').replace('\\','%')
        s2=s2[1:]
    
    #검색어와 날짜를 제외한 기본 url
        base_url1="http://cafe.naver.com/suhui?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=10197921%26search.menuid=2033%26search.searchdate="
        base_url2="%26search.query%3D"
        base_url3="%26search.page="
        while(1):
            l=[]#리스트
            pgs+=1
        #페이지수(= str(pgs)) 넘기면서 게시글 크롤링
            driver.get(base_url1+d1+d2+base_url2+s1+' '+s2+base_url3+str(pgs))
            #print(driver.current_url)
        #switch_to_frame해주고
            driver.switch_to.frame('cafe_main')
        #검색화면에서 게시글 url 모두 긁어오기
            article_list = driver.find_elements_by_css_selector("span.aaa > a.m-tcol-c")
            article_urls=[i.get_attribute('href')for i in article_list]
            
           # print(article_urls)
        #article_urls가 빈 리스트인 경우, 게시글 끝
            if not article_urls:
                print("게시글 끝남")
                break
            else:
            #게시글에서 제목,내용,댓글,조회수,날짜,댓글수 수집
                for article in article_urls:
                    d={}#총합 저장할 사전
                    driver.get(article)
                # article도 switch_to_frame
                    driver.switch_to.frame('cafe_main')
                    soup = bs(driver.page_source, 'html.parser')
                # 게시글에서 제목 추출
                    title = soup.select('div.tit-box span.b')[0].get_text()
                  #  print(title)
                # 게시글에서 내용추출 / 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
                    content_tags = soup.select('#tbody')[0].select('p')
                    content = ' '.join([ tags.get_text() for tags in content_tags ])
                # 댓글 추출
                    comment_tags=soup.select('#cmt_list')[0].select('span.comm_body')
                    commentList=[]
                    for tags in comment_tags:
                        if(tags.get_text()!="삭제된 댓글입니다."):
                            commentList.append(tags.get_text())
                        else:
                            print("삭제된 댓글")
                    
                    comment = ' '.join(commentList)
        
                # 댓글수 추출
                    try:
                        commentNum=soup.select('div.reply-box a.reply_btn')[0].get_text()[3:]
                        
                        if(len(commentNum)>=4):
                            ScomNum=commentNum.split(",")
                            SScomNum=ScomNum[0]+ScomNum[1]
                        else:
                            SScomNum=commentNum
                        
                        self.comSum += int(SScomNum)
                    except:
                        SScomNum=0
                # 날짜 추출
                    date=soup.select('div.fr td.m-tcol-c')[0].get_text()
                # 조회수 추출
                    hitNum=soup.select('div.reply-box span.b')[1].get_text()
                    if(len(hitNum)>=4):
                        ShitNum=hitNum.split(",")
                        SShitNum=ShitNum[0]+ShitNum[1]
                    else:
                        SShitNum=hitNum
                    
                    self.hitSum += int(SShitNum)
                # 언급량 총합
                    self.refSum += 1
                # dict형태로 만들어 결과 list에 저장
                    res_list.append({'2title' : title, '3link':article ,'4content' : content,'5comment':comment,
                                 '6commentNum':SScomNum,'1date':date,'7hitNum':SShitNum})
                    
                    
            d["commentSum"]=self.comSum
            d["hitSum"]=self.hitSum
            d["refSum"]=self.refSum
            
            l.append(d)
            df = pd.DataFrame(l)
        return res_list,df
       
    def dftoCSV(self,obdf,df,s1,s2,d1,d2):
    # 결과 데이터프레임화
        cafe_df = pd.DataFrame(obdf)
        
    # csv파일로 추출
        cafe_df.to_csv('수만휘_content_'+s1+' '+s2+' '+d1+'~'+d2+'.csv', encoding='utf-8-sig', index=False)
        df.to_csv('수만휘'+'_value_'+s1+'_'+s2+' _'+d1+'~'+d2+'.csv', encoding='utf-8-sig', index=False)
        print("------파일 생성------")
                       