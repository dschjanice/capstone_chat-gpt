## run the app by tiping in the terminal
# streamlit run notebooks/streamlit_app.py  --theme.base="light"  --theme.primaryColor="#1b786e"  --theme.backgroundColor="#eeeeee" --theme.secondaryBackgroundColor="#f7f7f7" --theme.textColor="#424242" --theme.font="sans serif"

import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import datetime as dt
from datetime import datetime
import seaborn as sns


st.set_page_config(layout="wide")

## add a title
st.title('ReviewRevealer')

## add text in markdown
st.write('We are showing ChatGPT Reviews for iOS and Android')

# Load df
df_raw = pd.read_csv("/Users/janice/Documents/Bootcamp/Git/Capstone/capstone_chat-gpt/data/chatgpt-combined_short_topics.csv")
df_raw['appVersion'] = df_raw['appVersion'].replace(np.nan, "not available")
df_raw["Operating System"] = np.where(df_raw.Source == 'Apple', "iOS", "Android")
df_raw['at_dt'] = pd.to_datetime(df_raw['at'])

st.sidebar.write("Filter the shown data")
df_source = df_raw
df_app = df_raw
if st.sidebar.toggle('Select iOS or Android Reviews'):
    source = st.sidebar.selectbox("Filter here on the operating system", df_raw['Operating System'].sort_values().unique())
    df_source = df_raw[df_raw['Operating System'].isin([source])]
    df_app = df_source
    if source == 'Android':
        appversion = st.sidebar.multiselect(
            "Filter here on the Android AppVersion", 
            df_source['appVersion'].sort_values().unique(),
            default=list(df_app['appVersion'].sort_values().unique()))
        df_app = df_source[df_source['appVersion'].isin(appversion)]

category = st.sidebar.multiselect(
    "Filter here on the Sentiment of the Review", 
    df_app['category'].sort_values().unique(), 
    default=list(df_app['category'].sort_values().unique()))

review_date = st.sidebar.date_input(
    "Review Date Range", 
    (df_app['at_dt'].min(), 
    df_app['at_dt'].max()),
    key='#date_range',)

df_cat = df_app[df_app['category'].isin(category)]
df = df_cat.loc[(pd.to_datetime(df_cat['at']) >= pd.to_datetime(review_date[0])) & (pd.to_datetime(df_cat['at']) <= pd.to_datetime(review_date[1]))]

## Plots
c1 = '#c0791b'
c2 = '#1b786e'
c3 = '#424242'
c4 = '#5f5f5f'
c5 = '#202112'
f = 16

## absolute numbers
col1_1, col1_2= st.columns(2)
with col1_1:
    for var in ['category']:
        list=[]
        for i in range(1,6,1):
            x = df[var].unique()[i-1] if df[var].nunique() >= i else ''
            list.append(x)
        fig = px.histogram(df.sort_values(var), 
            x=var,
            title="Number of Reviews by " + var.capitalize(),
            labels={'count': 'Reviews'},
            text_auto=True,
            template='ggplot2',
            hover_data={"at_ym": "|%B %d, %Y"},
            color=var,
            color_discrete_map={
                list[0]: c1, 
                list[1]: c2, 
                list[2]: c3, 
                list[3]: c4,     
                list[4]: c5
                })
        fig.update_traces(textposition='auto')
        fig.update_layout(
            height=300,
            legend_title_text=var.capitalize(),
            font=dict(size=f),
            xaxis_title="Category",
            xaxis_title_font_size=f,
            xaxis_tickfont_size=f,
            yaxis_title="Reviews",
            yaxis_title_font_size=f,
            yaxis_tickfont_size=f, 
            legend_font_size=f,
            legend_title = dict(font = dict(size = f)))
        fig.update_xaxes(
            dtick="M2",
            tickformat="%B\n%Y")
        st.plotly_chart(fig, use_container_width=True,height=800)
        
with col1_2:    
    #apparently you dont need to write st.write and just “” as magic commands
    if st.checkbox(f'Push this button to show sample dataframe.'): # {appversion}'):
        st.write(df[['Source', 'content', 'category', 'Label']].sample(10))
    
### line charts ###
col2_1, col2_2= st.columns(2)
default_var = ['category']
with col2_1:
    st.subheader('Analysis per Topic')  
    if st.toggle('Select to compare by operating system'):
        default_var = ['Source']
with col2_2:
    topics = st.selectbox("Filter here on the topic", df['Label'].sort_values().unique(), index=4)
    df_topic = df[df['Label'].isin([topics])]
col3_1, col3_2 = st.columns(2)
with col3_1:
    st.write(f"**Weekly Reviews for the Topic {topics}**")
    for var in default_var:
        df_chart = df_topic.groupby(['at_wy',var]).size().reset_index(name='Reviews').sort_values([var, 'at_wy'], ascending=False)
        fig = px.line(df_chart, 
            y='Reviews', 
            x='at_wy',
            labels={'at_wy': 'Review Week'},
            text='Reviews',
            template='ggplot2',
            hover_data={"at_wy": "|%B %d, %Y"},
            color=var,
            color_discrete_sequence=[c1, c2, c3, c4, c5])
        fig.update_traces(textposition='top center')
        fig.update_layout(
            legend_title_text=var.capitalize(),
            font=dict(size=f),
            xaxis_title="Category",
            xaxis_title_font_size=f,
            xaxis_tickfont_size=f,
            yaxis_title="Reviews",
            yaxis_title_font_size=f,
            yaxis_tickfont_size=f, 
            legend_font_size=f,
            legend_title = dict(font = dict(size = f)))
        fig.update_xaxes(
            tickformat='%d/%m/%Y ', 
            overwrite = True)
        fig.add_annotation(
            x=dt.date(2023, 10, 1)
            , y=np.max(df_chart['Reviews']) + 0.1*np.max(df_chart['Reviews'])
            , text=f'New AppVersion  <br> Release'
            , yanchor='top'
            , showarrow=False
            , ax=-20
            , ay=-30
            , align="center"
            ,)
        fig.add_vline(
            x=dt.date(2023, 10, 1), 
            line_width=3, 
            line_dash="dot", 
            line_color="grey")
        st.plotly_chart(fig)
with col3_2:
    st.write(f"**Weekly Proportion of Reviews for the Topic {topics}**")
    for var in default_var:
        df_chart = df_topic.groupby(['at_wy',var]).size().reset_index(name='Reviews').sort_values([var, 'at_wy'], ascending=False)
        df_chart['Reviews (%)'] = df_chart.groupby('at_wy')['Reviews'].transform(lambda x: x / x.sum() * 100)
        max_cat = df_chart[var].iloc[np.argmax(df_chart['Reviews (%)'])]
        max_val = np.max(df_chart['Reviews (%)'])
        fig = px.line(df_chart, 
            y='Reviews (%)', 
            x='at_wy',
            labels={'at_wy': 'Review Week'},
            #text = np.where(df_chart["Reviews (%)"]==max_val ,df_chart['Reviews (%)'], " "), 
            template='ggplot2',
            hover_data={"at_wy": "|%B %d, %Y"},
            color=var,
            color_discrete_sequence=[c1, c2, c3, c4, c5])
        # fig.update_traces(
        #     textposition='bottom center',
        #     texttemplate= "%{text:2.1f}%",
        #     selector = ({'name':str(max_cat)}))
        fig.update_layout(
            legend_title_text=var.capitalize(),
            font=dict(size=f),
            xaxis_title="Category",
            xaxis_title_font_size=f,
            xaxis_tickfont_size=f,
            yaxis_title="Reviews (%)",
            yaxis_title_font_size=f,
            yaxis_tickfont_size=f, 
            legend_font_size=f,
            legend_title = dict(font = dict(size = f)))
        fig.update_xaxes(
            tickformat='%d/%m/%Y', 
            overwrite = True)
        fig.add_annotation(
            x=dt.date(2023, 10, 1)
            , y=np.max(df_chart['Reviews (%)']) + 10
            , text=f'New AppVersion  <br> Release'
            , yanchor='top'
            , showarrow=False
            , ax=-20
            , ay=-30
            , align="center"
            ,)
        fig.add_vline(
            x=dt.date(2023, 10, 1), 
            line_width=3, 
            line_dash="dot", 
            line_color="grey")
        st.plotly_chart(fig)
        
col4_1, col4_2 = st.columns(2)
with col4_1:
    st.write(f"**Have a look at this beautiful wordcloud for the topic {topics}.**")
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="#eeeeee", colormap='BrBG').generate(' '.join(df_topic['content']))
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)
with col4_2:
    st.write(f'**Here you can see some example sentences for the topic.**')
    st.write(df[['content', 'category']].sample(9))
