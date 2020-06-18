#Dash-dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
  #NOTE: header div
  html.Div([
    #NOTE: company logo
    html.Div([
      html.Img(src='assets/statistics.svg', className='logo')
    ],
    className='logo-container'
    ),
    #NOTE: title
    html.Div([
      html.H1('OB3 Admin Dashboard')
    ],
    className='title-container'
    ),
    #NOTE: external link
    html.Div([
      html.A('External link', href='#')
    ],
    className='link-container'
    )
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
    ]
    ),

    html.Div([
      html.P('Month'),
      dcc.Slider(
        id='month-slider',
        min=1,
        max=12,
        value=1,
        marks={str(i): str(i) for i in [1,2,3,4,5,6,7,8,9,10,11,12]},
        step=None
      )
    ]
    )
  #NOTE: end of general filter container
  ],
  className='general-filter-container'
  ),
  html.Hr(),
  html.Div([
  
    html.Div(
        [html.H6(id="total-distinct-users"), html.P("Distinct Users")],
        id="distinct-users",
        className="stat-container",
    ),
    
    html.Div(
        [html.H6(id="total-logins"), html.P("Login Sessions")],
        id="logins",
        className="stat-container",
    ),

    html.Div(
        [html.H6(id="total-new-users-sessions"), html.P("Sessions By New Users")],
        id="new-users",
        className="stat-container",
    ),

    html.Div(
        [html.H6(id="total-data-usage"), html.P("Data Usage")],
        id="data",
        className="stat-container",
    ),

    html.Div(
        [html.H6(id="total-new-resources"), html.P("New Resources")],
        id="resources",
        className="stat-container",
    )
  ],
  className="stat-box-container",
),
  #NOTE: container for user-activity graph and filters
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
  ]
  ),
  
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
  ]
  ),

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
#distinct users remain 10 due to dummy data!
#the stats should correspond to each institution as well (ongoing)
#need to add discussions/documents to data_usage_chart???
#should fix the bar chart to be more clear....

