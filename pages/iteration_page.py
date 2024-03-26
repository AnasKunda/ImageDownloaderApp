import streamlit as st
from constants import view_name_patterns, filter_dict
import tableauserverclient as TSC
from utils import create_zip

st.title("Select Iterations")

selected_rows = [view_d["View"] for view_d in st.session_state.views_df if view_d["Selected"]==True]
selected_views = [v for v in st.session_state.views if v.name in selected_rows]
if 'iterations' not in st.session_state:
    st.session_state.iterations = {}

with st.form(key="iteration_page_form", border=False):
    for view in selected_views:
        view_obj = view_name_patterns[view.name]
        container = st.container()
        container.subheader(f"{view.name}")
        # iter_options = [i for i in range(1,max(view_obj.iterations.keys())+1)] if view_obj.iterations else [1]
        iter_options = list(range(1,11))
        iter = container.selectbox(label="No. of Iterations", key=f'{view.name}_iterations',options=iter_options)
        st.session_state.iterations[view.name] = iter
        
    
        # for filter_name, selected_filter_value in st.session_state.selected_filter_value.items():
        #     if (filter_dict[filter_name]['is_required']==True) or ((filter_dict[filter_name].is_required==False) and (selected_filter_value != st.session_state.filter[filter_name][0])):
        #         common_filters.append(selected_filter_value.split(":"))
        #     else:
        #         continue
            
        # image_request_object = TSC.ImageRequestOptions()
        
        # if view_obj.iterations: # If a view has iterations......
        #     for i in range(1, iter+1): # FOR EACH ITERATION......
        #         # selected_filters.append(view_obj.iterations[i][0].split(':'))
        #         iteration_filter = view_obj.iterations[i]
                
        #         if common_filters: # add common filters
        #             for cf in common_filters:
        #                 print(f"Filter: {cf[0]},{cf[1]}")
        #                 image_request_object.vf(cf[0],cf[1])
        #         for i_f in iteration_filter: # add iteration-specific filters
        #             print(f"Filter: {i_f}")
        #             image_request_object.vf(i_f.split(",")[0],i_f.split(",")[1])
                    
        #         final_views[len(final_views)+1] = view
        #         image_request_objects[len(image_request_objects)+1] = image_request_object
                
        # else: # View doesn't have iterations...only add common filters if needed...
        #     if common_filters:
        #         for cf in common_filters:
        #             print(f"Filter: {cf[0]},{cf[1]}")
        #             image_request_object.vf(cf[0],cf[1])
        #         final_views[len(final_views)+1] = view
        #         image_request_objects[len(image_request_objects)+1] = image_request_object
    
    next_button = st.form_submit_button(label="Go To Download Page")

home_button = st.button("Go Back")

if next_button:    
    # create_zip(final_views, image_request_objects)
    st.switch_page("pages/download_page.py")
    
    
if home_button:
    st.switch_page("index.py")  
        
        
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
        