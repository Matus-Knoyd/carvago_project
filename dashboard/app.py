import dash
import dash_auth
import dash_bootstrap_components as dbc

from auth.logins.valid_users import VALID_USERNAME_PASSWORD_PAIRS
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

# load env variables
load_dotenv()

# app settings
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                external_stylesheets = [dbc.themes.BOOTSTRAP,
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'])
app.title = 'Car Market Analyzer' 

# auth settings
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)




