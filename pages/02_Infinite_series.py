from itertools import cycle

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.compute_pi import pi_leibniz, pi_euler
from src.helpers import load_css, CONFIG_PLOTLY, error, text_from_markdown

st.set_page_config(layout="centered", page_title="π - Infinite series",
                   page_icon=":chart_with_upwards_trend:")

load_css("pages/styles.css")

PAGE_TEXT_FILE = 'pages/02_Infinite_series.md'
content = text_from_markdown(PAGE_TEXT_FILE)

with st.sidebar:
    maximum = st.slider('Terms', 0, 400, 100, 20)
    st.write('Estimation of pi - Euler:', pi_euler(maximum))
    st.write('Error - Euler:', round(error(pi_euler(maximum), np.pi) * 100, 2), '%')
    st.write('Estimation of pi - Leibniz:', pi_leibniz(maximum))
    st.write('Error - Leibniz:', round(error(pi_leibniz(maximum), np.pi) * 100, 2), '%')

terms = range(1, maximum + 1)

fig = go.Figure()

trace_leibniz = go.Scatter(x=list(terms),
                           y=[pi_leibniz(i) for i in terms],
                           name='Leibniz',
                           )

trace_euler = go.Scatter(x=list(terms),
                         y=[pi_euler(i) for i in terms],
                         name='Euler',
                         )

fig.add_trace(trace_leibniz)
fig.add_trace(trace_euler)
fig.add_hline(y=np.pi, line_dash='dot',
              annotation_text='Pi value',
              annotation_position='top left')

palette = cycle(px.colors.qualitative.Plotly)

fig.add_trace(trace_leibniz.update(xaxis='x2', yaxis='y2',
                                   showlegend=False,
                                   line=dict(color=next(palette)),
                                   ))
fig.add_trace(trace_euler.update(xaxis='x2', yaxis='y2',
                                 showlegend=False,
                                 line=dict(color=next(palette)),
                                 ))

fig.add_hline(xref='x2', y=np.pi, line_dash='dot')  # ignored by Plotly. Issue #3755
# work around to add pi horizontal line:                          (PT-BR-> gambiarra!)
fig.add_shape(type="line", xref="x2 domain", yref="y2", x0=0, y0=np.pi, x1=1, y1=np.pi,
              line=dict(dash="dot"),)

last_quarter_x = trace_euler.x[int(len(trace_euler.x) * 0.75):]
range_x2 = [min(last_quarter_x, default=0), max(last_quarter_x, default=0)]

fig.update_layout(
    legend=dict(orientation='h',
                yanchor='top',
                y=-0.2,
                xanchor='left'),
    margin=dict(l=20, r=20, t=20, b=20),
    modebar=dict(orientation='v'),
    xaxis=dict(title='Terms'),
    yaxis=dict(title='Approximation'),
    xaxis2=dict(domain=[0.7, 0.95], anchor='y2', range=range_x2,
                showline=True, mirror=True, linecolor='black', linewidth=1,
                ),
    yaxis2=dict(domain=[0.2, 0.5], anchor='x2', range=[3.13, 3.1425],
                showline=True, mirror=True, linecolor='black', linewidth=1,
                ),
)

fig.add_annotation(xref='x2 domain', yref='y2 domain',
                   x=0.5, y=1,
                   text='Zoom',
                   showarrow=False,
                   yanchor='bottom',
                   )


st.markdown(''.join(content[0]))
st.plotly_chart(fig, use_container_width=True, config=CONFIG_PLOTLY)
st.markdown(''.join(content[1]))
