import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from ydata_profiling import ProfileReport
import sys
import os

st.set_page_config(page_title='Data Profiler', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='expanded')

def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv', '.xlsx'):
        return ext
    else:
        False
        
def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader('Upload a .csv or .xlsx file (not exceeding 10 MB)', type=['csv', 'xlsx'], accept_multiple_files=False)
    if uploaded_file is not None:
        st.write('Modes of Operation')
        minimal = st.checkbox('Do you want to display a minimal report?')
        display_mode = st.radio('Select Display Mode', 
                                options=('Primary', 'Dark', 'Orange'))
        
        if display_mode == 'Dark':
            theme = 'flatly'
            primary_colors = ['black']
        elif display_mode == 'Orange':
            theme = 'united'
            primary_colors = ['orange']
        else:
            theme = None
            primary_colors = ['blue']
    
if uploaded_file is not None:
    # validate extension
    ext = validate_file(uploaded_file)
    
    # Load .csv file
    if ext:
        file_size = get_filesize(uploaded_file)
        
        if file_size <= 10:        
            if ext == '.csv':
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet', sheet_tuple)
                df = xl_file.parse(sheet_name)
        
            # Generate report
            with st.spinner('Generating Report...'):
                pr = ProfileReport(df, minimal=minimal,
                                html={'style': {'theme': theme,
                                                'primary_colors': primary_colors}})
                
            components.html(pr.to_html(), height=1000, scrolling=True)
        else:
            st.error('File size exceeds the limit of 10 MB! Your file size is {:.2f} MB'.format(file_size))
    else:
        st.error('Please only upload an .csv or .xlsx file!')
else:
    st.title('Data Profiler')
    st.info('Upload your file using the left side bar to generate a data profiling report.')