## run the app by tiping in the terminal
# streamlit run notebooks/streamlit_app.py  --theme.base="light"  --theme.primaryColor="#1b786e"  --theme.backgroundColor="#eeeeee" --theme.secondaryBackgroundColor="#f7f7f7" --theme.textColor="#424242" --theme.font="sans serif"

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
## add a title
st.title('ReviewRevealer')
## add text in markdown
st.write('We are showing ChatGPT Reviews for iOS and Android')


# Read file and keep in variable
with open("/Users/janice/Documents/Bootcamp/Git/Capstone/capstone_chat-gpt/charts/lda.html" ,'r') as f: 
    html_data = f.read()

## Show in webpage
components.html(html_data, height=800)