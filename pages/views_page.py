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
    st.set_page_config(page_title="Tableau Image Downloader", layout="wide")
    # set up logging
    logging.basicConfig(filename='logs.log', format='%(message)s', level=logging.INFO)
    #
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    # Get Filters
    # if st.session_state.stage == 0:
    #     filters = get_filters(
    #         server_url = st.secrets["server_url"],
    #         token_name = st.secrets["token_name"], 
    #         token_value = st.secrets["token_value"], 
    #         site_name = st.secrets["site_name"],
    #         site_id = st.secrets["site_id"]
    #     )
    #     st.session_state.filter = filters
    #     st.session_state.stage = 1
        # with st.form(key="Select Workbook", border=False):
        #     workbook = st.selectbox(
        #         label="Select Workbook",
        #         options=["Dashboard B", "Hawkeye Succinct with Benchmarks"],
        #         index=0
        #     )
        #     submit_workbook_button = st.form_submit_button(label="Fetch Views", on_click=set_workbook, args=(workbook,1,)) 
    st.title("Select Workbook")
    workbook = st.selectbox(
            label=" ",
            options=["Dashboard B", "Hawkeye Succinct with Benchmarks"],
            index=None
        )
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
        if st.session_state.stage != 1:
            with server.auth.sign_in(tableau_auth):
                logging.info("Authentication Successful")
                views = fetchViews(
                    _server=server,
                    workbook_name=workbook
                )
        else:
            fetchViews.clear()
            with server.auth.sign_in(tableau_auth):
                logging.info("Authentication Successful")
                views = fetchViews(
                    _server=server,
                    workbook_name=workbook
                )
            
        if 'filter' not in st.session_state:
            filters = get_filters(
                server_url = st.secrets["server_url"],
                token_name = st.secrets["token_name"], 
                token_value = st.secrets["token_value"], 
                site_name = st.secrets["site_name"],
                site_id = st.secrets["site_id"]
            )
            
            st.session_state.filter = filters
    
        default = ["Serve View", "Return View (Heat Map)"]
        # image_crop_popover = st.popover("Crop Image")
        # view_select = image_crop_popover.selectbox(label="Select View",options=views,format_func=lambda x: x.name)
        
        view_dict = [{"View":v.name, "Selected":True if v.name in default else False} for v in views]
        
        with st.form(key="Select Views", border=False):
            col1, col2, col3 = st.columns(3)
            # Filter Selection
            col1.subheader("Select Filter")
            # col2.subheader("Player Name")
            if 'selected_filter_value' not in st.session_state:
                st.session_state.selected_filter_value = {}
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

            col2.subheader('Select Views')
            views_df = col2.data_editor(
                data=view_dict,
                column_config={"Selected":st.column_config.CheckboxColumn()},
                key="View DataFrame",
                height=600,
                width=400
            )

            with col3:
                st.subheader('Load from Preferences')
                pref_names = load_pref()
                preference = st.selectbox(label="", key="pref_select", options=pref_names, index=None)
                st.subheader('Go to Next Page')
                submit_button = st.form_submit_button(label="Next")
            # show_selected_view = st.sidebar.button(label="Show Selected View", on_click=set_state, args=(1,))
      
            
        if submit_button:
            st.session_state.views = views
            st.session_state.views_df = views_df
            if not preference:
                st.switch_page("pages/iteration_page.py")
            else:
                create_zip_from_pref(preference)
        #     selected_rows = [view_d["View"] for view_d in views_df if view_d["Selected"]==True]
        #     selected_views = [v for v in views if v.name in selected_rows]
        #     # selected_name = st.session_state.selected_filter_value[list(st.session_state.selected_filter_value.keys())[0]]
        #     selected_filters, image_option_names = [], []
        #     for filter_name, selected_filter_value in st.session_state.selected_filter_value.items():
                
        #         if (filter_dict[filter_name]['is_required']==True) or ((filter_dict[filter_name].is_required==False) and (selected_filter_value != st.session_state.filter[filter_name][0])):
        #             # image_options = image_request_object.vf(*selected_filter_value.split(":"))
        #             selected_filters.extend(selected_filter_value.split(":"))
        #             image_option_names.append(selected_filter_value)
        #         else:
        #             continue
                
        #     image_request_object = TSC.ImageRequestOptions()
        #     image_request_object.vf(*selected_filters)
        #     # image_request_object.vf('surface','Hard')
            
        #     create_zip(selected_views, [v.name for v in selected_views], image_request_object, image_option_names)


        #     st.subheader('Download Views')
        #     st.download_button(label='Download Selected Views', data=zip_file, file_name='Tableau_images.zip', mime='application/zip', on_click=set_state, args=(1,))
                
    
                # download_selected_views = st.download_button(
                #     label="Download Selected Views",
                #     data=zip_buffer,
                #     file_name='tableau_images.zip',
                #     mime="application/zip",
                #     type="primary",
                #     on_click=set_state,
                #     args=(1,)
                # )
        ### TOAST NOTIFICATION
        # if st.session_state.stage == 1:
        #     st.toast('Image downloaded successfully', icon="✅")
        #     set_state(0)
        #     st.rerun()

            
        # download_selected_views = st.sidebar.button(label="Download Selected View")
        # if download_selected_views:
            
            
    
    
if __name__ == '__main__':
    main()