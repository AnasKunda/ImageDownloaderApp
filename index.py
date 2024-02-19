import streamlit as st
from utils import *
import logging
import zipfile
import io
import base64
import tableauserverclient as TSC
import streamlit.components.v1 as components

def main():
    st.set_page_config(page_title="Tableau Image Downloader", layout="centered")
    # set up logging
    logging.basicConfig(filename='logs.log', format='%(message)s', level=logging.INFO)
    #
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
        
    # Get Filters
    if st.session_state.stage == 0:
        filters = get_filters(
            server_url = st.secrets["server_url"],
            token_name = st.secrets["token_name"], 
            token_value = st.secrets["token_value"], 
            site_name = st.secrets["site_name"],
            site_id = st.secrets["site_id"]
        )
        st.session_state.filter = filters
        st.session_state.stage = 1
    # authenticate server
    tableau_auth, server = authenticate(
        tokan_name = st.secrets["token_name"], 
        token_value = st.secrets["token_value"], 
        site_id = st.secrets["site_id"], 
        server_url = st.secrets["server_url"]
    )
    with server.auth.sign_in(tableau_auth):
        logging.info("Authentication Successful")
        ### WORKBOOK SELECTOR. RIGHT NOW NOT NEEDED BUT CAN BE USED FOR FUTURE
        # workbook = st.selectbox(
        #     label="Select Workbook",
        #     options=["Dashboard B"],
        #     index=0
        # )
        views = fetchViews(
            _server=server,
            workbook_name="Dashboard B"
        )
        
        default = ["Serve View", "Return View (Heat Map)"]
        view_dict = [{"View":v.name, "Selected":True if v.name in default else False} for v in views]
        
        with st.form(key="Select Views", border=False):
            # selected_views= st.multiselect(
            #     label=f"Views in Dashboard B",
            #     options=views,
            #     default=views[:3],
            #     format_func = lambda x: x.name,
            #     key="select_view_selectbox"
            # )
            col_1, col_2 = st.columns([3,2])
            # Filter Selection
            col_2.subheader("Select Filter")
            # col2.subheader("Player Name")
            for filter_name, filter_values in st.session_state.filter.items():
                selected_name = col_2.selectbox(
                    label=filter_name,
                    options=filter_values,
                    format_func=lambda x: x.split(':')[-1]
                )
            # container2 = st.container()
            # _, col_2, _ = container2.columns([1,3,1])
            views_df = col_1.data_editor(
                data=view_dict,
                column_config={"Selected":st.column_config.CheckboxColumn()},
                key="View DataFrame",
                height=600
            )
            
            col_2.subheader('Download Views')
            submit_button = col_2.form_submit_button(label="Download Selected Views", on_click=set_state, args=(2,))
            # show_selected_view = st.sidebar.button(label="Show Selected View", on_click=set_state, args=(1,))
        if submit_button:
            selected_rows = [view_d["View"] for view_d in views_df if view_d["Selected"]==True]
            selected_views = [v for v in views if v.name in selected_rows]
            if selected_name!='None:None':
                image_request_object = TSC.ImageRequestOptions()
                image_options = image_request_object.vf(*selected_name.split(":"))
                image_option_names = selected_name
            else:
                image_options, image_option_names = None, None
            create_zip(server, selected_views, [v.name for v in selected_views], image_options, image_option_names)
        # if st.session_state.stage == 2:
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