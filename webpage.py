import streamlit as st
import pandas as pd
import preprocessing,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Drag your chat here")
if uploaded_file is not None :
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')

    df = preprocessing.preprocess(data)
    st.title("Top Statistics")

    users_list = df['user'].unique().tolist()
    users_list.remove("group_notification")
    users_list.sort()
    users_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("show analysis wrt to",users_list)

    if st.sidebar.button("Show Analysis") :

        num_message,num_word,media_count,link_count = helper.fetch_stats(selected_user,df)
        col1 , col2 , col3 , col4 = st.columns(4)

        with col1 :
            st.header("Total messages")
            st.title(num_message)

        with col2 :
            st.header("Total words")
            st.title(num_word)
        
        with col3 : 
            st.header("Total Media shared")
            st.title(media_count)

        with col4 :
            st.header("Total Links shared")
            st.title(link_count)

    ### finding the most active users in the group
    if selected_user == 'Overall' :
        st.title("Most active users")
        x , chat_per = helper.most_busy_users(df)
        fig , ax = plt.subplots()

        col5 , col6 = st.columns(2)

        with col5 :
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col6 :
            st.dataframe(chat_per)


    ### Time Analysis
    st.title("Analysis of chat with time")
    timeline_df = helper.time_analysis(selected_user,df)
    # st.dataframe(timeline_df)                          # To print the data frame
    # st.area_chart(timeline_df,x='time',y='message',x_label="Number of Messages",y_label="Time") ## Area chart
    st.line_chart(timeline_df,x='time',y='message',x_label="Number of Messages",y_label="Time")


    ### Word Cloud
    st.title("Word Cloud --->")
    df_wc= helper.create_word_cloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    ### most common words
    st.title("Most Common words used with their count ")
    common_words_df = helper.most_common_words(selected_user,df)
    st.bar_chart(common_words_df,x='Words',y="Count",sort=True)
    


    ### Analysis of Emojis
    st.title("Emojis Used")
    emoji_df = helper.emoji_hepler(selected_user,df)
    st.dataframe(emoji_df)


    st.title("Chat Data")
    st.dataframe(df)