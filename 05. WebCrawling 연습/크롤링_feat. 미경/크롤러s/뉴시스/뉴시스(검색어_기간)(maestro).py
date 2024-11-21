#!/usr/bin/env python
# coding: utf-8

# In[7]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql


# In[8]:


# 1단계: 사이트 페이지 오픈
# url 로 모든 제어가 가능할때 사용하는 함수

def OpenNewsUrl(search,sdate,edate):   
    url = "https://newsis.com/search/?val={search}&sort=acc&jo=all_jogun&bun=all_bun&sdate={sdate}&term=direc&edate={edate}&s_yn=Y&catg=0&t=0&page=1&"
    url = url.format(search=search,sdate=sdate,edate=edate)

#     print(url)   # url 확인용
    
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get(url)
    time.sleep(2)
    
    ListNewsUrl(driver)


# In[9]:


# 2단계: 목록에서 페이지 이동하면서 url 가져오기

def ListNewsUrl(driver):
    url_temp = driver.current_url   # 현재 브라우저의 url 정보를 가져오는 명령어
    url_temp = url_temp.replace("&page=1","")   # url 에 page가 포함되어 있기에 이것을 제거
    for x in range(1,2+1,1):
        url = url_temp + "&page={pageNo}".format(pageNo=x)   # 여기 변수명과 위의 변수명은 같아야 함
        print("리스트: ",url)    # 목록페이지의 url 보는 용도
        driver.get(url)
        time.sleep(2)            # 2초 대기
        
        arrStrUrls =[]
        arrUrls = driver.find_elements_by_css_selector(".articleList2 li .tit a")   # 목록페이지에서 url list 가져오기 
        
#         print(len(arrUrls))
#         print(arrUrls[0])
        
        for i in arrUrls:
            arrStrUrls.append(i.get_attribute("href"))
            
#             print(i.text)
#             print(i.get_attribute("href"))
        
#         print("URL List Count:",len(arrStrUrls))       # url list가 몇개인지 확인
#         for i in arrStrUrls:                           # 배열의 url list 내용 보기 
#             print(i)
        
        NewsInfo(driver,arrStrUrls)


# In[10]:


# 3단계: 세부페이지에서 제목, 날짜, 내용 가져오기
def NewsInfo(driver,arrStrUrl):
    try:
        for strHref in arrStrUrl:
            driver.get(strHref)
            time.sleep(2)
            print(strHref)

            strNewsTitle =""
            arrNewsTitles = driver.find_elements_by_css_selector(".view .top .tit")
            strNewsTitle = arrNewsTitles[0]
            strNewsTitle = strNewsTitle.text
            print(strNewsTitle)        

            strNewsDate =""
            arrNewsDates = driver.find_elements_by_css_selector(".infoLine .left .txt")  # 날짜가 포함된 html element 가져오기
            strNewsDate = arrNewsDates[0].text               # 날짜가 있는 element 내용 보기 .text로 HTML태그 제거
            strNewsDate = strNewsDate.replace("등록 ","")    # 날짜 앞의 불필요한 글자 지우기
            strNewsDate = strNewsDate.replace(".","")[0:8]   # 8자리 YYYYMMDD 형태로 만들기
            print(strNewsDate)      

            strNewsSubtitle = ""
#             arrNewsSubtitles = driver.find_elements_by_css_selector(".scroller-wrap01 .story-news .tit-sub ")
#             if(len(arrNewsSubtitles) != 0):
#                 strNewsSubtitle = arrNewsSubtitles[0].text
#             print(strNewsSubtitle)    

            strNewsContent = ""
            arrNewsContents = driver.find_elements_by_css_selector(".viewer article ")
            for i in arrNewsContents:
                strNewsContent = strNewsContent + i.text        
            print(strNewsContent)

#            4단계 DB에 데이터를 넣을때 사용
            dbData = [[strHref,strNewsDate,strNewsTitle,strNewsSubtitle,strNewsContent]]
            connectDB(dbData)
            
    except:
        print('페이지 오류:',strHref)
        pass


# In[11]:


def connectDB(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    DB_NAME = 'news'
    
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    curs = conn.cursor()
    sql = """insert into yhnews(url,newsDate,newsTitle,newsSubtitle,contents) values (%s, %s, %s, %s, %s)"""
    curs.executemany(sql,dbData)
    conn.commit()

    conn.close()


# In[12]:


search = "요소수"  # 검색어
sdate = "20210701"
edate = "20211101"
OpenNewsUrl(search,sdate,edate)   


# In[ ]:




