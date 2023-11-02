import re
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns

def gettimeanddate(string):
     string = string.split(',')
     date, time = string[0], string[1]
     time=time.split('-')
     time=time[0].strip()

     return date+" "+time

def getstring(text):
    return text.split('\n')[0]

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s[APap][Mm]\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message':messages, 'message_date': dates})
    # converting the message_date to date time format
    df['message_date'] = df['message_date'].apply(
        lambda text: gettimeanddate(text))
    
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('whatsapp notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df['message']=df['message'].apply(lambda text:getstring(text))

    df.drop(['user_message'],axis=1)
    df=df[['message','date','user']]
    df=df.rename(columns={'message':'Message','date':'Date','user':'User'})

    df['Only_date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df



