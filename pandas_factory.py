# NOTE: source here: 
# https://stackoverflow.com/questions/42420260/how-to-convert-cassandra-map-to-pandas-dataframe
# https://stackoverflow.com/questions/41247345/python-read-cassandra-data-into-pandas/41484806#41484806

from cassandra.util import OrderedMapSerializedKey
import pandas as pd

def pandas_factory(colnames, rows):

    # Convert tuple items of 'rows' into list (elements of tuples cannot be replaced)
    rows = [list(i) for i in rows]

    # Convert only 'OrderedMapSerializedKey' type list elements into dict
    for idx_row, i_row in enumerate(rows):

        for idx_value, i_value in enumerate(i_row):

            if type(i_value) is OrderedMapSerializedKey:

                rows[idx_row][idx_value] = dict(rows[idx_row][idx_value])

    return pd.DataFrame(rows, columns=colnames)