import streamlit as st
import re
import os
import joblib
import pandas as pd

st.set_page_config(page_title="IEIS - Machine", page_icon="🖼️")
st.title("Machine ⚙️")

def real_k():
    st.subheader('Percentage of Accuracy Testing')
    k = [3, 5, 7, 9]
    acc1 = joblib.load("models/acc_3")
    acc2 = joblib.load("models/acc_5")
    acc3 = joblib.load("models/acc_7")
    acc4 = joblib.load("models/acc_9")
    accuracy = [acc1, acc2, acc3, acc4]
    chart_data = pd.DataFrame(
        {'k': [float(val) for val in accuracy]},
        index=k
    )
    st.area_chart(chart_data)

def fixed_data():
    positive_images = os.listdir("dataset/happy/")
    negative_images = os.listdir("dataset/sad/")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Data Percentage')
        chart_data = pd.DataFrame(
            {'happy': [len(positive_images)],
            'sad': [len(negative_images)]},
            index=['sentiment']
        )
        st.bar_chart(chart_data)
    with col2:
        st.subheader('Data Info')
        all_data = len(positive_images) + len(negative_images)
        data_train = round(all_data * 0.8)
        data_test = round(all_data * 0.2)
        data_df1 = pd.DataFrame({"train": [data_train]})
        data_df2 = pd.DataFrame({"test": [data_test]})
        st.data_editor(
            data_df1,
            column_config={
                "train": st.column_config.NumberColumn(
                    label="Training Data",
                    help="The number of data training",
                    width="medium",
                )
            },
            disabled=True,
            hide_index=True,
        )
        st.data_editor(
            data_df2,
            column_config={
                "test": st.column_config.NumberColumn(
                    label="Testing Data",
                    help="The number of data testing",
                    width="medium",
                ),
            },
            disabled=True,
            hide_index=True,
        )

real_k()
fixed_data()