#Dash-dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html

month_dict = {
  'January': 1,
 'February': 2,
  'March': 3,
  'April': 4,
  'May': 5,
  'June': 6,
  'July': 7,
  'August': 8,
  'September': 9,
  'October': 10,
  'November': 11,
  'December': 12
}


app = dash.Dash(__name__)

app.layout = html.Div([
  #NOTE: header div
  html.Div([
    #NOTE: company logo
    html.Div([
      html.Img(src='assets/paper.png', className='logo')
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
      html.A('Learn More', href='https://www.ob3.io/', target='_blank')
    ],
    className='link-container'
    )
  ],
  className='header-container'
  ),

  #NOTE: general filter container
  html.Div([ 
    html.Div([
      dcc.Dropdown(
        id='association-filter',
        options=[{'label': i, 'value': i} for i in ['uniA', 'uniB', 'uniC']],
        placeholder='Select Association'
      )    
    ]
    ),

    html.Div([
      dcc.Dropdown(
        id='month-filter',
        options=[{'label': key, 'value': month_dict[key]} for key in month_dict.keys()],
        clearable=False,
        value=1
      )
    ],
    ),
  ],
  className='general-filter-container'
  ),
  

  html.Div([
  
    html.Div(
        [html.H2(id="total-distinct-users"), html.H4("Distinct Users")],
        id="distinct-users",
        className="stat-container",
    ),
    
    html.Div(
        [html.H2(id="total-logins"), html.H4("Login Sessions")],
        id="logins",
        className="stat-container",
    ),

    html.Div(
        [html.H2(id="total-new-users-sessions"), html.H4("Sessions By New Users")],
        id="new-users",
        className="stat-container",
    ),

    html.Div(
        [html.H2(id="total-data-usage"), html.H4("MB Data Usage")],
        id="data",
        className="stat-container",
    ),

    html.Div(
        [html.H2(id="total-new-resources"), html.H4("New Resources")],
        id="resources",
        className="stat-container",
    )
  ],
  className="stat-box-container",
  ),
  
  #NOTE: login-chart-filter-container

  html.Div([
    #NOTE: status
    html.Div([
      dcc.Dropdown(
        id='login-chart-status-filter',
        options=[{'label': i, 'value': i} for i in ['student', 'teacher', 'alumnus']],
        placeholder='Select Status'
      )
    ]),

    html.Div([
      dcc.Dropdown(
        id='login-chart-frequency-filter',
        options=[{'label': i, 'value': i} for i in ['Daily', 'Weekly']],
        value='Daily',
        clearable=False,
      )
    ]),
    
    html.Div([
      dcc.Dropdown(
        id='login-chart-chart-type-filter',
        options=[{'label': i, 'value': i} for i in ['Bar Chart', 'Line Chart', 'Scatter Chart']],
        value='Bar Chart',
        clearable=False,
      )
    ])
  ],
  className='login-chart-filter-container'
  ),
  
  html.Div([
    dcc.Graph(id='user_activity_graph'),
  ],
  className='user-activity-graph-container'),
  
  html.Div([
    #NOTE: course filter
    html.Div(id='data-chart-course-filter-container', 
      children=[
        dcc.Dropdown(
          id='data-chart-course-filter',
          placeholder='Select A Course'
        )
      ])   
  ],
  className='data-chart-filter-container'
  ),
  
  html.Div([
    dcc.Graph(id='data_usage_graph'),
  ],
  className='data-usage-graph-container'),

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

