import streamlit as st
import streamlit.components.v1 as components

html_url = "https://raw.githubusercontent.com/deedeeharris/apps/main/plotting/time_series.html"


p = open(html_url)
components.html(p.read())
