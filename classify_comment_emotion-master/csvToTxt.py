import csv

def getCsv(titleList,contentList,commentList):
    file_name='testreview'
    f=open(file_name+'.csv','r',encoding='utf-8')
    csvReader=csv.reader(f)
    for i in csvReader:
        titleList.append(i[0])
        contentList.append(i[1])
        commentList.append(i[2])
    f.close()

def main():
    titleList=[]
    contentList=[]
    commentList=[]
    file_name='testreview'
    getCsv(titleList,contentList,commentList)
   
    f=open(file_name+'.txt','w',encoding='utf-8')
    for i in range(len(titleList)):
        f.write(titleList[i]+'\t')
        f.write(contentList[i]+'\t')
        f.write(commentList[i]+'\t\n')

    f.close()
    
main()
