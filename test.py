from cloud import session
import json
from chart_helper import make_login_chart
from pandas import DataFrame
import pandas as pd
from queries_dict import admin_queries

def clean_data(selected_month):
  rows = session.execute(admin_queries['logins_over_time'], [selected_month])
  df = DataFrame(rows)
  #NOTE: 
  return df.to_json(date_format='iso')
json_df = clean_data(1)
original_df = DataFrame.from_dict(json.loads(json_df))
fig = make_login_chart(original_df, 'Testing JSON back and forth')
fig.show()