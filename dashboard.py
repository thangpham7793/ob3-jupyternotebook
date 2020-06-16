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


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets=external_stylesheets
app = dash.Dash(__name__)

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
  ],
  className='header-container'
  ),
  html.Hr(),

  #NOTE: month-slider-container
  html.Div([ 
    #NOTE: container for general filters
    #NOTE: association
    html.Div([
      html.P('Association'),
      dcc.Dropdown(
        id='association-filter',
        options=[{'label': i, 'value': i} for i in ['none', 'uniA', 'uniB', 'uniC']],
        value='none',
      )    
    ],
    style={'width': '48%'}
    ),

    html.Div([
      dcc.Slider(
        id='month-slider',
        min=1,
        max=12,
        value=1,
        marks={str(i): str(i) for i in [1,2,3,4,5,6,7,8,9,10,11,12]},
        step=None
      )
    ],
    style={'width': '48%'}
    )
  #NOTE: end of general filter container
  ],
  className='month-slider-container'
  ),
  html.Hr(),
  html.Div([
    html.Div(
        [html.H6(id="total-logins"), html.P("Login Count")],
        id="logins",
        className="stat-container",
    ),
    html.Div(
        [html.H6(id="total-distinct-users"), html.P("Distinct Users")],
        id="users",
        className="stat-container",
    ),
    html.Div(
        [html.H6(id="total-new-docs"), html.P("New Documents")],
        id="documents",
        className="stat-container",
    ),
    html.Div(
        [html.H6(id="total-new-discussions"), html.P("New Discussions")],
        id="discussion",
        className="stat-container",
    ),
    html.Div(
        [html.H6(id="total-data-usage"), html.P("Data Usage")],
        id="data",
        className="stat-container",
    )
  ],
  className="stat-box-container",
),
  #NOTE: container for highlight stats, user_activity_graph and status and association filters
  html.Div([
    #NOTE: highlight boxes
    
    
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

    dcc.Graph(id='user_activity_graph')
  ]),
  
  html.Hr(),
  html.Div([
    #NOTE: course filter
    html.Div(id='data-chart-course-filter-container', 
      children=[
        html.P('Filter by Course'),
        dcc.RadioItems(
          id='data-chart-course-filter',
          value='none',
          labelStyle={'display' : 'inline-block'})
      ],
    ),
    dcc.Graph(id='data_usage_graph')
  ]),

  html.Hr(),
  #NOTE: hidden container for storing jsonified login data
  html.Div(id='jsonified-login-df', style={'display': 'none'}),
  html.Div(id='jsonified-data-usage-df', style={'display' : 'none'})
],
  className='main-container'
)

#NOTE: refetch login data when a new month is picked
@app.callback(
  Output('jsonified-login-df', 'children'),
  [Input('month-slider', 'value')])
def get_and_store_login_data(selected_month):
  rows = session.execute(admin_queries['logins_over_time'], [selected_month])
  df = DataFrame(rows)
  return df.to_json(date_format='iso')

@app.callback(
  Output('jsonified-data-usage-df', 'children'),
  [Input('month-slider', 'value')])
def get_and_store_usage_data(selected_month):
  rows = session.execute(admin_queries['data_usage_by_month'], [selected_month])
  df = DataFrame(rows)
  #print(df.to_json(date_format='iso'))
  return df.to_json(date_format='iso')

#NOTE: reset status filter on month change
@app.callback(
  [Output('login-chart-status-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_login_chart_status_filter(selected_month):
  return ['none']

#NOTE: reset association filter on month change
@app.callback(
  [Output('association-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_login_chart_association_filter(selected_month):
  return ['none']

#NOTE: reset chart type filter on month change
@app.callback(
  [Output('login-chart-chart-type-filter', 'value')], 
  [Input('month-slider', 'value')]
)
def reset_login_chart_chart_type_filter(selected_month):
  return ['bar']

#NOTE: reset frequency filter on month change
@app.callback(
  Output('login-chart-frequency-filter', 'value'),
  [Input('month-slider', 'value')]
)
def reset_login_chart_frequency_filter(selected_month):
  return 'daily'

#NOTE: update login chart on new filter
@app.callback(
  Output('user_activity_graph', 'figure'),
  [Input('jsonified-login-df', 'children'),
   Input('association-filter', 'value'),
   Input('login-chart-status-filter', 'value'),
   Input('login-chart-chart-type-filter', 'value'),
   Input('login-chart-frequency-filter', 'value')],
  [State('month-slider', 'value')]
)
def update_login_chart_on_filter_change(jsonified_login_df, association, status, chart_type, frequency, month):
  if jsonified_login_df is None:
    print("Nothing to show for!")
    raise PreventUpdate
  else:
    df = chart_helper.decode_json_df(jsonified_login_df)
    #print(df.head())
    if (association == 'none'):
      if (status == 'none'):
        fig = chart_helper.make_login_chart(df, month, frequency=frequency[0], chart_type=chart_type)
        #print(fig.data)
        return fig
      else:
        fig = chart_helper.make_login_chart(df, month, status=status, frequency=frequency[0], chart_type=chart_type)
        #print(fig.data)
        return fig
    else:
      if (status == 'none'):
        fig = chart_helper.make_login_chart(df, month, association=association, frequency=frequency[0], chart_type=chart_type)
        #print(fig.data)
        return fig
      else:
        fig = chart_helper.make_login_chart(df, month, association, status, frequency=frequency[0], chart_type=chart_type)
        #print(fig.data)
        return fig

#NOTE: return new options for each association
@app.callback(
  Output('data-chart-course-filter', 'options'),
  [Input('association-filter', 'value')],
  [State('jsonified-data-usage-df', 'children')]
)
def update_data_chart_course_filter(association, jsonified_data_usage_df):
  if (jsonified_data_usage_df is None):
    raise PreventUpdate
  else:
    df = chart_helper.decode_json_df(jsonified_data_usage_df)
    options = chart_helper.get_course_filter_options(df, association)
    return options

#NOTE: display/hide course filter
@app.callback(
  Output('data-chart-course-filter-container', 'style'),
  [Input('association-filter', 'value')],
  [State('jsonified-data-usage-df', 'children')]
)
def update_data_chart_course_filter(association, jsonified_data_usage_df):
  if (jsonified_data_usage_df is None) or (association == 'none'):
    return {'display' : 'none'}
  else:
    return {'display' : 'block'}


#NOTE: set default value for newly created options
@app.callback(
  Output('data-chart-course-filter', 'value'),
  [Input('data-chart-course-filter', 'options')]
)
def set_default_course_filter(options):
  return 'none'

#NOTE: update usage chart on new filter
@app.callback(
  Output('data_usage_graph', 'figure'),
  [Input('jsonified-data-usage-df', 'children'),
   Input('association-filter', 'value'),
   Input('data-chart-course-filter', 'value')],
  [State('month-slider', 'value')]
)
def update_file_usage_chart(jsonified_data_usage_df, association='none', course_id='none', month='none'):
    df = chart_helper.decode_json_df(jsonified_data_usage_df)
    if (course_id == 'none') & (association == 'none'):
        fig = chart_helper.make_aggregate_data_usage_chart(df, association, course_id, month)
        return fig
    elif (association != 'none') & (course_id == 'none'):
        filtered_df = df[df['association'] == association]
        fig = chart_helper.make_data_bar_chart_facetted_by(filtered_df, 'course_id', association, course_id, month)
        return fig
    else:
        filt = (df['association'] == association) & (df['course_id'] == course_id)
        filtered_df = df[filt]
        fig = chart_helper.make_data_bar_chart_facetted_by(filtered_df, 'paper_id', association, course_id, month)
        return fig


#ANCHOR: cbs for stat boxes: total-logins, total-distinct-users, total-data-usage
@app.callback(
  Output('total-logins', 'children'),
  [Input('jsonified-login-df', 'children'), 
   Input('association-filter', 'value')]
)
def display_total_logins_by_association(jsonified_df, association):
  return chart_helper.get_total_logins_by_association(jsonified_df, association)

@app.callback(
  Output('total-distinct-users', 'children'),
  [Input('jsonified-login-df', 'children'), 
   Input('association-filter', 'value')]
)
def display_total_distinct_users_by_association(jsonified_df, association):
  return chart_helper.get_total_distinct_users_by_association(jsonified_df, association)

@app.callback(
  Output('total-data-usage', 'children'),
  [Input('jsonified-data-usage-df', 'children'), 
   Input('association-filter', 'value')]
)
def display_total_distinct_users_by_association(jsonified_df, association):
  return chart_helper.get_total_data_usage_by_association(jsonified_df, association)

#NOTE: run app in debug mode
if __name__ == '__main__':
  app.run_server(debug=True)


#TODO: add highlight boxes + arrange a nice layout
#distinct users remain 10 due to dummy data!
#the stats should correspond to each institution as well (ongoing)
#need to add discussions/documents to data_usage_chart???
#should fix the bar chart to be more clear....

