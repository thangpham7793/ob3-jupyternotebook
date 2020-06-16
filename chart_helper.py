import plotly.express as px
import pandas as pd
import datetime
from string import Template
from pandas import DataFrame
import json

#dict for month conversion
month_dict = {
  '1': 'January',
  '2': 'February',
  '3': 'March',
  '4': 'April',
  '5': 'May',
  '6': 'June',
  '7': 'July',
  '8': 'August',
  '9': 'September',
  '10': 'October',
  '11': 'November',
  '12': 'December'
}



def quick_sunburst (df, maxdepth=-1):
    columns_list = list(df.columns) 
    return px.sunburst(df, path=columns_list[0:-1], 
                           values=columns_list[-1], 
                           maxdepth=maxdepth)

def decode_json_df(jsonified_df):
    return DataFrame.from_dict(json.loads(jsonified_df))

def filter_count_by_name(df, name):
    filt = (df['author_full_name'] == name)
    filtered_data = df[filt].groupby('type').count().reset_index() #reset_index() restores the type col
    title = 'Contributions Of ' + name
    return px.bar(filtered_data,
                    x='type',
                    y='author_full_name',
                    labels = {'author_full_name': name},
                    title= title,
                    width=900)


def filters_for_login_chart(df, association=None, status=None):
  df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))
  if (association is None) & (status is None):
    return df
  elif (association != None) & (status == None):
    return df[df['association'] == association]
  elif (association != None) & (status != None):
    return df[(df['association'] == association) & (df['status'] == status)]
  else: 
    return df[(df['status'] == status)]


def uppercase_first_letter_in_title(title):
  right_stripped_title = title.rstrip()
  fixed_title = ''
  for w in right_stripped_title.split(' '):
    fixed_title += w[0].upper() + w[1:] + ' '
  return fixed_title


  
def make_login_chart_title(month, association=None, status=None):
  title_template = Template('${association}${status}Logins in $month')
  month=str(month)
  if (association is None) & (status is None):
    title = title_template.substitute(association='', status='', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  elif (association != None) & (status == None):
    title = title_template.substitute(association=association + ' ', status='', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  elif (association != None) & (status != None):
    title = title_template.substitute(association=association + ' ', status=status + ' ', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  else: 
    title = title_template.substitute(association='', status=status + ' ', month=month_dict[month])
    return uppercase_first_letter_in_title(title)

def make_login_chart(df, month=None, association=None, status=None, frequency='d', chart_type='bar'):
  data = filters_for_login_chart(df, association, status)
  
  total_logins_by_frequency = data.set_index('date').resample(frequency).count().reset_index()

  total_logins_by_frequency = total_logins_by_frequency.rename(columns = {'status' : 'number of logins'})
  
  title = make_login_chart_title(month, association, status)

  if chart_type == 'bar':
      fig = px.bar(total_logins_by_frequency, 
              x = 'date', 
              y = 'number of logins', 
              color='number of logins', 
              color_continuous_scale='teal',
              color_continuous_midpoint=total_logins_by_frequency['number of logins'].median(),
              range_color=[0, total_logins_by_frequency['number of logins'].max()],
              title=title)
      fig.update_xaxes(rangeslider_visible=True)
      return fig
  elif chart_type == 'scatter':
      fig = px.scatter(total_logins_by_frequency, 
              x = 'date', 
              y = 'number of logins', 
              color='number of logins', 
              color_continuous_scale='teal',
              color_continuous_midpoint=total_logins_by_frequency['number of logins'].median(),
              range_color=[0, total_logins_by_frequency['number of logins'].max()],
              title=title)
      fig.update_xaxes(rangeslider_visible=True)
      return fig
  elif chart_type == 'line':
      fig = px.line(total_logins_by_frequency, 
              x = 'date', 
              y = 'number of logins', 
              title=title)
      fig.update_xaxes(rangeslider_visible=True)
      return fig

def make_data_usage_chart_title(association, course_id, month):
  title_template = Template('${association}${course_id}Data Usage in $month ${category}')
  month=str(month)
  if (association == 'none') & (course_id == 'none'):
    title = title_template.substitute(association='', course_id='', category='by institution', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  elif (association != 'none') & (course_id == 'none'):
    title = title_template.substitute(association=association + ' ', course_id='', category='by course', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  elif (association != 'none') & (course_id != 'none'):
    title = title_template.substitute(association=association + ' ', course_id=course_id + ' ', category='by paper', month=month_dict[month])
    return uppercase_first_letter_in_title(title)
  else: 
    title = title_template.substitute(association='', category='by paper', month=month_dict[month])
    return uppercase_first_letter_in_title(title)

def make_aggregate_data_usage_chart(df, association=None, course_id=None, month=None):
  title = make_data_usage_chart_title(association, course_id, month)
  aggregate_df = df.groupby(['association', 'course_id', 'type']).sum().reset_index()
  fig = px.bar(aggregate_df,
      x='association', y='size_in_mb',
      color='type',
      facet_row='association', barmode='group',
      hover_name='course_id', 
      labels={'size_in_mb' : 'Size in MB'},
      title=title)
  return fig

def make_data_bar_chart_facetted_by(df, colname, association=None, course_id=None, month=None):
  title = make_data_usage_chart_title(association, course_id, month)
  fig = px.bar(df, 
          x=colname, y='size_in_mb',
          color='type',
          color_discrete_sequence=['blue', 'orange', 'green', 'red'],
          hover_name='type', 
          hover_data = {'paper_id' : False, 'type' : False, 'course_id' : False},
          barmode='group', 
          labels={'size_in_mb': 'Size in MB'}, 
          facet_row=colname,
          title=title)
  return fig

def get_course_filter_options(df, association):
  filtered_df = df[df['association'] == association]
  unique_vals = filtered_df['course_id'].unique()
  options = [{'label': i, 'value': i} for i in unique_vals]
  options = [{'label': 'none', 'value' : 'none'}] + options
  return options

#ANCHOR: helpers for stat boxes

#NOTE: return filtered df for login stat boxes
def filter_data_by_association(df, association='none'):
    if (association == 'none'): 
        return df
    else:
        return df[df['association'] == association]

def get_total_logins_by_association(jsonified_df, association):
  df = decode_json_df(jsonified_df)
  filtered_df = filter_data_by_association(df, association)
  total_logins = len(filtered_df)
  return total_logins

def get_total_distinct_users_by_association(jsonified_df, association):
  df = decode_json_df(jsonified_df)
  filtered_df = filter_data_by_association(df, association)
  total_distinct_users = len(filtered_df['user_id'].unique())
  return total_distinct_users
  
def get_total_data_usage_by_association(jsonified_df, association):
  df = decode_json_df(jsonified_df)
  filtered_df = filter_data_by_association(df, association)
  total_data_usage = round(filtered_df['size_in_mb'].sum(), 2)
  return str(total_data_usage) + " MB"
