import tableauserverclient as TSC

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