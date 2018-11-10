import requests, operator, glob2
from pandas import DataFrame
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from functools import reduce
from math import ceil

# coding: utf-8

# In[ ]:

class Naver:        
    def __init__(self,s1,s2,d1,d2) :
        #교재,과목, 시작날짜, 끝날짜
        self.bookName =s1
        self.subjectName =s2
        
        self.startDate =d1
        self.endDate =d2
        
        #댓글수,조회수,언급수 총합 
        self.comSum=0 
 #       self.hitSum=0 
        self.refSum=0
        
        
    def bringPages(self,oburl):
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("body")
        all2=all.find("div",{"id":"wrap"})
        all3=all2.find("div",{"id":"container"})
        all4=all3.find("div",{"id":"s_content"})
        all5=all4.find("div",{"class":"section"})
        all6=all5.find("h2")
        all7=all6.find("span",{"class":"number"})
        all8=all7.find("em")
        pages=all8.text
        
        #ex) (1-10/619) p3이 게시글 수, "," 예외처리
        p=pages[5:]
        if(len(p)>=5):
            p=pages[5:6]
            p2=pages[7:]
            p3=p+p2
        elif(len(p)==0):
            p=pages[4:]
            p3=p
        else:
            p3=p
        self.refSum=p3
        return ceil(int(p3)/10)
  
    def bringContent(self,oburl):
        return_list=""
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"c-heading__content"})
        if not all:
            return_list = ""
        else:
            return_list=all.text
        
        return return_list
    
    def bringComment(self,oburl):
        return_list=""
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"answer-content__list _answerList"})
        all2=all.find_all("div",{"class":"_endContentsText c-heading-answer__content-user"})

        for item in all2:
            return_list=item.text
        
        return return_list
    
    def bringCommentNum(self,oburl):
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"c-classify__title-part"})
        all2=all.find("em",{"class":"_answerCount num"}).text
        midcNum=all2
        if(len(midcNum)>=4):
            NmidcNum=midcNum.split(",")
            Nfinal_cNum=NmidcNum[0]+NmidcNum[1]
        else:
            Nfinal_cNum=midcNum
        return int(Nfinal_cNum)

    def crawlingData(self,s1,s2,d1,d2):
        self.bookName = s1
        self.subjectName = s2

        self.startDate = d1
        self.endDate = d2

        l=[]#리스트
        l2=[]#총합 저장할 리스트
        
        urlf="https://kin.naver.com/search/list.nhn?sort=date&query="+self.bookName+"%20%26quot%3B"+self.subjectName+"&period="+self.startDate+"%7C"+self.endDate+"&section=kin&page="
    
       # print(self.bringPages(urlf+"1"))
        pgs=self.bringPages(urlf+"1")
        
        for page in range(pgs):
            r = requests.get(urlf+str(page+1))
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            all = soup.find("ul",{"class":"basic1"})
            all2 = all.find_all("li")
            
            #post-list를 찾아 all에 대입 후
            #all2에 배열 형태로 저장
          
            for item in all2:

                dict2 = {}
                d={}#사전 d
                linkNum = item.find("dt").find("a")["href"]
                date=item.find("dd",{"class":"txt_inline"}).text
                title=item.find("dt").text
                title=title[1:len(title)-1]
                    
                d["3link"]=linkNum
                d["2title"]=title
                d["1date"]=date
                d["4content"]=self.bringContent(linkNum)
                d["5comment"]=self.bringComment(linkNum)
                d["6commentNum"]=self.bringCommentNum(linkNum)
   #             d["7hitNum"]=self.bringHitNum(linkNum)
                
                self.comSum+=d["6commentNum"]
              #  self.hitSum+=d["7hitNum"]
                    
                l.append(d) #리스트에 사전 추가
                df=pd.DataFrame(l)
               
        dict2["commentSum"]=self.comSum
    #    dict2["hitSum"]=self.hitSum
        dict2["refSum"]=self.refSum
        
        l2.append(dict2)
        df2=pd.DataFrame(l2)
        
        return df,df2
    
    '''    #조회수가 사라져서 죄다 *로 나옵니다...
    def bringHitNum(self,oburl):
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"end_qbox"})
        if(all==None):
            #print(oburl)
            return '*'
        all2=all.find("div")
        all3=all2.find("div")
        all4=all3.find("div")
        all5=all4.find("dl")
    
        if(all5==None):
            #print(oburl)
            return '*'
        hN=all5.text.split("조회수")        
        final_hn=hN[1].split("\n")
        
        midHN=final_hn[0]
        #"," 예외처리
        if(len(midHN)>=4):
            NmidHN=midHN.split(",")
            Nfinal_hn=NmidHN[0]+NmidHN[1]
        else:
            Nfinal_hn=midHN
        return(int(Nfinal_hn))'''  