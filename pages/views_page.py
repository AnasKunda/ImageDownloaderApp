import streamlit as st
from utils import *
import logging
import zipfile
import io
import base64
import tableauserverclient as TSC
import streamlit.components.v1 as components
from constants import *

def main():
    st.set_page_config(page_title="Select Views", layout="wide")
    # set up logging
    logging.basicConfig(filename='logs.log', format='%(message)s', level=logging.INFO)

    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    # Workbook selectbox
    st.title("Select Workbook")
    workbook = st.selectbox(
            label=" ",
            options=["Dashboard B", "Hawkeye Succinct with Benchmarks"],
            index=None
        )
    # refresh views button
    # It sets session state to 1 if user clicks on this button
    refresh_views_button = st.button(
        label='Refresh Views',
        on_click=set_state,
        args=(1,)
    )
        
    if workbook:
        # authenticate server
        tableau_auth, server = authenticate(
            tokan_name = st.secrets["token_name"], 
            token_value = st.secrets["token_value"], 
            site_id = st.secrets["site_id"], 
            server_url = st.secrets["server_url"]
        )
        # The if condition states the user has pressed refresh views button or not
        if st.session_state.stage != 1: # user has not pressed refresh views button
            with server.auth.sign_in(tableau_auth):
                logging.info("Authentication Successful")
                views = fetchViews(
                    _server=server,
                    workbook_name=workbook
                )
        else: # user has pressed refresh views button. 
            fetchViews.clear() # Clear the cache so that new view list can be fetched from the server.
            with server.auth.sign_in(tableau_auth):
                logging.info("Authentication Successful")
                views = fetchViews(
                    _server=server,
                    workbook_name=workbook
                )
        # Fetch common filters    
        if 'filter' not in st.session_state:
            filters = get_filters(
                server_url = st.secrets["server_url"],
                token_name = st.secrets["token_name"], 
                token_value = st.secrets["token_value"], 
                site_name = st.secrets["site_name"],
                site_id = st.secrets["site_id"]
            )
            
            st.session_state.filter = filters
        
        # Views that are selected when screen loads
        default = ["Serve View", "Return View (Heat Map)"]
        view_dict = [{"View":v.name, "Selected":True if v.name in default else False} for v in views]
        
        # The form contains common filter selection, view selection, preference selection
        # and download button.
        with st.form(key="Select Views", border=False):
            col1, col2, col3 = st.columns(3)
            # Filter Selection
            col1.subheader("Select Filter")
            
            if 'selected_filter_value' not in st.session_state:
                # the st.session_state.selected_filter_value stores the common filter values
                st.session_state.selected_filter_value = {} 
            # Iterate over filters to load their selectboxes
            for filter_name, filter_values in st.session_state.filter.items():
                default = 0 if filter_dict[filter_name]["has_default"] else None
                selected_value = col1.selectbox(
                    label=filter_name,
                    options=filter_values,
                    format_func=lambda x: x.split(':')[-1],
                    index=default,
                    placeholder="All"
                )
                st.session_state.selected_filter_value[filter_name] = selected_value
            # Table of view selection comes here
            col2.subheader('Select Views')
            views_df = col2.data_editor(
                data=view_dict,
                column_config={"Selected":st.column_config.CheckboxColumn()},
                key="View DataFrame",
                height=600,
                width=400
            )
            # Preference selection selectbox comes here
            with col3:
                st.subheader('Load from Preferences')
                pref_names = load_pref()
                preference = st.selectbox(label="", key="pref_select", options=pref_names, index=None)
                st.subheader('Go to Next Page')
                submit_button = st.form_submit_button(label="Next")
      
        with st.form(key='delete preference', border=False):
            col_1, col_2, col_3 = st.columns(3)
            
            with col_1:
                st.subheader('Delete Preference')
                del_pref_names = load_pref()
                del_preference = st.selectbox(label="", key="del_pref_select", options=del_pref_names, index=None)
                del_submit_button = st.form_submit_button(label="Delete Preference")
        
        if del_submit_button:
            status = delete_pref(pref_name=del_preference)
            st.rerun()
        
        if submit_button:
            st.session_state.views = views
            st.session_state.views_df = views_df
            if not preference:  
                # if no preference is selected, the flow will go to iterations page to select iterations.
                # otherwise, it will download images from the saved preferences.
                st.switch_page("pages/iteration_page.py")
            else:
                create_zip_from_pref(preference)
                 
if __name__ == '__main__':
    main()