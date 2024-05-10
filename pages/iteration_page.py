import streamlit as st
from constants import view_name_patterns, filter_dict
import tableauserverclient as TSC
from utils import create_zip

st.set_page_config(page_title="Set Iterations", layout="wide")
st.title("Select Iterations")

# load selected views from previous page
selected_rows = [view_d["View"] for view_d in st.session_state.views_df if view_d["Selected"]==True]
selected_views = [v for v in st.session_state.views if v.name in selected_rows]

if 'iterations' not in st.session_state:
    # st.session_state.iterations stores the info 
    # about how many iterations user selects for each selected view. 
    st.session_state.iterations = {} 

with st.form(key="iteration_page_form", border=False):
    # load a selectbox for each view
    for view in selected_views:
        view_obj = view_name_patterns[view.name]
        container = st.container()
        container.subheader(f"{view.name}")
        iter_options = list(range(1,11))
        iter = container.selectbox(label="No. of Iterations", key=f'{view.name}_iterations',options=iter_options)
        st.session_state.iterations[view.name] = iter
    
    next_button = st.form_submit_button(label="Go To Download Page")

home_button = st.button("Go Back")

if next_button:    
    st.switch_page("pages/download_page.py")
    
if home_button:
    st.switch_page("./pages/views_page.py")  
        