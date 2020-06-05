import plotly.express as px

def quick_sunburst (df):
    columns_list = list(df.columns) 
    return px.sunburst(df, path=columns_list[0:-1], values=columns_list[-1])

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