import requests

def requestHtml():
	bookName="수학 문제집"
	r=requests.get("https://kin.naver.com/search/list.nhn?query=”+bookName)
	source=r.text
	print(source)

requestHtml()

