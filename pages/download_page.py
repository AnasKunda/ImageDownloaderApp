import streamlit as st
from constants import view_name_patterns, filter_dict, iteration_filter_dict
import tableauserverclient as TSC
from utils import create_zip, save_pref

st.set_page_config(page_title="Download Images", layout="wide")
st.title("Set Filters & Download")

# Load selected views
selected_rows = [view_d["View"] for view_d in st.session_state.views_df if view_d["Selected"]==True]
selected_views = [v for v in st.session_state.views if v.name in selected_rows]
final_views = {}
image_request_objects = {}
iteration_details = {}

#view_obj is the TableauView object created in constants.py file.
#This view contains info like crop setting, applicable common filters and view-specific filters. 

#view_name_patterns is a dictionary which takes the view's name, and returns the appropriate
#TableauView object.


with st.form(key="download_page_form", border=False):
    for view in selected_views:
        view_obj = view_name_patterns[view.name]
        container = st.container()
        container.subheader(f"{view.name}")
        
        cols = container.columns(len(view_obj.iteration_filters.keys())+1 if view_obj.iteration_filters else 2)
        
        cols[0].markdown("**Iteration**")
        for i in range(1,st.session_state.iterations[view.name]+1):
            cols[0].selectbox(label=" ", key=f"{view.name}_iter_{i}", options=[i])
        
        # if there are any view specific filters
        if view_obj.iteration_filters:
            for i in range(1, len(cols[1:])+1):
                filter_name = list(view_obj.iteration_filters.keys())[i-1]
                cols[i].markdown(f"**{filter_name}**")
                for j in range(1, st.session_state.iterations[view.name]+1):
                    ''' The options parameter is what user sees as the options.
                        For each view specific filter, the options are loaded from a dictionary created in constants.py.    
                    '''
                    cols[i].selectbox(label=" ",key=f"{view.name}_{filter_name}_iter_{j}", options=iteration_filter_dict[filter_name]["values"], index=None, format_func=lambda x:"(NULL)" if x == False else x, placeholder="All")   
        else:
            cols[1].markdown("**No Additional Filters**")

    # Textbox and button for saving preference
    pref_name = st.text_input(label="Preference Name", value=None, placeholder="Save Preference by Name")
    include_filter_image = st.checkbox(label="Include Filter Image")
    download_button = st.form_submit_button(label="Download Views")
    
if download_button:
    for view in selected_views:
        view_obj = view_name_patterns[view.name]
        common_filters = [] # stores common filters specific to the view
        iteration_details[view.name] = {} # stores view filters specific to the view

        # COMMON FILTERS
        for filter_name, selected_filter_value in st.session_state.selected_filter_value.items():
            if selected_filter_value is not None:
                common_filters.append(selected_filter_value.split(":"))
        
        if view_obj.iteration_filters: # If a view has iteration filters......
            for i in range(1, st.session_state.iterations[view.name]+1): # FOR EACH ITERATION...... 
                current_iteration_filters = [] 
                image_request_object = TSC.ImageRequestOptions() # Tableau server's object to apply filters
                for filter_name in list(view_obj.iteration_filters.keys()):
                    filter_field = view_obj.iteration_filters[filter_name]
                    filter_value = st.session_state[f"{view.name}_{filter_name}_iter_{i}"]
                    if filter_value is None:
                        continue
                    current_iteration_filters.append(f"{filter_field},{filter_value}")
                if common_filters: # add common filters
                    for cf in common_filters:
                        ''' For some view, a common filter might not be applicable.
                            This information is stored in view_obj (TableauView object of that view)
                        '''
                        if view_obj.exclude_common_filters and cf[0] in view_obj.exclude_common_filters:
                            continue
                        else:
                            # print(f"Filter: {cf[0]},{cf[1]}") # for debugging
                            image_request_object.vf(cf[0],cf[1]) # Tableau server's function to apply filter
                for i_f in current_iteration_filters: # add iteration-specific filters
                    # print(f"Filter: {i_f}") # for debugging
                    image_request_object.vf(i_f.split(",")[0],i_f.split(",")[1])
                final_views[len(final_views)+1] = view # this dict will be passed on to download images
                iteration_details[view.name][i] = current_iteration_filters # iteration_details dict is used when we want to save current setting as a preference.
                image_request_objects[len(image_request_objects)+1] = image_request_object # the image request object is created for each iteration, and passed on to image downloading function.
                    
        else: # View doesn't have iterations...only add common filters if needed...
            image_request_object = TSC.ImageRequestOptions()
            if common_filters:
                for cf in common_filters:
                    if view_obj.exclude_common_filters and cf[0] in view_obj.exclude_common_filters:
                        continue
                    else:
                        print(f"Filter: {cf[0]},{cf[1]}")
                        image_request_object.vf(cf[0],cf[1])
                                            
                final_views[len(final_views)+1] = view
                iteration_details[view.name][1] = []
                image_request_objects[len(image_request_objects)+1] = image_request_object
 
    # if user has entered a preference name in textbox, then save current setting with that preference name
    if pref_name:
        st.session_state.iteration_details = iteration_details
        print(f"st.session_state.iterations: {st.session_state.iterations}")
        save_pref(pref_name, include_filter_image)
    # create a filename based on common filters
    filename = ""
    for filter_pair in common_filters:
        filename += filter_pair[1].replace(" ","_")+"__"
    filename = filename[:-2]
    # download zip file containing all images
    create_zip(final_views, image_request_objects, include_filter_image, filename)
    
back_button = st.button(label="Go Back", key="back_button")
home_button = st.button(label="Go Home", key="home_button")

if back_button:
    st.switch_page("./pages/iteration_page.py")
    
if home_button:
    st.switch_page("./pages/views_page.py")
        
    