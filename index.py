import streamlit as st
from utils import *
import logging

def main():
    # set up logging
    logging.basicConfig(filename='logs.log', format='%(message)s', level=logging.INFO)
    # authenticate server
    tableau_auth, server = authenticate(
        tokan_name = st.secrets["token_name"], 
        token_value = st.secrets["token_value"], 
        site_id = st.secrets["site_id"], 
        server_url = st.secrets["server_url"]
    )
    with server.auth.sign_in(tableau_auth):
        logging.info("Authentication Successful")
        
    
    
if __name__ == '__main__':
    main()