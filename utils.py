import tableauserverclient as TSC
import streamlit as st
import zipfile
import io
import base64
import streamlit.components.v1 as components
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_views_dataframe, get_view_data_dataframe
from constants import *
from PIL import Image, ImageFile
from pathlib import Path
import pandas as pd

# @st.cache_data
def authenticate(tokan_name, token_value, site_id, server_url):
    """Connect to Tableau server using Personal Access Token

    Args:
        tokan_name (string): The personal access token name.
        token_value (string): The personal access token value.
        site_id (string): The portion of the URL that follows the /site/ in the URL.
        server_url (string): Specifies the address of the Tableau Server or Tableau Cloud (for example, https://MY-SERVER/).
        
    Returns:
    tableau_auth (PersonalAccessTokenAuth object)
    server (Server object)
    """
    tableau_auth = TSC.PersonalAccessTokenAuth(tokan_name, token_value, site_id)
    server = TSC.Server(server_url, use_server_version=True)
    
    return tableau_auth, server

def refresh_views(server,workbook_name):
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 workbook_name))
    fetched_workbook, _ = server.workbooks.get(
        req_options = req_option
    )
    server.workbooks.populate_views(fetched_workbook[0])
    # _server.workbooks.populate_preview_image(fetched_workbook[0])
    return fetched_workbook[0].views

@st.cache_data
def fetchViews(_server, workbook_name):
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                 TSC.RequestOptions.Operator.Equals,
                                 workbook_name))
    fetched_workbook, _ = _server.workbooks.get(
        req_options = req_option
    )
    _server.workbooks.populate_views(fetched_workbook[0])
    # _server.workbooks.populate_preview_image(fetched_workbook[0])
    return fetched_workbook[0].views

def download_zip(zip_buffer, download_filename):        
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(zip_buffer.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(zip_buffer).decode()
            
        dl_link = f"""
                    <html>
                    <head>
                    <title>Start Auto Download file</title>
                    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
                    <script>
                    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
                    </script>
                    </head>
                    </html>
                    """
    
    return dl_link

# @st.cache_data
def create_zip(final_views, filters, include_filter_image, filename):
    zip_buffer = io.BytesIO()
    
    tableau_auth, server = authenticate(
            tokan_name = st.secrets["token_name"], 
            token_value = st.secrets["token_value"], 
            site_id = st.secrets["site_id"], 
            server_url = st.secrets["server_url"]
        )
    with server.auth.sign_in(tableau_auth):
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as my_zip:
            for i,v in final_views.items():
                server.views.populate_image(v, filters[i])
                filter_name = '__'.join(['_'.join(filter_pair).replace(" ","") for filter_pair in filters[i].view_filters])
                view_obj = view_name_patterns[v.name]
                if view_obj:
                    preprocess = True if view_obj.preprocess else False
                    if include_filter_image:
                        no_of_images = view_obj.no_of_images
                    else:
                        no_of_images = view_obj.no_of_images - 1
                    for j in range(no_of_images):
                        image_io = crop_image(v.image,view_obj.crop_coords[j],preprocess,paste_coords=view_obj.paste_coords,img2=view_obj.img2)
                        my_zip.writestr(zinfo_or_arcname=f"{v.name.replace(' ','_')}__{filter_name}__crop_{j+1}.png",data=image_io.getvalue())
                else:
                    image_io = io.BytesIO(v.image)
                    my_zip.writestr(zinfo_or_arcname=f"{v.name.replace(' ','_')}.png",data=image_io.getvalue())
                
    components.html(
        download_zip(zip_buffer.getvalue(), f'{filename}.zip'),
        height=0
    )
    st.session_state.stage = 2
    # return zip_buffer
    
def get_filters(server_url, token_name, token_value, site_name, site_id, api_version="3.22"):
    filter_output = {}
    tableau_server_config = {
            'my_env': {
                    'server': server_url,
                    'api_version': api_version,
                    'personal_access_token_name': token_name,
                    'personal_access_token_secret': token_value,
                    'site_name': site_name,
                    'site_url': site_id
            }
    }
    conn = TableauServerConnection(tableau_server_config, env='my_env')
    conn.sign_in()

    for filter_name, filter_info in filter_dict.items():
        if 'values' in filter_dict[filter_name]:
            filter_values = filter_info['values']
        else:
            view_data_df = get_view_data_dataframe(conn, view_id=filter_info["get_values_from_view_id"])
            filter_values = view_data_df[filter_info["field_name_in_source_view"]].unique().tolist()
        filter_output[filter_name] = [f'{filter_info["filter_field_name"]}:{f}' for f in filter_values]
    
    conn.sign_out()
    return filter_output

def crop_image(image,crop_coords,preprocess,**kwargs):
    p = ImageFile.Parser()
    p.feed(image)
    image = p.close()
    if preprocess:
        image.paste(kwargs['img2'], kwargs['paste_coords'])
    image = image.crop(crop_coords)
    image_io = io.BytesIO()
    image.save(image_io, 'PNG')
    return image_io

# def populate_view(server, selected_view):
#     server.views.populate_image(selected_view)
#     # filename = selected_view.name
#     # try:
#     #     with open(filename, "wb") as f:
#     #         f.write(selected_view.image)
#     # except:
#     #     return 0
#     # return 1

# def populate_preview_image(server, selected_view):
#     server.views.populate_preview_image(selected_view)
    
def set_state(i):
    st.session_state.stage = i
    
def set_workbook(workbook, stage):
    st.session_state.workbook = workbook
    st.session_state.stage = stage
    
def save_pref(pref_name, include_filter_image):
    pref_file = Path("preferences.pkl")
    
    views = [view_d["View"] for view_d in st.session_state.views_df if view_d["Selected"]==True]
    common_filters = st.session_state.selected_filter_value
    iterations = st.session_state.iterations
    iteration_details = st.session_state.iteration_details

    try:
        _ = pref_file.resolve(strict=True)
    except FileNotFoundError:
        # pickle doesn't exist...create new dataframe and pickle
        # df = pd.DataFrame(data=[pref_name, views, common_filters, iterations, iteration_details],\
        #                   columns=['pref_name','views','common_filters','iterations','iteration_details'])
        df = pd.DataFrame.from_dict(
            data = {'1':[pref_name, views, common_filters, iterations, iteration_details, include_filter_image]},\
            columns=['pref_name','views','common_filters','iterations','iteration_details', 'include_filter_image'],\
            orient='index'
        )
        df.to_pickle('preferences.pkl')
    else:
        # pickle exists...load pickle
        df = pd.read_pickle('preferences.pkl')
        new_row = [pref_name, views, common_filters, iterations, iteration_details, include_filter_image]
        df.loc[len(df)] = new_row
        df.to_pickle('preferences.pkl')
        
    print("Preference saved...")
    
def load_pref():
    pref_file = Path("preferences.pkl")
    
    try:
        _ = pref_file.resolve(strict=True)
        
    except FileNotFoundError:
        return []
    
    else:
        pref_names = pd.read_pickle('preferences.pkl')['pref_name'].to_list()
        return pref_names
        
def create_zip_from_pref(pref_name):
    pref_row = pd.read_pickle('preferences.pkl')
    pref_row = pref_row.loc[pref_row.pref_name == pref_name]
    common_filters = pref_row.common_filters.values[0]
    print(f"common_filters: {common_filters}")
    iterations = pref_row.iterations.values[0]
    iteration_details = pref_row.iteration_details.values[0]
    include_filter_image = pref_row.include_filter_image.values[0]
    final_views = {}
    image_request_objects = {}
    
    view_names = pref_row.views.values[0]
    views = [v for v in st.session_state.views if v.name in view_names]
    for v in views:
        view_obj = view_name_patterns[v.name]
        v_iteration = iterations[v.name]
        view_iteration_filters = iteration_details[v.name]
        print(f"view_iteration_filters: {view_iteration_filters}")
        
        for i in range(1,v_iteration+1):
            image_request_object = TSC.ImageRequestOptions()
            if i in view_iteration_filters:
                current_iteration_filters = view_iteration_filters[i]
            
            # COMMON FILTERS
            for _,cf in common_filters.items():
                if cf is not None:
                    if view_obj.exclude_common_filters and cf.split(':')[0] in view_obj.exclude_common_filters:
                        continue
                    else:
                        print(f"Filter: {cf.split(':')[0]},{cf.split(':')[1]}")
                        image_request_object.vf(cf.split(':')[0],cf.split(':')[1])  
                
            # ITERATION SPECIFIC FILTERS
            if current_iteration_filters:
                for i_f in current_iteration_filters: # add iteration-specific filters
                    print(f"Filter: {i_f}")
                    image_request_object.vf(i_f.split(",")[0],i_f.split(",")[1]) 
                
            final_views[len(final_views)+1] = v 
            image_request_objects[len(image_request_objects)+1] = image_request_object
    filename = "" 
    for i,v in common_filters.items():
        if v is not None:
            filename += v.split(":")[1].replace(" ","_")+"__"
    filename = filename[:-2]
    create_zip(final_views, image_request_objects, include_filter_image, filename)
               
# def downloaded_successfully(i):
#     st.success('Image downloaded successfully', icon="✅")
#     set_state(i)

# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.next = None
        
        
# class LinkedList:
#     def __init__(self):
#         self.head = None
#         self.current_node = None
        
#     def __str__(self):
#         if self.head:
#             current = self.head
#             while current.next:
#                 print(current.data, end=" ---> ")
#                 current = current.next
#         else:
#             print("The linked list is empty")
        
#     def insert(self, data):
#         newNode = Node(data)
#         if self.head:
#             current = self.head
#             while current.next:
#                 current = current.next
#             current.next = newNode
#         else:
#             self.head = newNode
            
#     def attach_ends(self):
#         if self.head:
#             current = self.head
#             while current.next:
#                 current = current.next
#             current.next = self.head
#         else:
#             return