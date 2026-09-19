import pandas as pd
import numpy as np
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji

## object of URLExtract class
extract = URLExtract()

def fetch_stats(selected_user,df) :

    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    ### Fetch number of messages
    num_message = df.shape[0]

    ### Fetch number of messages
    words = []
    for message in df['message'] :
        words.extend(message.split())

    ### Fetch number of imagees shared
    count_media = 0
    for message in df['message'] :
        if "image omitted" in message :
            count_media += 1
        elif "video omitted" in message :
            count_media += 1

    ### Fetch all Links
    links = []
    for message in df["message"] :
        links.extend(extract.find_urls(message))

    ### Return all the fetched data
    return num_message , len(words) , count_media , len(links)



def most_busy_users(df) :
    ### Top 5 users of the group who have the most messages
    busy_users = df['user'].value_counts().head()
    busy_users.drop("group_notification",inplace=True)

    ### Percentage of mssages
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100 , 2).reset_index().rename(columns={'count' : 'Percent' , 'user' : 'Name'})

    return busy_users , new_df


def create_word_cloud(selected_user,df) :

    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user,df) :
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != 'image omitted']
    temp = temp[temp['message'] != 'video omitted']

    word = []
    for message in temp['message'] :
        word.extend(message.lower().split())

    common_words = pd.DataFrame(Counter(word).most_common(10))
    common_words.rename(columns={0 : 'Words' , 1 : 'Count'},inplace=True)

    return common_words


def emoji_hepler(selected_user,df) :
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message'] :
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))
    emoji_df.rename(columns={1 : 'Emoji' , 2 : 'Counts'},inplace=True)

    return emoji_df

def time_analysis(selected_user,df) :
    if selected_user != "Overall" :
        df = df[df['user'] == selected_user]

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]) :
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline