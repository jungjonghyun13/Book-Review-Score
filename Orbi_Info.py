
# coding: utf-8
# In[ ]:
import requests, operator, glob2
from pandas import DataFrame
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

class Orbi:
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
          
    def get_tags(self,soup):
        try:
            tags = soup.find("div",{"class":"content-body"}).find("div",{"class":"tag-wrap"}).text.replace("\n"," ")
        except:
            tags="None"
        return tags

    def periodSetting(self,sDate, eDate, all2):
        ldate=all2[-1].find("p",{"class":"date"}).find("abbr")["title"]
        fdate=all2[0].find("p",{"class":"date"}).find("abbr")["title"]
        modify_lastDate = ldate[11:21]
        modify_firstDate = fdate[11:21]
        mfDate=parse(modify_firstDate)
        mlDate=parse(modify_lastDate)
        if (mfDate > eDate and mlDate > eDate):
            found=False
        else:
            found=True
        return found


    def get_comment(self,soup):
        comments_all=""
        try:
            comments = soup.find("div",{"class":"content-body"}).find("div",{"class":"comment-wrap"}).find_all("div",{"class":"comment-content"})
            for c in comments:
                comments_all+=c.text.replace("\n"," ").replace("\t"," ")
                if c.text =='':
                    comments_all="None"
        except:
            comments_all="None"
        return comments_all

    def get_hits(self,soup):
        try:
            hits = soup.find("div",{"class":"author-wrap"}).find("dl").find_all("dt")
            hits_num=hits[1].text[4:]
        except:
            hits_num=0
        return hits_num
   
    def linkOpen(self,linkNum, d):
        r = requests.get("https://orbi.kr/"+linkNum)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        tags=self.get_tags(soup)
        comments=self.get_comment(soup)
        hits_num=self.get_hits(soup)
        
        d['8tags']=tags
        d['5comments']=comments
        d['7hits_num']=hits_num
       
        try:
            content = soup.find("div",{"class":"content-wrap"}).text.replace("&nbsp","").replace("\n"," ").replace("\t"," ")
        except:
            content="None"
        return content, comments, tags, hits_num

    def find(self,subjectName, title, content, comments, tags):
        all=title+content+comments+tags
        if self.subjectName in all:
            return True
        else:
            return False
        
    def crawlingData(self,bookName, subjectName, startDate, endDate):
        self.bookName =bookName
        self.subjectName =subjectName
        self.startDate =startDate
        self.endDate =endDate
        
        global mod_year
        max_page=1000
        l=[]#리스트
        l2=[]#총합 저장할 리스트
        sDate=parse(self.startDate)
        eDate=parse(self.endDate)
        
        for page in range(max_page):
            r = requests.get("https://orbi.kr/search?q="+self.bookName+"&type=keyword&page="+str(page+1))
            c = r.content
            soup = BeautifulSoup(c, "html.parser")

            all = soup.find("ul", {"class": "post-list"})
            all2 = all.find_all("li")
       #post-list를 찾아 all에 대입 후
       #all2에 배열 형태로 저장
            if self.periodSetting(sDate, eDate, all2) is False:
                page+=1
                continue
                
            nagaja = True
            for item in all2:
                d={}
                dict2={}#총합 저장할 사전
                linkNum = item.find("p", {"class": "title"}).find("a")["href"]
                modify_linkNum=linkNum[1:12]
    
                date=item.find("p",{"class":"date"}).find("abbr")["title"]
                modify_date = date[11:21]
                mDate=parse(modify_date)
                if mDate > eDate:
                    continue
                if mDate >= sDate and mDate <= eDate:
                    title=item.find("p",{"class":"title"}).find("a").text

                    comments_num=item.find("p", {"class": "title"}).find("span",{"class":"comment-count"}).text
                
                    content,comments,tags,hits_num = self.linkOpen(modify_linkNum, d)
                    if self.find(self.subjectName, title, content, comments, tags) is False:
                        continue
                   
                    d["7hits_num"]=int(hits_num)
                    d["6comments_num"]=int(comments_num)
                    d["4content"]=content
                    d["3link"]='https://orbi.kr/' + modify_linkNum
                    d["2title"]=title
                    d["1date"]=modify_date
                    
                    self.refSum+=1
                    self.comSum+=d["6comments_num"]
                    self.hitSum+=d["7hits_num"]         
               
                    l.append(d) #리스트에 사전 추가
                else:
                    df=pd.DataFrame(l)
                    nagaja = False
                    break
                    
            #이중 for문 탈출
            if(nagaja == False):
                break
                
            df=pd.DataFrame(l)
        
        dict2["commentSum"]=self.comSum
        dict2["hitSum"]=self.hitSum
        dict2["refSum"]=self.refSum
        
        l2.append(dict2)
        df2=pd.DataFrame(l2)
        
        return df,df2