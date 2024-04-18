import streamlit as st

st.set_page_config(page_title="Tableau Image Downloader", layout="wide")

container1 = st.container(border=None)
_, a2, _ = container1.columns(3)
_, a2_2, _ = a2.columns([1,5,1])
a2_2.title("Enter Password")

container2 = st.container(border=None)
_, b2, _ = container2.columns(3)
pss = b2.text_input(label="", type="password")

container3 = st.container(border=None)
_, c2, _ = container3.columns(3)
_, c2_2, _ = c2.columns([2,1,2])
login = c2_2.button(label="Login")

if login:
    if pss == st.secrets.password:
        st.switch_page("pages/index.py")
    else:
        st.error("Incorrect password, try again...")