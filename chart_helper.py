import plotly.express as px
import pandas as pd
import datetime


def quick_sunburst (df, maxdepth=-1):
    columns_list = list(df.columns) 
    return px.sunburst(df, path=columns_list[0:-1], 
                           values=columns_list[-1], 
                           maxdepth=maxdepth)

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
    if (association is None) & (status is None):
        return None
    elif (association != None) & (status == None):
        return df['association'] == association
    elif (association != None) & (status != None):
        return (df['association'] == association) & (df['status'] == status)
    else: 
        return (df['status'] == status)

def make_login_chart(df, title, association=None, status=None, frequency='d', chart_type='bar'):
    filters = filters_for_login_chart(df, association, status)
    data = []
    if filters is None:
      data = df
    else:
      data = df[filters]
    data['date'] = data['date'].apply(lambda x: pd.to_datetime(x.date()))
    total_logins_by_frequency = data.set_index('date').resample(frequency).count().reset_index()
    total_logins_by_frequency = total_logins_by_frequency.rename(columns = {'status' : 'number of logins'})

    if chart_type == 'bar':
        return px.bar(total_logins_by_frequency, 
                x = 'date', 
                y = 'number of logins', 
                color='number of logins', 
                color_continuous_scale='teal',
                color_continuous_midpoint=total_logins_by_frequency['number of logins'].median(),
                range_color=[0, total_logins_by_frequency['number of logins'].max()],
                title=title)
    elif chart_type == 'scatter':
        return px.scatter(total_logins_by_frequency, 
                x = 'date', 
                y = 'number of logins', 
                color='number of logins', 
                color_continuous_scale='teal',
                color_continuous_midpoint=total_logins_by_frequency['number of logins'].median(),
                range_color=[0, total_logins_by_frequency['number of logins'].max()],
                title=title)
    elif chart_type == 'line':
        return px.line(total_logins_by_frequency, 
                x = 'date', 
                y = 'number of logins', 
                title=title)


