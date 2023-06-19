import streamlit as st
import re
import pandas as pd
from pathlib import Path
import Backend as be

st.set_page_config(page_title="IEIS - Machine", page_icon="🖼️")
st.title("Machine ⚙️")

BASE_DIR = Path(__file__).resolve().parent.parent
image_folder_happy = BASE_DIR / "dataset/happy/"
image_folder_sad = BASE_DIR / "dataset/sad/"

txt = st.text_area('Enter k values separated by commas', placeholder='3, 5, 7, 9')
valid_characters = "0123456789, \n"

def case_folding(sentence):
    sentence = sentence.replace('\n', ' ')
    sentence = sentence.replace(',', ' ')
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence

def real_k():
    st.subheader('Percentage of Accuracy Testing')
    k = [3, 5, 7, 9]
    accuracy = [be.knn_score(int(n)) for n in k]
    chart_data = pd.DataFrame(
        {'k': [float(val) for val in accuracy]},
        index=k
    )
    st.area_chart(chart_data)

def fixed_data():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Data Percentage')
        positive_images = list(image_folder_happy.glob("*"))
        negative_images = list(image_folder_sad.glob("*"))
        chart_data = pd.DataFrame(
            {'happy': [len(positive_images)],
            'sad': [len(negative_images)]},
            index=['sentiment']
        )
        st.bar_chart(chart_data)
    with col2:
        st.subheader('Data Info')
        data = be.get_data()
        data_df1 = pd.DataFrame({"train": [data[0]]})
        data_df2 = pd.DataFrame({"test": [data[1]]})
        st.data_editor(
            data_df1,
            column_config={
                "train": st.column_config.NumberColumn(
                    label="Training Data",
                    help="The data of the training",
                    width="medium",
                )
            },
            hide_index=True,
        )
        st.data_editor(
            data_df2,
            column_config={
                "test": st.column_config.NumberColumn(
                    label="Testing Data",
                    help="The data of the testing",
                    width="medium",
                ),
            },
            hide_index=True,
        )

if txt == '':
    submit = st.button('Submit', disabled=True)
    real_k()
    fixed_data()
else:
    submit = st.button('Submit', disabled=False)
    if submit:
        st.subheader('Percentage of Accuracy Testing')
        k = case_folding(txt).split(' ')
        accuracy = [be.knn_score(int(n)) for n in case_folding(txt).split(' ')]
        chart_data = pd.DataFrame(
            {'k': [float(val) for val in accuracy]},
            index=[int(num) for num in k]
        )
        st.area_chart(chart_data)
        fixed_data()