import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique users
    users_list = df['user'].unique().tolist()
    #users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("show analysis wrt",users_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_msgs,num_words,num_medias,num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_msgs)

        with col2:
            st.header('Total Words')
            st.title(num_words)

        with col3:
            st.header('Media Shared')
            st.title(num_medias)

        with col4:
            st.header('Total Links')
            st.title(num_links)

        #monthly_timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily_timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity-Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding the active users in group
        if selected_user == 'Overall':
            st.title("Most Active Users")
            x,new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordCloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most-common-words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        #st.dataframe(most_common_df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji
        st.title('Emojis Analysis')
        emojis_df = helper.emoji_helper(selected_user,df)
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emojis_df[1].head(),labels=emojis_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
