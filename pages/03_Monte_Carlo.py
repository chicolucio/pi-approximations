import random

import streamlit as st

from src.compute_pi import PiMonteCarlo
from src.helpers import load_css, CONFIG_PLOTLY, text_from_markdown

st.set_page_config(layout="centered", page_title="π - Monte Carlo",
                   page_icon=":chart_with_upwards_trend:")

load_css("pages/styles.css")

PAGE_TEXT_FILE = 'pages/03_Monte_Carlo.md'
content = text_from_markdown(PAGE_TEXT_FILE)

MINIMUM = 1
MAXIMUM = 10_000
INITIAL_VALUE = 10

# TODO create page text

if 'random_integer' not in st.session_state:
    st.session_state['random_integer'] = INITIAL_VALUE


def random_integer():
    st.session_state['random_integer'] = random.randint(MINIMUM, MAXIMUM)


with st.sidebar:
    points = st.slider('Points', 0, MAXIMUM,
                       st.session_state['random_integer'], 500)
    st.button('Random number', on_click=random_integer)

pi_monte_carlo = PiMonteCarlo(1)
pi_monte_carlo.points = int(points) if points != 0 else 1

st.markdown(''.join(content[0]))
st.plotly_chart(pi_monte_carlo.plot(backend='plotly', arc=True),
                use_container_width=True,
                config=CONFIG_PLOTLY)
st.markdown(''.join(content[1]))

with st.sidebar:
    st.write('Number of points:', pi_monte_carlo.points)
    st.write('Estimation of pi:', pi_monte_carlo.calculate)
    st.write('Percent error:', round(pi_monte_carlo.error() * 100, 2), '%')
