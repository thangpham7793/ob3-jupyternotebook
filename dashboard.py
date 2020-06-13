#Dash-dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#helper-functions
from chart_helper import make_login_chart

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
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
  ]),
  html.Hr(),

  #NOTE: a container for the 2 smaller filter containers
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

  #NOTE: container for highlight stats, user_activity_graph and status and association filters
  html.Div([
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
      className="row container-display",
    ),
    
    #NOTE: status
    html.Div([
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
      dcc.Dropdown(
        id='login-chart-association-filter',
        options=[{'label': i, 'value': i} for i in ['none', 'independent', 'uniA', 'uniB', 'uniC']],
        value='none',
      )    
    ],
    style={'width': '48%'}
    ),

    html.Div([
      dcc.RadioItems(
        id='login-chart-chart-type-filter',
        options=[{'label': i, 'value': i} for i in ['bar', 'line', 'scatter']],
        value='none',
        labelStyle={'display' : 'inline-block'}
      )
    ],
    style={'width': '48%'}
    ),
    html.Div([
       dcc.Graph(id='user_activity_graph')
    ])
  ]),
  
  html.Hr(),
  html.Div([
    #NOTE: association filter
    html.Div([
      dcc.Dropdown(
        id='data-chart-association-filter',
        options=[{'label': i, 'value': i} for i in ['none', 'uniA', 'uniB', 'uniC']],
        value='none',
      )    
    ],
    style={'width': '48%'}
    ),

    #NOTE: course filter
    html.Div([
      html.P('Filter by Course'),
      dcc.RadioItems(
        id='data-chart-course-filter',
        options=[{'label': i, 'value': i} for i in ['none','courseA', 'courseB', 'courseC']],
        value='none',
        labelStyle={'display' : 'inline-block'}
      )
    ]),
    html.Div([
      html.H3('file_usage_chart here!'),
      dcc.Graph(id='data_usage_graph')
    ])
  ]),

  html.Hr(),
  html.Div([
    html.Div([
      html.H3('Filter for 3rd chart')
    ]),
    html.Div([
      html.H3('3rd chart here!'),
      dcc.Graph(id='3rd chart')
    ])
  ]),

  html.Hr(),
  #NOTE: hidden container for storing jsonified login data
  html.Div(id='jsonified-login-df', style={'display': 'none'}),
  html.Div(id='jsonified-data-usage-df', style={'display' : 'none'})
])

#NOTE: refetch login data when a new month is picked
@app.callback(
  Output('jsonified-login-df', 'children'),
  [Input('month-slider', 'value')])
def clean_login_data(selected_month):
  rows = session.execute(admin_queries['logins_over_time'], [selected_month])
  df = DataFrame(rows)
  return df.to_json(date_format='iso')

@app.callback(
  Output('jsonified-data-usage-df', 'children'),
  [Input('month-slider', 'value')])
def clean_usage_data(selected_month):
  rows = session.execute(admin_queries['data_usage_by_month'], [selected_month])
  df = DataFrame(rows)
  print(df.head(10))
  return df.to_json(date_format='iso')

#NOTE: reset status filter on month change
@app.callback(
  [Output('login-chart-status-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_association_filter(selected_month):
  return ['none']

#NOTE: reset association filter on month change
@app.callback(
  [Output('login-chart-association-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_association_filter(selected_month):
  return ['none']

#NOTE: reset chart type filter on month change
@app.callback(
  [Output('login-chart-chart-type-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_association_filter(selected_month):
  return ['bar']

#NOTE: update login chart on new filter
@app.callback(
  Output('user_activity_graph', 'figure'),
  [Input('jsonified-login-df', 'children'),
   Input('login-chart-association-filter', 'value'),
   Input('login-chart-status-filter', 'value'),
   Input('login-chart-chart-type-filter', 'value')],
  [State('month-slider', 'value')]
)
def update_login_chart_on_filter_change(jsonified_login_df, association, status, chart_type, month):
  if jsonified_login_df is None:
    print("Nothing to show for!")
    raise PreventUpdate
  else:
    df = decode_json_df(jsonified_login_df)
    #print(df.head())
    if (association == 'none'):
      if (status == 'none'):
        fig = make_login_chart(df, month, chart_type=chart_type)
        #print(fig.data)
        return fig
      else:
        fig = make_login_chart(df, month, status=status, chart_type=chart_type)
        #print(fig.data)
        return fig
    else:
      if (status == 'none'):
        fig = make_login_chart(df, month, association=association, chart_type=chart_type)
        #print(fig.data)
        return fig
      else:
        fig = make_login_chart(df, month, association, status, chart_type=chart_type)
        #print(fig.data)
        return fig

#NOTE: update usage chart on new filter
@app.callback(
  Output('data_usage_graph', 'figure'),
  [Input('jsonified-data-usage-df', 'children'),
   Input('data-chart-association-filter', 'value'),
   Input('data-chart-course-filter', 'value')],
  [State('month-slider', 'value')]
)
def update_file_usage_chart(jsonified_data_usage_df, association='none', course_id='none', month='none'):
    df = decode_json_df(jsonified_data_usage_df)
    if (association == 'none' & course_id == 'none'):
        fig = chart_helper.make_aggregate_data_usage_chart(df)
        return fig
    else:
        filtered_df = df[df['course_id'] == course_id]
        fig = px.bar(filtered_df, 
                x='course_id', y='size_in_mb',
                color='type',
                color_discrete_sequence=['blue', 'orange', 'green', 'red'],
                hover_name='type', 
                hover_data = {'paper_id' : False, 'type' : False, 'course_id' : False},
                barmode='group', 
                labels={'size_in_mb': 'Size in MB'}, 
                facet_row='paper_id')
        return fig

#NOTE: run app in debug mode
if __name__ == '__main__':
  app.run_server(debug=True)


#TODO: add new_user_chart/query to dashboard/ 
# refactor/test component tables
# modularize each part of the layout/callbacks?
# arrange a nice layout