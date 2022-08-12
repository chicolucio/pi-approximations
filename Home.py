import streamlit as st

from src.helpers import text_from_markdown, load_css

st.set_page_config(layout="centered", page_title="π approximations",
                   page_icon=":chart_with_upwards_trend:")

load_css("pages/styles.css")

PAGE_TEXT_FILE = 'pages/01_Home.md'
content = text_from_markdown(PAGE_TEXT_FILE)

st.markdown(''.join(content[0]))
st.markdown(''.join(content[1]))

st.image('https://upload.wikimedia.org/wikipedia/commons/4/4a/Pi-unrolled_slow.gif',
         caption='Animation illustrating the ratio. Source: Wikipedia')

st.markdown(''.join(content[2]))
