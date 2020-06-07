from cloud import session
from pandas_factory import pandas_factory
session.row_factory = pandas_factory

query = '''
SELECT * FROM marked_component_by_user_id
WHERE user_id = '2' 
AND paper_id = 'paperB' 
GROUP BY doc_id;
'''

data = []
rslt = session.execute(query, timeout=None)
df = rslt._current_rows

print(df)