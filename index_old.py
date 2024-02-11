import streamlit as st
from utils import *
import logging

def main():
    st.set_page_config(layout="wide")
    # set up logging
    logging.basicConfig(filename='logs.log', format='%(message)s', level=logging.INFO)
    #
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
    # authenticate server
    tableau_auth, server = authenticate(
        tokan_name = st.secrets["token_name"], 
        token_value = st.secrets["token_value"], 
        site_id = st.secrets["site_id"], 
        server_url = st.secrets["server_url"]
    )
    with server.auth.sign_in(tableau_auth):
        logging.info("Authentication Successful")
        workbook = st.sidebar.selectbox(
            label="Select Workbook",
            options=["Dashboard B"],
            index=0
        )
    # refresh_view_button = st.sidebar.checkbox(
    #     label='Refresh Views'
    # )
    # if refresh_view_button:
        views = fetchViews(
            server=server,
            workbook_name=workbook
        )
        selected_views= st.sidebar.selectbox(
            label=f"Views in {workbook}",
            options=views,
            format_func = lambda x: x.name,
            key="select_view_selectbox"
        )
        show_selected_view = st.sidebar.button(label="Show Selected View", on_click=set_state, args=(1,))
            
        if st.session_state.stage>=1:
            # """ If we want to dynamically show previews of multiple selected views, use this block. """
            # col1, col2, col3 = st.columns(3, gap="large")
            # column_linked_list = LinkedList()
            # for c in [col1, col2, col3]:
            #     column_linked_list.insert(c)
            # column_linked_list.attach_ends()
            # column_linked_list.current_node = column_linked_list.head
            # # for view in selected_views:
            # server.views.populate_preview_image(selected_views)
            # column_linked_list.current_node.data.image(image=selected_views.preview_image, caption=selected_views.name, use_column_width="always")
            # column_linked_list.current_node = column_linked_list.current_node.next
            populate_preview_image(server, selected_views)
            col1, col2 = st.columns(2, gap="large")
            col1.subheader(body="Preview")
            col1.image(image=selected_views.preview_image, caption=selected_views.name, use_column_width="always")
            col2.subheader(body="Filter your view")
            col2.subheader(body="Download your view")
            populate_view(server, selected_views)
            download_selected_views = col2.download_button(
                label="Download Selected View",
                data=selected_views.image,
                file_name=f'{selected_views.name.replace(' ','_')}.png',
                mime="image/png",
                type="primary",
                on_click=set_state,
                args=(2,)
            )
            if st.session_state.stage == 2:
                st.toast('Image downloaded successfully', icon="✅")
                set_state(0)
                st.rerun()

            
        # download_selected_views = st.sidebar.button(label="Download Selected View")
        # if download_selected_views:
            
            
    
    
if __name__ == '__main__':
    main()