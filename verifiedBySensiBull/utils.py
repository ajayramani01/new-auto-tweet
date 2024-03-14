
from selenium import webdriver
# from PIL import Image
from bs4 import BeautifulSoup
import time
from .models import verifiedUser
import datetime
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd
from core.settings import X_USER_ID,X_PASSWD,X2FA,CREDS

from auto_tweet.models import tweet_history
from auto_tweet.tweet_script import tweet_with_image_with_login
import subprocess
import pyotp
import logging
logger = logging.getLogger(__name__)
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

def provide_2FA():
    totp = pyotp.TOTP(X2FA)
    return totp.now()

def login_twitter(driver):
    username_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
    next_button_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'
    password_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
    twofa_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
    verification_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div'
    time.sleep(5)
    # time.sleep(50) #Additonal time for slow internet connection
    driver.find_element(By.XPATH,username_xpath).send_keys(X_USER_ID)
    time.sleep(2)
    driver.find_element(By.XPATH,next_button_xpath).click()
    time.sleep(2)
    # time.sleep(50) #Additonal time for slow internet connection

    driver.find_element(By.XPATH,password_xpath).send_keys(X_PASSWD)
    time.sleep(2)
    driver.find_element(By.XPATH,login_xpath).click()
    time.sleep(4)
    # time.sleep(50) #Additonal time for slow internet connection
    verification_passwd=provide_2FA()
    driver.find_element(By.XPATH,twofa_xpath).send_keys(verification_passwd)
    time.sleep(2)
    driver.find_element(By.XPATH,verification_xpath).click()
    # time.sleep(50) #Additonal time for slow internet connection
    # print("Login Success!")



    


def opendriver(todays_date=datetime.datetime.today().date()):
    driver = webdriver.Chrome(options=options)
    # todays_date=datetime.datetime(2024,2,5).date()
    if isinstance(todays_date, str):
        todays_date=(datetime.datetime.strptime(todays_date,'%Y-%m-%d')).date()
    msg="Checking data for "+str(todays_date)
    logger.info(msg)

    driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
    try:
        login_twitter(driver)
        time.sleep(20)
    except:
        logger.info("Login Failed!")
        return 1
    
    scroll_pause_time = 5 #increase if scraping fails due to slow internet
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    # print("Scrolling page")
    list_a=[]
    prevs_found=0
    
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        soup = BeautifulSoup(driver.page_source, "html.parser")
        verified_a= soup.find_all("a", {"aria-label": "verified.sensibull.com See Verified Profit and Loss on Sensibull"})
        list_a.extend(verified_a)
        if list_a:
            data_exist=verifiedUser.objects.filter(verification_url=list_a[-1]['href'])
        else:
            continue
        if data_exist:
            # print('User data already exist')
            new_data=data_exist[0]
        else:
            new_data=getUserData(list_a[-1]['href'])
        if new_data:
            check_date=new_data.date.date()
            if check_date==todays_date:
                # print("Its Today's data",check_date)
                pass
            else:
                # print(check_date, todays_date)
                # print("Got previous day data!",prevs_found)
                prevs_found+=1
                if prevs_found>6:
                    break
        if (screen_height) * i > scroll_height:
            break 
    
    verified_a= set(list_a)
    for a in verified_a:
        data_exist=verifiedUser.objects.filter(verification_url=a['href'])
        if data_exist:
            # print('User data already exist')
            pass
        else:
            getUserData(a['href'])
    
    list_of_traders=generateWinnerLoser(todays_date)
    list_of_winlose=[]
    for i in list_of_traders:
        list_of_winlose.append(verifiedUser.objects.get(id=i))
    list_of_traders=[i.x_username for i in list_of_winlose]
    logger.info(list_of_traders)    
    
    tweet_headline='Traders Closed Positively Today: '+str(", ".join(list_of_traders[0:5]))+'. Traders Closed Negatively Today: '+str(", ".join(list_of_traders[5:]))
    # print(len(tweet_headline))
    todays_date=todays_date.strftime('%Y-%m-%d')
    generateimageWinLos(todays_date,tweet_headline)
    

        
def getUserData(url):
    # url='https://t.co/fpcX7JwDXA'
    driver2 = webdriver.Chrome(options=options)
    # tz_params = {'timezoneId': 'Asia/Kolkata'}
    # driver2.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
    driver2.get(url)
    time.sleep(5)
    logger.info(url)
    soup = BeautifulSoup(driver2.page_source, "html.parser")
    name= soup.find_all("div", {"class": "twitter-profile-name"})
    X_user= soup.find_all("span", {"class": "style__MutedText-sc-1a2uzpb-8 iylEpU"})
    date= soup.find_all("div", {"class": "taken-timestamp"})
    try:
        name=name[0].text
        X_user=X_user[0].text
    except:
        # print('Retrying!')
        return getUserData(url)
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
    try:
        date=str(date[0].text).split(' @ ')[1]
    except:
        # print('User deleted data')
        return None
    try:
        date=datetime.datetime.strptime(date,'%d %b %Y, %I:%M %p')
    except:
        logger.info("Fetching Failed" + url)
        logger.info(date)
    try:
        new_data=verifiedUser.objects.create(
        verification_url=url,
        name=name,
        x_username=X_user,
        totalPL=totalPL,
        ROI=ROI,
        total_capital=total_capital,
        date=date
        )
        return new_data
    except:
        logger.info('Save Failed'+url)
        return None
    

def generateWinnerLoser(provided_date):

    df = pd.DataFrame(list(verifiedUser.objects.all().values()))
  
    df["date"] = df['date'].map(lambda date: date.date())
    df = df[df.date == provided_date]
    df = df[df.totalPL != '']

    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace(',',''))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('L','*10e5'))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('Cr','*10e7'))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: eval(totalPL))
    df=df.sort_values('totalPL')

    Losers=list(df.head()["id"])
    Winners=list(df.tail()['id'])[::-1]

    return Winners+Losers


def generateimageWinLos(date,tweet=['Todays data:']):
    obj = tweet_history.objects.create(tweet=tweet)
    img_output='/home/alkatraz019/Desktop/AplusTopper/AutoTweet/media/tweet/'+str(obj.id)+'.png'
    img_input='http://127.0.0.1:5000/image-gen/'+date+'/'

    subprocess.run(["wkhtmltoimage", "--width", "1200", "--height", "1200", img_input, img_output])
    time.sleep(10)
    obj.tweet_img = 'tweet/'+str(obj.id)+'.png'
    obj.save()

    all_creds=CREDS.split(',,')
    for i in all_creds:
        creds=i.split(',')
        logger.info(creds[1])
        tweet_with_image_with_login(creds[0],creds[1],creds[2],creds[3],creds[4],obj.tweet,obj.tweet_img.url)
        time.sleep(1)



