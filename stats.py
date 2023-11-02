import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji
import streamlit as st
from wordcloud import WordCloud
from urlextract import URLExtract
extract = URLExtract()


def fetch_stats(selected_user, df):

    if (selected_user != "Overall"):
        df = df[df['user'] == selected_user]

    # fetch the number of msgs
    num_messages = df.shape[0]

    # fetch the number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch the number of media msgs
    num_media_msgs = df[df['Message'] == '<Media omitted>']

    # fetch the number of linls shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words), num_media_msgs.shape[0], len(links)



def most_active_users(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'User': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'whatsapp notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    temp = temp[temp['Message'] != 'This message was deleted\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    words = pd.DataFrame(words, columns=['words'])
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(words['words'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'whatsapp notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    temp = temp[temp['Message'] != 'This message was deleted\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    pure_words = []
    for message in words:
        pure_words.extend([c for c in message if c in emoji.demojize(message)])

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_stats(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c not in emoji.demojize(message)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common((len(Counter(emojis)))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('Only_date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()

def month_activity_map(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if (selected_user != "Overall"):
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', values='Message', aggfunc='count').fillna(0)

    return user_heatmap