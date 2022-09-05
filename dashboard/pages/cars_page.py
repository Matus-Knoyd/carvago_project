import datetime as dt
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from libs.help_functions import (
    get_available_makes,
    get_make_distinct,
    get_model_distinct,
    get_model_min_max_model_mileage,
    get_model_min_max_price,
    get_model_features,
    get_summary_stats_data,
    get_latest_cars_data,
    get_car_price_history)

from app import app

import logging
logger = logging.getLogger(__name__)

settings = html.Div(children=[
        dcc.Interval(id='car-update-interval', interval=1*3600000),
        html.Div(
            [
                html.Div(dbc.Label("Make:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-make',
                    options=[{'label': 'All Makes', 'value': 'All'}] + [{'label': p, 'value': p} for p in get_available_makes()],
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select a make",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Model:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-model',
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select a model",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Color:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-color',
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select a color",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Interior Color:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-interior-color',
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select an interior color",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Power (kW):"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-power',
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select a power",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Drive type:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-drive-type',
                    options=[{'label': 'All drive types', 'value': 'All'}],
                    value=['All'],
                    clearable=False,
                    multi=True,
                    placeholder="Select a drive type",
                    optionHeight=25,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [
                html.Div(dbc.Label("Features:"), className='tab-label'),
                dcc.Dropdown(
                    id='drpdwn-car-feature',
                    value=[],
                    clearable=True,
                    multi=True,
                    placeholder="Select a features",
                    optionHeight=45,
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [   
                html.Div(dbc.Label("Mileage (km):"), className='tab-label'),
                dcc.RangeSlider(
                    id='range-slider-car-mileage',
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [   
                html.Div(dbc.Label("Price (€):"), className='tab-label'),
                dcc.RangeSlider(
                    id='range-slider-car-price',
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ],
            className="custom-dropdown"
        ),
        html.Div(
            [   
                html.Div(dbc.Label("Registration:"), className='tab-label'),
                dcc.DatePickerRange(
                    id='date-picker-car-registration',
                    min_date_allowed=dt.date(2016,1,1),
                    start_date=dt.date(2016,1,1),
                ),
            ],
            className="custom-dropdown"
        ),
    ],
    className='sidebar-settings'
)

main_content = html.Div(
    [
        html.Div(
            [   
                dcc.Graph(id='line-chart-car-market-summary', animate=False)
            ],
            className= 'content-holder'
        ),
        html.Div(
            [   
                dcc.Graph(id='scatter-plot-latest-cars', animate=False)
            ],
            className= 'content-holder'
        ),
        html.Div(
            [   
                dcc.Graph(id='scatter-plot-car-price-history', animate=False)
            ],
            className= 'content-holder'
        ),
    ]
)


@app.callback(
    [Output('drpdwn-car-model', 'options'),
     Output('drpdwn-car-model', 'value')],
    [Input('drpdwn-car-make', 'value')]   
)
def car_update_model_dropdown_options(makes_list):
    dropdown_values = get_make_distinct(makes_list, 'model')
    options = [{'label': 'All Models', 'value': 'All'}] + [{'label': v, 'value': v} for v in dropdown_values]
    value = ['All']

    return options, value

@app.callback(
    [Output('drpdwn-car-color', 'options'),
     Output('drpdwn-car-color', 'value')],
    [Input('drpdwn-car-make', 'value')]   
)
def car_update_color_dropdown_options(makes_list):
    dropdown_values = get_make_distinct(makes_list, 'color')
    options = [{'label': 'All Colors', 'value': 'All'}] + [{'label': v, 'value': v} for v in dropdown_values]
    value = ['All']

    return options, value

@app.callback(
    [Output('drpdwn-car-interior-color', 'options'),
     Output('drpdwn-car-interior-color', 'value')],
    [Input('drpdwn-car-make', 'value')]   
)
def car_update_interior_color_dropdown_options(makes_list):
    dropdown_values = get_make_distinct(makes_list, 'interior_colour')
    options = [{'label': 'All Colors', 'value': 'All'}] + [{'label': v, 'value': v} for v in dropdown_values]
    value = ['All']

    return options, value

@app.callback(
    [Output('drpdwn-car-power', 'options'),
     Output('drpdwn-car-power', 'value')],
    [Input('drpdwn-car-model', 'value')]   
)
def car_update_power_dropdown_options(models_list):
    dropdown_values = get_model_distinct(models_list, 'power')
    options = [{'label': 'All', 'value': 'All'}] + [{'label': v, 'value': v} for v in dropdown_values]
    value = ['All']

    return options, value

@app.callback(
    [Output('drpdwn-car-drive-type', 'options'),
     Output('drpdwn-car-drive-type', 'value')],
    [Input('drpdwn-car-model', 'value')]   
)
def car_update_drive_type_dropdown_options(models_list):
    dropdown_values = get_model_distinct(models_list, 'drive_type')
    options = [{'label': 'All', 'value': 'All'}] + [{'label': v, 'value': v} for v in dropdown_values]
    value = ['All']

    return options, value

@app.callback(
    [Output('drpdwn-car-feature', 'options')],
    [Input('drpdwn-car-model', 'value')]   
)
def car_update_feature_dropdown_options(models_list):
    dropdown_values = get_model_features(models_list)
    options = [{'label': v, 'value': v} for v in dropdown_values]

    return [options]

@app.callback(
    [Output('range-slider-car-mileage', 'min'),
     Output('range-slider-car-mileage', 'max'),
     Output('range-slider-car-mileage', 'value')],
    [Input('drpdwn-car-model', 'value')]   
)
def car_update_mileage_range_slider(models_list):
    min, max = get_model_min_max_model_mileage(models_list)

    return min, max, [min, max]

@app.callback(
    [Output('range-slider-car-price', 'min'),
     Output('range-slider-car-price', 'max'),
     Output('range-slider-car-price', 'value')],
    [Input('drpdwn-car-model', 'value')]   
)
def car_update_mileage_range_slider(models_list):
    min, max = get_model_min_max_price(models_list)

    return min, max, [min, max]


@app.callback(
    [Output('date-picker-car-registration', 'max_date_allowed'),
     Output('date-picker-car-registration', 'end_date')],
    [Input('car-update-interval', 'n_intervals')]   
)
def car_update_car_registration_date_picker(intevral):
    today = dt.date.today()
    
    return today, today

@app.callback(
    Output('line-chart-car-market-summary', 'figure'),
    [   
        Input('drpdwn-car-make', 'value'),
        Input('drpdwn-car-model', 'value'),
        Input('drpdwn-car-color', 'value'),
        Input('drpdwn-car-interior-color', 'value'),
        Input('drpdwn-car-power', 'value'),
        Input('drpdwn-car-drive-type', 'value'),
        Input('drpdwn-car-feature', 'value'),
        Input('range-slider-car-mileage', 'value'),
        Input('range-slider-car-price', 'value'),
        Input('date-picker-car-registration','start_date'),
        Input('date-picker-car-registration', 'end_date')
    ]   
)
def update_car_market_summary_line_chart(make_list, 
        model_list, 
        color_list,
        interior_color_list,
        power_list,
        drive_type_list,
        features_list,
        mileage_range,
        price_range,
        start_date,
        end_date):
    
    df = get_summary_stats_data(
        make_list, 
        model_list, 
        color_list,
        interior_color_list,
        power_list,
        drive_type_list,
        features_list,
        mileage_range,
        price_range,
        start_date,
        end_date)

    col_fig_settings = {
        'average_price': {'line_color': '#17a3dd'},
        'min_price': {'visible': 'legendonly', 'line_color': 'green'},
        'max_price': {'visible': 'legendonly', 'line_color': 'red'},
        'count_offers': {'visible': 'legendonly', 'line_color': 'black'}
    }

    fig = go.Figure()
    for col in df.columns.drop('date'):
        fig.add_trace(
            go.Scatter(
                x=df['date'], 
                y=df[col],
                mode='lines',
                name=col, 
                **col_fig_settings[col]
            )
        )
        
    fig.update_layout(
        title = {
            'text': f'<b>Car market summary</b>',
            'x': 0.5
        },
        xaxis = {
            'title': 'Date',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6'
        },
        yaxis = {
            'title': 'Price (€)',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6'
            },
        margin= {'r': 5},
        plot_bgcolor = '#FFF',
        paper_bgcolor= '#FFF',
    )
    
    return fig

@app.callback(
    Output('scatter-plot-latest-cars', 'figure'),
    [   
        Input('drpdwn-car-make', 'value'),
        Input('drpdwn-car-model', 'value'),
        Input('drpdwn-car-color', 'value'),
        Input('drpdwn-car-interior-color', 'value'),
        Input('drpdwn-car-power', 'value'),
        Input('drpdwn-car-drive-type', 'value'),
        Input('drpdwn-car-feature', 'value'),
        Input('range-slider-car-mileage', 'value'),
        Input('range-slider-car-price', 'value')
    ]   
)
def update_latest_cars_scater_plot(make_list, 
        model_list, 
        color_list,
        interior_color_list,
        power_list,
        drive_type_list,
        features_list,
        mileage_range,
        price_range):
    
    df = get_latest_cars_data(
        make_list, 
        model_list, 
        color_list,
        interior_color_list,
        power_list,
        drive_type_list,
        features_list,
        mileage_range,
        price_range)

    df['customdata'] = df['id']+ ' ' + df['url']

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['mileage'], 
            y=df['price'],
            customdata = df['customdata'],
            mode='markers',
            line_color='#17a3dd',
            hovertemplate =
            '<br><b>Price (€)</b>: %{y:.2f}'+
            '<br><b>Mileage (km)</b>: %{x}<br>'+
            '<b>Registration</b>: %{text}',
            text = df["registration"].astype(str) + 
                '<br><b>Make</b>: ' + df["make"] +
                '<br><b>Model</b>: ' + df["model"] +
                '<br><b>Power (kW)</b>: ' + df["power"].astype(str) +
                '<br><b>Color</b>: ' + df["color"] +
                '<br><b>Interior Color</b>: ' + df["interior_colour"] +
                '<br><b>Body type</b>: ' + df["body"] +
                '<br><b>Drive type</b>: ' + df["drive_type"] +
                '<br><b>Id</b>: ' + df["id"]
        )
    )

    fig.update_layout(
        title = {
            'text': f'<b>Price/Mileage distribution</b>',
            'x': 0.5
        },
        xaxis = {
            'title': 'Mileage (km)',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6'
        },
        yaxis = {
            'title': 'Price (€)',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6'
            },
        margin = {'r': 5},
        plot_bgcolor = '#FFF',
        paper_bgcolor = '#FFF',
    )
    
    return fig

@app.callback(
    Output('scatter-plot-car-price-history', 'figure'),
    Input('scatter-plot-latest-cars', 'clickData'))
def update_car_price_history_line_chart(clickData):
    if clickData is None:
        raise PreventUpdate
        
    car_id, url = clickData['points'][0]['customdata'].split()

    df = get_car_price_history(car_id)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['date'], 
            y=df['price'],
            mode='lines',
            line_color='#17a3dd',
            hovertemplate =
            '<br><b>Price (€)</b>: %{y:.2f}'+
            '<br><b>Date</b>: %{x}<br>'
        )
    )
        
    fig.update_layout(
        title = {
            'text': f'<b>Price history of:<br> <a href={url}>{url}</a></b>',
            'x': 0.5
        },
        xaxis = {
            'title': 'Date',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6'
        },
        yaxis = {
            'title': 'Price (€)',
            'showgrid': True, 
            'gridwidth': 1, 
            'gridcolor': '#F6F6F6',
            },
        margin = {'r': 5},
        plot_bgcolor = '#FFF',
        paper_bgcolor = '#FFF',
    )
    
    return fig
    

