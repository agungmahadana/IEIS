import streamlit as st
import re
import os
import math
import pandas as pd

st.set_page_config(page_title="IEIS - Dataset", page_icon="🖼️")
st.title("Dataset 📂")

image_folder_happy = "dataset/happy/"
image_folder_sad = "dataset/sad/"

positive_images = os.listdir(image_folder_happy)
negative_images = os.listdir(image_folder_sad)

image_files = []
file_names = []

type = st.radio("Select type", ('All', 'Happy', 'Sad'), horizontal=True)

if type == 'All':
    image_files.extend([os.path.join(image_folder_happy, img) for img in positive_images])
    image_files.extend([os.path.join(image_folder_sad, img) for img in negative_images])
    file_names.extend(positive_images)
    file_names.extend(negative_images)
elif type == 'Happy':
    image_files.extend([os.path.join(image_folder_happy, img) for img in positive_images])
    file_names.extend(positive_images)
elif type == 'Sad':
    image_files.extend([os.path.join(image_folder_sad, img) for img in negative_images])
    file_names.extend(negative_images)

row = st.number_input("Enter the value of row", min_value=1, max_value=math.ceil(len(image_files) / 6))

columns = st.columns(6)
for i in range(row):
    for j in range(6):
        index = i * 6 + j
        if index < len(image_files):
            with columns[j]:
                st.image(image_files[index], caption=file_names[index])