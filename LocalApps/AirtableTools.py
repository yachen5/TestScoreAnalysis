import pandas as pd
import streamlit as st
from pyairtable import Api

try:
    api = Api(st.secrets["AIRTABLE_API_KEY"])
except FileNotFoundError:
    import config2 as cf

    api = Api(cf.AIRTABLE_API_KEY)


def write_data(adf, base_name):
    table = api.table(base_name, 'Results')
    for i, row in adf.iterrows():
        record = dict(row)
        table.create(record)


def batch_write_data(adf, base_name):
    table = api.table(base_name, 'Results')
    df_to_dict = adf.to_dict(orient='records')
    # st.write(df_to_json)
    # data = json.dumps(df_to_json)
    table.batch_create(df_to_dict)


def read_data(base_name):
    table = api.table(base_name, 'Results')
    data = table.all()
    df = pd.DataFrame.from_records((r['fields'] for r in data))
    # df = pd.DataFrame(data)
    st.dataframe(df)
    return df


def delete_data(base_name):
    table = api.table(base_name, 'Results')
    aaa = table.all()
    dff = pd.DataFrame(aaa)

    try:
        idlist = list(dff['id'].unique())
        table.batch_delete(idlist)
    except KeyError:
        pass
