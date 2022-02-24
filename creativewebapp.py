import streamlit as st
from creativepull import creativepull
import os
import pandas as pd
from pathlib import Path

os.chdir(str(os.path.join(Path.home(), 'Downloads')))

# title of app
st.title('Creative Status')

# Container 1
with st.container():
    uploaded_file = st.file_uploader(label='Upload CSV', type='csv')
    bundle_id = st.text_input('What is the bundle ID?')
    st.button('Download', on_click=lambda : download())

global df
if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except:
            pass

try:
    st.write(df)
except:
    pass



def download():
    try:
        df_live = creativepull(bundle_id)
        dfmerge = pd.merge(df, df_live, on=['Campaign ID', 'Creative ID'], how='left')
        dfmerge.loc[dfmerge['Status'] > 0, 'Status'] = 'Live'
        dfmerge.fillna('Paused', inplace=True)  
        try:
            dfmerge.to_csv(uploaded_file.name.replace('.csv', '_status.csv'), index=False)
            st.success(f'{uploaded_file.name} Downloaded')
        except:
            st.error('Unable To Download')
    except:
        st.warning('An Error Occured: Please contact SE')