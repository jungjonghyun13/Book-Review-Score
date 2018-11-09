import requests, operator, glob2
from pandas import DataFrame
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from functools import reduce
from math import ceil

# coding: utf-8

# In[ ]:

class nonRV:        
    def __init__(self,s1,s2,s3,d1,d2) :
        #교재,과목, 시작날짜, 끝날짜
        self.n_s1 =s1
        self.n_s2 =s2
        self.n_s3 =s3
        self.n_d1 =d1
        self.n_d2 =d2
        
        #댓글수,조회수,언급수 총합 
        self.comSum=0 
        self.hitSum=0 
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
        return(int(Nfinal_hn))
    
    def bringContent(self,oburl):
        return_list=""
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"end_qbox"})
        if (all!=None):
            all2=all.find("div",{"id":"qna_detail_question"})
            if(all2==None):
                all2=all.find("div",{"class":"end_question"})
                all3=all2.find("div",{"class":"end_content _endContents"})
                all4=all3.find("div",{"class":"_endContentsText"})
                all5=all4.find_all("p")
                for item in all5:
                    return_list+=item.text
            else:
                all3=all2.find("div")
                all4=all3.find("div",{"id":"contents_layer_0"})
                all5=all4.find("div")
                all6=all5.find("div",{"class":"_endContentsText"})
                all7=all6.find_all("p")
                all8=""
                if all7==[]:
                    all8=all6.text
                for item in all7:
                    return_list+=item.text
                for item in all8:
                    return_list+=item
        return return_list
    
    def bringComment(self,oburl):
        return_list=""
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"class":"end_abox"})
        if (all!=None):
            all2=all.find("div")
            all3=all2.find("div")
            all4=all3.find("div",{"class":"_contentsLayer"})
            all5=all4.find("div")
            all6=all5.find("div",{"class":"_endContentsText"}).text
            all4_2=[]
            all5_2=[]
            all6_2=[]
            all2_2=all.find("div",{"id":"qna_detail_answerList_normal"})
            all3_2=all2_2.find_all("div")
            for item in all3_2:
                if(item!=None):
                    all4_2.append(item.find("div",{"class":"_contentsLayer"}))
            for item in all4_2:
                if(item!=None):
                    all5_2.append(item.find("div",{"class":"end_content _endContents"}))
            for item in all5_2:
                if(item!=None):
                    all6_2.append(item.find("div").text)
            
            for item in all6:
                if(item!=None):
                    return_list+=item
                
            for item in all6_2:
                if(item!=None):
                    return_list+=item              
        return return_list
    
    def bringCommentNum(self,oburl):
        r=requests.get(oburl)
        c=r.content
        soup = BeautifulSoup(c, "html.parser")
        all=soup.find("div",{"id":"wrap"})
        all2=all.find("div",{"id":"container"})
        all3=all2.find("div",{"id":"content"})
        all4=all3.find("div",{"id":"sortOptions"})
        all5=all4.find("p",{"class":"re_num"})
        all6=all5.find("span")
        cNum=all6.text.split("개")
        midcNum=cNum[0]
        if(len(midcNum)>=4):
            NmidcNum=midcNum.split(",")
            Nfinal_cNum=NmidcNum[0]+NmidcNum[1]
        else:
            Nfinal_cNum=midcNum
        return int(Nfinal_cNum)

    def crawlingData(self,s1,s2,s3,d1,d2):
        self.n_s1 = s1
        self.n_s2 = s2
        self.n_s3 = s3
        self.n_d1 = d1
        self.n_d2 = d2

        l=[]#리스트
        l2=[]#총합 저장할 리스트
        #urlf="https: //kin.naver.com/search/list.nhn?sort=date&query="+self.n_s1+"%20%26quot%3B"+self.n_s2+"%26quot%3B&period="+self.n_d1+"%7C"+self.n_d2+"&section=kin&page="
        urlf= "https://kin.naver.com/search/list.nhn?sort=date&query="+self.n_s1+"%20%26quot%3B"+self.n_s2+"%26quot%3B+-%26quot%3B"+self.n_s3+"&period="+self.n_d1+"%7C"+self.n_d2+"&section=kin&page="
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
                if(self.bringHitNum(linkNum)!='*'):
                    title=item.find("dt").text
                    title=title[1:len(title)-1]
                    
                    d["link"]=linkNum
                    d["title"]=title
                    d["date"]=date
                    d["content"]=self.bringContent(linkNum)
                    d["comment"]=self.bringComment(linkNum)
                    d["commentNum"]=self.bringCommentNum(linkNum)
                    d["hitNum"]=self.bringHitNum(linkNum)
                    
                    self.comSum+=d["commentNum"]
                    self.hitSum+=d["hitNum"]
                    
                    l.append(d) #리스트에 사전 추가
                df=pd.DataFrame(l)
               
        dict2["commentSum"]=self.comSum
        dict2["hitSum"]=self.hitSum
        dict2["refSum"]=self.refSum
        
        l2.append(dict2)
        df2=pd.DataFrame(l2)
        
        return df,df2

    def dftoCSV(self,obdf,obdf2,s1,s2,s3,d1,d2):
        obdf.to_csv('논리뷰_ '+s1+'_'+s2+'-'+s3+'_'+d1+' ~ '+d2+'.csv', encoding='utf-8-sig', index=False)
        print("------파일생성------")
        
        obdf2.to_csv('논리뷰_조댓언_'+s1+'_'+s2+'-'+s3+'_'+d1+' ~ '+d2+'총합.csv', encoding='utf-8-sig', index=False)
        print("------총합 파일 생성------")