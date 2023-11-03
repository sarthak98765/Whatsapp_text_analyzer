import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import stats
import numpy as np
import re
import seaborn as sns

st.set_page_config(page_title='WhatsApp Chat Analyzer',layout='wide', initial_sidebar_state='expanded')

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Upload a WhatsApp Chat File:')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df['User'].unique().tolist()

    user_list.sort()
    user_list.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t:", user_list)
    st.title("Whatsapp Chat Analysis for "+ selected_user)
    
    
    # Stats
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_msgs, links = stats.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Links Shared")
            st.title(links)
 
        # monthly timeline
        st.title('Monthly Timeline')
        timeline = stats.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title('Overall Timeline')
        daily_timeline = stats.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Only_date'], daily_timeline['Message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Days")
            busy_day = stats.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Months")
            busy_month = stats.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity heatmap
        st.title('Weekly Activity Map')
        user_heatmap = stats.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the most active users in a group
        if selected_user == 'Overall':
            st.title("Most Active Users")
            x, new_df = stats.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title('Wordcloud')
        df_wc = stats.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = stats.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='red')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # most common emojis
        emoji_df = stats.emoji_stats(selected_user, df)
        st.title("Emoji Analysis")

        if emoji_df.empty is True:
            st.header("No Emojis Used")

        else:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
