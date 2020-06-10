from cloud import session
from pandas import DataFrame
import asyncio

# NOTE: execute SELECT * in a particular session on a given table
def select_all_from(table_name, limit = -1):
  query = ''
  if limit != -1:
    query = "SELECT * FROM {} LIMIT {}".format(table_name, limit)
  else:
    query = "SELECT * FROM {}".format(table_name)
  print(query)
  return session.execute(query)
  
def to_df (rows):
  data = DataFrame(rows)
  return data

def select_all_as_df (table_name, limit = -1):
  rows = select_all_from(table_name, limit)
  return to_df(rows)

async def make_queries_get_df (query):
  rows = session.execute(query)
  return to_df(rows)

