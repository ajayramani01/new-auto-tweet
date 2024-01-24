from .models import tweet_history,xlsxFiles
import pandas as pd
import numpy as np
import dataframe_image as dfi
from .tweet_script import tweet_with_image
from PIL import Image

def generateIMG(xlsx,tweet='Todays data:'):

    obj = tweet_history.objects.create(tweet=tweet)
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

    record1=records.iloc[0:4]
    print(record1)
    record2=records.iloc[5:9]
    record2.rename(columns={'BANK NIFTY':'NIFTY'},inplace=True)
    print(record2)
    record3=records.iloc[10:]
    record3.rename(columns={'BANK NIFTY':'FINNIFTY'},inplace=True)
    print(record3)

    dfi.export(record1, 'temp/1.png')
    dfi.export(record2, 'temp/2.png')
    dfi.export(record3, 'temp/3.png')
    list_im = ['temp/1.png', 'temp/2.png', 'temp/3.png']
    imgs    = [ Image.open(i) for i in list_im ]
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

    imgs_comb = np.vstack([i.resize(min_shape) for i in imgs])
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( 'media/tweet/'+str(obj.id)+'.png' )

    obj.tweet_img = 'tweet/'+str(obj.id)+'.png'
    obj.save()
    tweet_with_image(obj.tweet,obj.tweet_img.url)
