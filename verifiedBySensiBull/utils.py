
from selenium import webdriver
# from PIL import Image
from bs4 import BeautifulSoup
import time
from .models import verifiedUser
import datetime
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.settings import X_USER_ID,X_PASSWD
def login_twitter(driver):
    username_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
    next_button_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'
    password_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
    time.sleep(5)
    driver.find_element(By.XPATH,username_xpath).send_keys(X_USER_ID)
    time.sleep(2)
    driver.find_element(By.XPATH,next_button_xpath).click()
    time.sleep(2)
    driver.find_element(By.XPATH,password_xpath).send_keys(X_PASSWD)
    time.sleep(2)
    driver.find_element(By.XPATH,login_xpath).click()

    


def opendriver():
    driver = webdriver.Chrome()
    
    driver.get('https://twitter.com/search?q=%23verifiedbysensibull')
    login_twitter(driver)
    time.sleep(20)

    scroll_pause_time = 2
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("Scrolling page")
    while i<10:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    verified_a= soup.find_all("a", {"aria-label": "verified.sensibull.com See Verified Profit and Loss on Sensibull"})
    for a in verified_a:
        getUserData(a['href'])

        

    



def getUserData(url):
    # url='https://t.co/fpcX7JwDXA'
    driver2 = webdriver.Chrome()
    driver2.get(url)
    time.sleep(5)
    print(url)
    soup = BeautifulSoup(driver2.page_source, "html.parser")
    name= soup.find_all("div", {"class": "twitter-profile-name"})
    X_user= soup.find_all("span", {"class": "style__MutedText-sc-1a2uzpb-8 iylEpU"})
    date= soup.find_all("div", {"class": "taken-timestamp"})
    

    

    





    name=name[0].text
    X_user=X_user[0].text
    try:
        selector=soup.select('#app > div > div.style__AppWrapper-sc-8vyh1s-0.FmsnX.sn-page--positions-screenshot.page-sidebar-is-open > div.style__AppContent-sc-8vyh1s-1.fcFrhL.sn-l__app-content > div.style__ContainerSpacing-sc-8vyh1s-2.kwNiQk > div > div:nth-child(1) > div.style__ScreenshotStatsSummaryWrapperSm-sc-1a2uzpb-7.dA-drzz > div > div.section-pnl-group > div > div > div')
        totalPL=selector[0].text
    except:
        totalPL=''
    try:
        selector=soup.select('#app > div > div.style__AppWrapper-sc-8vyh1s-0.FmsnX.sn-page--positions-screenshot.page-sidebar-is-open > div.style__AppContent-sc-8vyh1s-1.fcFrhL.sn-l__app-content > div.style__ContainerSpacing-sc-8vyh1s-2.kwNiQk > div > div:nth-child(1) > div.style__ScreenshotStatsSummaryWrapperSm-sc-1a2uzpb-7.dA-drzz > div > div.section-pnl-group > div:nth-child(2) > div > div')
        ROI=selector[0].text
    except:
        ROI=''
    try:
        selector=soup.select('#app > div > div.style__AppWrapper-sc-8vyh1s-0.FmsnX.sn-page--positions-screenshot.page-sidebar-is-open > div.style__AppContent-sc-8vyh1s-1.fcFrhL.sn-l__app-content > div.style__ContainerSpacing-sc-8vyh1s-2.kwNiQk > div > div:nth-child(1) > div.style__ScreenshotStatsSummaryWrapperSm-sc-1a2uzpb-7.dA-drzz > div > div.section-pnl-group > div:nth-child(3) > div > div')
        total_capital=selector[0].text
    except:
        total_capital=''
    date=str(date[0].text).split(' @ ')[1]
    try:
        date=datetime.datetime.strptime(date,'%d %b %Y, %I:%M %p')
    except:
        print("Fetching Failed")
        print(date)
    try:
        verifiedUser.objects.create(
        verification_url=url,
        name=name,
        x_username=X_user,
        totalPL=totalPL,
        ROI=ROI,
        total_capital=total_capital,
        date=date
        )
    except:
        print('User Data Exists')
    
    

