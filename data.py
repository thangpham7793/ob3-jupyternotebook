import datetime
import pandas as pd
from queries import make_queries_get_df
import asyncio

async def set_time_index(df):
  df['date'] = df['date'].apply(lambda x: pd.to_datetime(x.date()))
  return df
#login_by_january_df['date'] = login_by_january_df['date'].apply(lambda x: pd.to_datetime(x.date()))

async def get_january_login_data():
  login_by_january_df = await make_queries_get_df('''
  SELECT status, association, todate(login_time) as date
  FROM user_by_activity 
  WHERE month = 1
  AND login_time >= '2020-01-01T00:00:00'
  AND login_time < '2020-02-01T00:00:00';
  ''')
  login_by_january_df = await set_time_index(login_by_january_df)
  return login_by_january_df


