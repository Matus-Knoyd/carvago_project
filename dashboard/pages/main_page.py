import base64
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output

from pages.cars_page import settings as cars_page_tab_settings
from pages.cars_page import main_content as cars_page_main_content

from app import app

navbar = dbc.Navbar(
    [   
        html.Div(id='hidden-div', style={'display': 'none'}),
        dcc.Interval(id='interval-update-data', interval=600*1000), # interval 600*10000 = 10min
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 html.A(
        #                     html.Img(src='data:image/png;base64,{}'.format(
        #                             base64.b64encode(open('assets/lighthouse_logo.png', 'rb').read()).decode()), 
        #                             height="35px", style = {'margin': '10px'}),
        #                     href="https://www.lighthouselabs.ca/"
        #                 )
        #             ],
        #         ),
        #     ],
        #     align="center",
        # ),
    ],
    className='navbar'
)

sidebar_menu = html.Div(
    [   
        html.Div(
            [
                html.Div(
                    [   
                        html.I(
                            id='tab-cars', 
                            title='Cars',
                            n_clicks=0, 
                            className="fas fa-car custom-tab", 
                        )
                    ],
                    className='tab-icon-holder'
                ),
            ],
            className = 'sidebar-menu'
        ),
    ]
)

tabs_settings = html.Div(
    [
        html.Div(id='tabs-content-settings')
    ], 
    className='tabs-settings'
)

layout = html.Div(
    [   
        html.Div(dbc.Row(dbc.Col(navbar))),
        html.Div(dbc.Row(
                    [   
                        dbc.Col(sidebar_menu,className='sidebar',width='auto'),
                        dbc.Col(tabs_settings, className='sidebar sidebar-shadow',width='auto'),
                        dbc.Col(id='main-content',className = 'main-content')
                    ],
                    className='main-window'
            )
        ),
    ]
)

def callback_last_triggered():
    called = [p['prop_id'].split('.')[0] for p in callback_context.triggered]
    return called[0]

@app.callback([Output('tabs-content-settings', 'children'),
               Output('main-content', 'children')],
              [Input('tab-cars', 'n_clicks')])
def render_tabs_settings(cars_tab_clicks):
    called = callback_last_triggered()

    return cars_page_tab_settings, cars_page_main_content
    
@app.callback([Output('tab-cars', 'style')],
              [Input('tab-cars', 'n_clicks')])
def change_tab_icons_styles(cars_tab_clicks):
    called = callback_last_triggered()
    active_style = {'color': '#17a3dd'}
    inactive_style = {'color': '#8B8B8B'}

    return [active_style]
