import streamlit as st
from streamlit.components.html import HTML


html_url = "https://raw.githubusercontent.com/deedeeharris/apps/main/plotting/time_series.html"

iframe = '<iframe src="{}" width="800" height="600"></iframe>'.format(html_url)
HTML(iframe)
