from cloud import session
from pandas import DataFrame
import pandas as pd

def to_df (rows):
  data = DataFrame(rows)
  return data

def make_queries_get_df (query):
  rows = session.execute(query, timeout=None)
  return to_df(rows)
