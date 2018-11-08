import konlpy
import csv
import sys
from pandas import DataFrame
import pandas as pd
from konlpy.tag import Kkma

def split(text):
    kkma = Kkma()
    List=kkma.sentences(text)
    return List

def getCsv(input_file,titleList,contentList,commentList):
    f=open(input_file+'.csv','r',encoding='utf-8')
    csvReader=csv.reader(f)
    for i in csvReader:
        titleList.append(i[1])
        contentList.append(i[3])
        commentList.append(i[5])
    f.close()

def sliceSentence(input_file):
    index=0
    titleList=[]
    contentList=[]
    commentList=[]
    AllList=[]
    getCsv(input_file, titleList,contentList,commentList)
    print(len(contentList))
    for index in range(1,len(contentList)):
        AllList.extend(split(titleList[index]))
        AllList.extend(split(contentList[index]))
        AllList.extend(split(commentList[index]))
        index+=1
        print('Loading')
    return AllList

'''
l=[]
input_file = 'Sentence_test'
#2016_수능특강_국어_화작문_orbi
output_file = input_file+'_sliced'
#긍부정_2016_수능특강_국어_화작문_orbi
df=pd.DataFrame({'sentence':sliceSentence(input_file)})
df.to_csv(output_file+'.csv', encoding='utf-8-sig', index=False)
'''