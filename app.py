#Dash-dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#helper-functions
import chart_helper

#Cassandra-related
from cloud import session
from queries_dict import admin_queries

#other Python libs
from pandas import DataFrame
import json
import datetime

#helper functions
def decode_json_df(jsonified_df):
    return DataFrame.from_dict(json.loads(jsonified_df))

app = dash.Dash(__name__)

app.layout = html.Div(
  [
  #NOTE: header div
  html.Div([
    #NOTE: company logo
    html.Div([
      html.H2('logo here')
    ]),
    #NOTE: title
    html.Div([
      html.H1('Admin Dashboard')
    ]),
    #NOTE: external link
    html.Div([html.H2('External link')])
  ],
  className='header-container'
  ),
  html.Hr(),

  html.Div([ 
    #NOTE: container for general filters
    html.Div([
      dcc.Slider(
        id='month-slider',
        min=1,
        max=4,
        value=1,
        marks={str(i): str(i) for i in [1,2,3,4,5,6,7,8,9,10,11,12]},
        step=None
      )
    ],
    style={'width': '48%'}
    )
  #NOTE: end of general filter container
  ]),
  html.Hr(),
  #NOTE: highlight boxes
  html.Div([
      html.Div(
          [html.H6(id="loginsText"), html.P("Login Count")],
          id="logins",
          className="mini_container",
      ),
      html.Div(
          [html.H6(id="usersText"), html.P("Distinct Users")],
          id="users",
          className="mini_container",
      ),
      html.Div(
          [html.H6(id="documentsText"), html.P("New Documents")],
          id="documents",
          className="mini_container",
      ),
      html.Div(
          [html.H6(id="discussionText"), html.P("New Discussions")],
          id="discussion",
          className="mini_container",
      ),
      html.Div(
          [html.H6(id="dataText"), html.P("Data Usage")],
          id="data",
          className="mini_container",
      )
    ],
    id="info-container",
    className="stat-container",
  ),
  #NOTE: container for user_activity_graph and its filters
  html.Div([
    html.Div([
        #NOTE: status
      html.Div([
        html.P('Status'),
        dcc.RadioItems(
          id='login-chart-status-filter',
          options=[{'label': i, 'value': i} for i in ['none', 'student', 'teacher', 'alumnus']],
          value='none',
          labelStyle={'display' : 'inline-block'}
        )
      ],
      style={'width': '48%'}
      ),
      #NOTE: association
      html.Div([
        html.P('Association'),
        dcc.Dropdown(
          id='login-chart-association-filter',
          options=[{'label': i, 'value': i} for i in ['none', 'uniA', 'uniB', 'uniC']],
          value='none',
        )    
      ],
      style={'width': '48%'}
      ),

      html.Div([
        html.P('Frequency'),
        dcc.RadioItems(
          id='login-chart-frequency-filter',
          options=[{'label': i, 'value': i} for i in ['daily', 'weekly']],
          value='daily',
          labelStyle={'display' : 'inline-block'}
        )
      ],
      style={'width': '48%'}
      ),
      
      html.Div([
        html.P('Chart Type'),
        dcc.RadioItems(
          id='login-chart-chart-type-filter',
          options=[{'label': i, 'value': i} for i in ['bar', 'line', 'scatter']],
          value='none',
          labelStyle={'display' : 'inline-block'}
        )
      ],
      style={'width': '48%'}
      ),
    ],
    className='login-chart-filter-container'
    ),
    

    html.Div([
       dcc.Graph(id='user_activity_graph')
    ],
    className='login-chart-container'
    )
  ],
  className='login-chart-main-container'
  ),
  
  html.Hr(),
  html.Div([
    #NOTE: association filter
    html.Div([
      html.Div([
      html.P('Association'),
      dcc.Dropdown(
        id='data-chart-association-filter',
        options=[{'label': i, 'value': i} for i in ['none', 'uniA', 'uniB', 'uniC']],
        value='none',
      )    
    ],
    style={'width': '48%'}
    ),

    #NOTE: course filter
    html.Div(id='data-chart-course-filter-container', 
      children=[
        html.P('Filter by Course'),
        dcc.RadioItems(
          id='data-chart-course-filter',
          value='none',
          labelStyle={'display' : 'inline-block'})
      ])
    ],
    className="data-chart-filter-container"
    ),
    
    html.Div([
      dcc.Graph(id='data_usage_graph')
    ])
  ]),

  html.Hr(),
  #NOTE: hidden container for storing jsonified login data
  html.Div(id='jsonified-login-df', style={'display': 'none'}),
  html.Div(id='jsonified-data-usage-df', style={'display' : 'none'})
  ],
  className='main-container'
)

#NOTE: run app in debug mode
if __name__ == '__main__':
  app.run_server(debug=True)


#TODO: add highlight boxes + arrange a nice layout