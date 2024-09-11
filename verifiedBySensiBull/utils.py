
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
from progress.bar import Bar

import pandas as pd
from core.settings import X_USER_ID,X_PASSWD,X2FA,X_USER_ID1,X_PASSWD1,X2FA1,X_USER_ID2,X_PASSWD2,X2FA2 ,CREDS

from auto_tweet.models import tweet_history
from auto_tweet.tweet_script import tweet_with_image_with_login
import subprocess
import pyotp
import logging
logger = logging.getLogger(__name__)
EXTRA_TIME=0
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")

def provide_2FA(x2f):
    totp = pyotp.TOTP(x2f)
    return totp.now()

def login_twitter(driver,user,id,x2f):
    username_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
    next_button_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div'
    password_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
    login_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button'
    twofa_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
    verification_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button'
    time.sleep(5)
    time.sleep(EXTRA_TIME) #Additonal time for slow internet connection
    driver.find_element(By.XPATH,username_xpath).send_keys(user)
    time.sleep(2)
    driver.find_element(By.XPATH,next_button_xpath).click()
    time.sleep(2)
    time.sleep(EXTRA_TIME) #Additonal time for slow internet connection

    driver.find_element(By.XPATH,password_xpath).send_keys(id)
    time.sleep(2)
    driver.find_element(By.XPATH,login_xpath).click()
    time.sleep(4)
    time.sleep(EXTRA_TIME) #Additonal time for slow internet connection
    verification_passwd=provide_2FA(x2f)
    driver.find_element(By.XPATH,twofa_xpath).send_keys(verification_passwd)
    time.sleep(2)
    driver.find_element(By.XPATH,verification_xpath).click()
    time.sleep(EXTRA_TIME) #Additonal time for slow internet connection
    # print("Login Success!")



    


def opendriver(todays_date=datetime.datetime.today().date()):
    driver = webdriver.Chrome(options=options)
    driver2 = webdriver.Chrome(options=options)
    driver2.set_window_size(3000,2000)
    # todays_date=datetime.datetime(2024,8,4).date()
    if isinstance(todays_date, str):
        todays_date=(datetime.datetime.strptime(todays_date,'%Y-%m-%d')).date()
    msg="Checking data for "+str(todays_date)
    logger.info(msg)
    driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
    try:
        login_twitter(driver,X_USER_ID,X_PASSWD,X2FA)
        time.sleep(20+EXTRA_TIME)
    except:
        logger.info("Login Failed @alkatraz!")
        # try:
        driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
        login_twitter(driver,X_USER_ID1,X_PASSWD1,X2FA1)
        time.sleep(20+EXTRA_TIME)
        # except:
        #     logger.info("Login Failed @IntraDayGurus!")
        #     try:
        #         driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
        #         login_twitter(driver,X_USER_ID2,X_PASSWD2,X2FA2)
        #         time.sleep(20+EXTRA_TIME)
        #     except:
        #         logger.info("Login Failed @IntraTraderHub!")
        #         return -1
            
    
    scroll_pause_time = 5+EXTRA_TIME#increase if scraping fails due to slow internet
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
            new_data=getUserData(driver2,list_a[-1]['href'])
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
    with Bar('Progress',max=len(verified_a),fill='#',suffix='%(percent).1f%% - %(eta)ds') as bar:
        for a in verified_a:
            data_exist=verifiedUser.objects.filter(verification_url=a['href'])
            if data_exist:
                # print('User data already exist')
                pass
            else:
                getUserData(driver2,a['href'])
            bar.next()
            print()
    
    list_of_traders=generateWinnerLoser(todays_date)
    list_of_winlose=[]
    for i in list_of_traders:
        list_of_winlose.append(verifiedUser.objects.get(id=i))
    list_of_traders=[i.x_username for i in list_of_winlose]
    logger.info(list_of_traders)    
    
    tweet_headline='Traders Closed Positively Today: '+str(", ".join(list_of_traders[0:5]))+'. Traders Closed Negatively Today: '+str(", ".join(list_of_traders[5:]))
    print(tweet_headline)
    todays_date=todays_date.strftime('%Y-%m-%d')
    generateimageWinLos(todays_date,tweet_headline)
    

        
def getUserData(driver2,url,retry=0):
    # url='https://t.co/fpcX7JwDXA'
    
    # tz_params = {'timezoneId': 'Asia/Kolkata'}
    # driver2.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
    driver2.get(url)
    time.sleep(5)
    time.sleep(EXTRA_TIME)
    logger.info(url)
    soup = BeautifulSoup(driver2.page_source, "html.parser")
    name= soup.find_all("div", {"class": "twitter-profile-name"})
    date= soup.find_all("div", {"class": "taken-timestamp"})
    try:
        selector=name[0].find_next_sibling("span")
        name=name[0].text
        X_user=selector.text
        logger.info(name +' '+ X_user)
    except:
        # print('Retrying!')
        if retry > 3:
            
            logger.info("Max retries " + url)
            return None
        return getUserData(driver2,url,retry+1)
    pnl_section= soup.find_all("div", {"class" : "section-pnl-details"})
    try:
        selector=pnl_section[0].contents
        selector=selector[0].find_next_sibling("div")
        totalPL=selector.text
    except:
        totalPL=''
    try:
        selector=pnl_section[1].contents
        selector=selector[0].find_next_sibling("div")
        ROI=selector.text
    except:
        ROI=''
    try:
        selector=pnl_section[2].contents
        selector=selector[0].find_next_sibling("div")
        total_capital=selector.text
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
        logger.info(totalPL+' '+ROI+' '+total_capital)
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
    print(len(df))
  
    df["date"] = df['date'].map(lambda date: date.date())
    df = df[df.date == provided_date]
    print(len(df))
    df = df[df.totalPL != '']
    print(len(df))

    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace(',',''))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('L','*10e5'))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: totalPL.replace('Cr','*10e7'))
    df["totalPL"] = df['totalPL'].map(lambda totalPL: eval(totalPL))
    df=df.sort_values('totalPL')
    print(len(df))
    Losers=list(df.head()["id"])
    Winners=list(df.tail()['id'])[::-1]
    print(Losers)
    print(Winners)

    return Winners+Losers

import os

def generateimageWinLos(date,tweet=['Todays data:']):
    print("Image 1")
    obj = tweet_history.objects.create(tweet=tweet)
    print("Image 2")
    # img_output='/home/alkatraz019/Desktop/AplusTopper/AutoTweet/media/tweet/'+str(obj.id)+'.png'
    output_dir = 'C:/Users/ajayt/Desktop/Aplus Topper/New Task/AutoTweet__/AutoTweet/media/tweet'
    img_output = os.path.join(output_dir, str(obj.id) + '.png')
    img_input='http://127.0.0.1:5000/image-gen/'+date+'/'
    print("Image 3")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        result = subprocess.run(
            ["wkhtmltoimage", "--width", "1200", "--height", "1200", img_input, img_output],
            capture_output=True, text=True, check=True
        )
        print("Command output:", result.stdout)
        print("Command error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error executing wkhtmltoimage:", e)
    print("Image 4")
    time.sleep(10)
    print("Image 5")
    obj.tweet_img = 'tweet/'+str(obj.id)+'.png'
    print("Image 6")
    obj.save()
    print("Image 7")

    all_creds=CREDS.split(',,')
    for i in all_creds:
        creds=i.split(',')
        logger.info(creds[1])
        tweet_with_image_with_login(creds[0],creds[1],creds[2],creds[3],creds[4],obj.tweet,obj.tweet_img.url)
        time.sleep(1)



def helper(todays_date=datetime.datetime.today().date()):
    driver = webdriver.Chrome(options=options)
    driver2 = webdriver.Chrome(options=options)
    driver2.set_window_size(3000,2000)
    if isinstance(todays_date, str):
        todays_date=(datetime.datetime.strptime(todays_date,'%Y-%m-%d')).date()
    msg="Checking data for "+str(todays_date)
    logger.info(msg)

    driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
    try:
        login_twitter(driver,X_USER_ID,X_PASSWD,X2FA)
        time.sleep(20+EXTRA_TIME)
    except:
        logger.info("Login Failed @alkatraz!")
        driver.get('https://twitter.com/search?q=%23VerifiedBySensibull&f=live')
        login_twitter(driver,X_USER_ID1,X_PASSWD1,X2FA1)
        time.sleep(20+EXTRA_TIME)

    scroll_pause_time = 5+EXTRA_TIME
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
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
            new_data=data_exist[0]
        else:
            new_data=getUserData(driver2,list_a[-1]['href'])
        if new_data:
            check_date=new_data.date.date()
            if check_date==todays_date:
                pass
            else:
                prevs_found+=1
                if prevs_found>6:
                    break
        if (screen_height) * i > scroll_height:
            break 
    
    verified_a= set(list_a)
    with Bar('Progress',max=len(verified_a),fill='#',suffix='%(percent).1f%% - %(eta)ds') as bar:
        for a in verified_a:
            data_exist=verifiedUser.objects.filter(verification_url=a['href'])
            if data_exist:
                # print('User data already exist')
                pass
            else:
                getUserData(driver2,a['href'])
            bar.next()
            print()

def web_scrap(pl='pl_desc',flag=False):
    driver = webdriver.Chrome(options=options)
    driver1 = webdriver.Chrome(options=options)
    # driver2 = webdriver.Chrome(options=options) 
    driver1.set_window_size(3000,2000)
    url = 'https://web.sensibull.com/verified-pnl/hall-of-fame?page=1&sort_by=' + pl + '&category=live_positions'
    driver1.get(url)
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    div = soup.find('div', {'role': 'tabpanel', 'id': 'tabpanel-live_positions'})
    a_tags = div.find_all('a')
    verification_urls = []
    for i in range(0,len(a_tags),2):
        a = a_tags[i]
        href = ("https://web.sensibull.com" + a.get('href'))
        verification_urls.append(href)
    print("VERIFICATION DONE")
    soup = BeautifulSoup(driver1.page_source, "html.parser")
    table = soup.find_all('table')
    table_rows = soup.find_all('tr')
    results = []
    list_of_traders = []
    for i in range(1,len(table_rows)):
        row = table_rows[i]
        td_tags = row.find_all('td')
        text = td_tags[0].get_text(strip=True)
        cleaned_text = text[4:-6].strip()
        name_username = cleaned_text.split('@')
        x_username = '@' + name_username[1]
        x_user_photo = "https://twitter.com/"+ name_username[1] + "/photo" 
        save_image_from_url(x_user_photo,name_username[1])
        verification_url = verification_urls[i-1]
        totalPL = td_tags[2].get_text(strip=True)
        ROI = td_tags[4].get_text(strip=True)
        total_capital = td_tags[3].get_text(strip=True)
        list_of_traders.append(x_username)
        results.append({
            'name': name_username[0],
            'saved_image':name_username[1],
            'x_username': x_username,
            'x_user_photo': x_user_photo,
            'verification_url': verification_url,
            'totalPL': totalPL,
            'ROI': ROI,
            'total_capital': total_capital
        })
        # print(name," ",x_username)
        # print("P&L ",totalPL)
        # print("ROI ",ROI)
        # print("CAPITAL ",total_capital)
        # print(verification_url)
        # print(x_user_photo)
    print("WEB SCRAPING DONE")
    driver.quit()
    driver1.quit()
    if flag:
        if pl == 'pl_desc':
            tweet_headline='Traders Closed Positively Today: '+str(", ".join(list_of_traders))
        else:
            tweet_headline='Traders Closed Negatively Today: '+str(", ".join(list_of_traders))
        todays_date=datetime.datetime.today().date()
        todays_date=todays_date.strftime('%Y-%m-%d')
        new_tweet(todays_date,tweet_headline,pl)
        return
    return results

def new_tweet(date,tweet,pl):
    obj = tweet_history.objects.create(tweet=tweet)
    # img_output='/home/alkatraz019/Desktop/AplusTopper/AutoTweet/media/tweet/'+str(obj.id)+'.png'
    output_dir = 'C:/Users/ajayt/Desktop/Aplus Topper/New Task/AutoTweet__/AutoTweet/media/tweet'
    img_output = os.path.join(output_dir, str(obj.id) + '.png')
    if pl == 'pl_desc':
        img_input='http://127.0.0.1:5000/leaderboard-profit/'
    else:
        img_input='http://127.0.0.1:5000/leaderboard-loss/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        result = subprocess.run(
            ["wkhtmltoimage", "--width", "1200", "--height", "1200", img_input, img_output],
            capture_output=True, text=True, check=True
        )
        print("Command output:", result.stdout)
        print("Command error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error executing wkhtmltoimage:", e)
    time.sleep(10)
    obj.tweet_img = 'tweet/'+str(obj.id)+'.png'
    obj.save()
    all_creds=CREDS.split(',,')
    for i in all_creds:
        creds=i.split(',')
        logger.info(creds[1])
        tweet_with_image_with_login(creds[0],creds[1],creds[2],creds[3],creds[4],obj.tweet,obj.tweet_img.url)
        time.sleep(1)


import requests
def save_image_from_url(url,username) -> None:
    output_dir = 'C:/Users/ajayt/Desktop/Aplus Topper/New Task/AutoTweet__/AutoTweet/verifiedBySensiBull/static/images'
    current_date = datetime.datetime.now().strftime('%Y-%m-%d') 
    img_filename = f"{username}.jpg"
    img_path = os.path.join(output_dir, img_filename)
    if os.path.exists(img_path):
        print(f'Image already exists')
        return
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)
        img_element = driver.find_element(By.TAG_NAME, 'img')
        img_url = img_element.get_attribute('src')
        if not img_url:
            print('No image URL found.')
            return
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f'Image saved as {img_path}')
    finally:
        driver.quit()