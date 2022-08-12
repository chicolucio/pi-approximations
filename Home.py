import streamlit as st

from src.helpers import text_from_markdown, load_css, find_me_buttons

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

sites = ("linkedin", "portfolio", "github", "github_sponsors")
links = (
    "flsbustamante",
    "https://franciscobustamante.com.br",
    "chicolucio",
    "chicolucio",
)

columns = st.columns([1, 1, 1.2, 1, 1])

with columns[2]:
    st.write('Developed by: Francisco Bustamante')
    st.info("Follow me for more interactive projects:")
    for site, link in zip(sites, links):
        find_me_buttons(site, link)
