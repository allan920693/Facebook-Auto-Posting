# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:32:14 2016

@author: YuJia
"""
import facebook
import time
from bs4 import BeautifulSoup
import schedule
import os
from datetime import datetime
from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By


def getExtendToken(user_token,app_id,app_secret):

    graphMe = facebook.GraphAPI(user_token)
    # Extend the expiration time of a valid OAuth access token.
    long_token = graphMe.extend_access_token(app_id, app_secret)
    return long_token['access_token']

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
 
def scrapVideo(): 
    keywords = ['Lebron','Curry','Westbrook','Harden','Jeremy']
    i = datetime.now()
    yesterday = i.day-1               
    browser_c = Firefox()
    browser_c.set_window_position(0, 0) 
    browser_c.set_window_size(1050, 700)  
     
    browser_c.get('https://www.youtube.com/channel/UCR_eeue4E0jNBz8A55DOuOg')
    soup = BeautifulSoup(browser_c.page_source)
    
    itemsThisPage = soup.select('.yt-lockup-content h3.yt-lockup-title')
    for video in itemsThisPage:
        text = video.find('a')
        videoText = str(text)
        videoTitleText = find_between (videoText, 'title="', '"' )
        for word in keywords:
          if  word in  videoTitleText and str(yesterday) in videoTitleText:
             player = word  
             herf =  find_between (videoText, 'href="', '"' )
             fullHerf = 'https://www.youtube.com'+herf
             return fullHerf, videoTitleText, player
             break  
       
       
    browser_c.quit()
    
def postFB():  
    
    user_token = 'Paste your user token'
    app_id = 'Paste your app_id' # Obtained from https://developers.facebook.com/
    app_secret = 'Paste your app_secret' # Obtained from https://developers.facebook.com/
    longToken = getExtendToken(user_token,app_id,app_secret)
  
    graphMe = facebook.GraphAPI(longToken)
     
    profile = graphMe.get_object("me")
    posts = graphMe.get_connections(profile['id'],'posts')       
    
    [fullHerf, videoTitleText,player] = scrapVideo()
       
    attachment =  {
        'name': videoTitleText,
        'link': fullHerf
    }

    graphMe.put_wall_post(message='Daily NBA Video-'+player+'-HighLight', attachment=attachment)
    print "Post Done at "+   str(datetime.now()) 
     
    

schedule.every().day.at("18:30").do(postFB)        
        

while 1:
    schedule.run_pending()
    time.sleep(1)    
        
os.system("pause")