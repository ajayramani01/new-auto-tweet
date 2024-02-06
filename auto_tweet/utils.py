from .models import tweet_history,xlsxFiles
import pandas as pd
import numpy as np
from .tweet_script import tweet_with_image
import subprocess
import time
def return_json_of_xlsx(xlsx):


    FILE_PATH=xlsx.xlsx.url
    SHEET_INDEX = 0
    records = pd.read_excel(FILE_PATH[1:],index_col=False)

    records=records.replace(np.nan, '')
    # print(records)
    
    records.style.map("font-weight: bold")
    # print(records)

    blankIndex=[''] * len(records)
    records.index=blankIndex
    # print(records)
    # dfi.export(records, 'media/tweet/'+str(obj.id)+'.png')
    records.rename(columns={'BANK NIFTY':'BANK_NIFTY','Sell Below':'Sell_Below','Buy Above':'Buy_Above'},inplace=True)
    record1=records.iloc[0:4]

    record2=records.iloc[5:9]
    record2.rename(columns={'BANK_NIFTY':'NIFTY'},inplace=True)

    record3=records.iloc[10:]
    record3.rename(columns={'BANK_NIFTY':'FINNIFTY'},inplace=True)


    json1=record1.reset_index().to_json(orient ='records') 
    json2=record2.reset_index().to_json(orient ='records') 
    json3=record3.reset_index().to_json(orient ='records') 
    
    return [json1,json2,json3]

  


def generateImageXlsx(tweet=['Todays data:']):
    obj = tweet_history.objects.create(tweet=tweet)
    img_output='media/tweet/'+str(obj.id)+'.png'
    img_input='http://127.0.0.1:8000/xlsx-data/'

    subprocess.run(["wkhtmltoimage", "--width", "1200", "--height", "1200", img_input, img_output])
    time.sleep(2)

    obj.tweet_img = 'tweet/'+str(obj.id)+'.png'
    obj.save()
    # tweet_with_image(obj.tweet,obj.tweet_img.url)