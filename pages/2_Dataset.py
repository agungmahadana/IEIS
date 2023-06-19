import streamlit as st
import re
import math
import pandas as pd
from pathlib import Path
from skimage import io

st.set_page_config(page_title="IEIS - Dataset", page_icon="🖼️")
st.title("Dataset 📂")

BASE_DIR = Path(__file__).resolve().parent.parent
image_folder_happy = BASE_DIR / "dataset/happy/"
image_folder_sad = BASE_DIR / "dataset/sad/"

positive_images = [image.name for image in image_folder_happy.glob("*")]
negative_images = [image.name for image in image_folder_sad.glob("*")]

image_files = []
file_names = []

type = st.radio("Select type", ('All', 'Happy', 'Sad'), horizontal=True)

if type == 'All':
    for i in range(max(len(positive_images), len(negative_images))):
        if i < len(positive_images):
            image_files.append(image_folder_happy / positive_images[i])
            file_names.append(positive_images[i])
        if i < len(negative_images):
            image_files.append(image_folder_sad / negative_images[i])
            file_names.append(negative_images[i])
elif type == 'Happy':
    image_files.extend([image_folder_happy / image for image in positive_images])
    file_names.extend(positive_images)
elif type == 'Sad':
    image_files.extend([image_folder_sad / image for image in negative_images])
    file_names.extend(negative_images)

row = st.number_input("Enter the value of row", min_value=1, max_value=math.ceil(len(image_files) / 6))

columns = st.columns(6)
for i in range(row):
    for j in range(6):
        index = i * 6 + j
        if index < len(image_files):
            with columns[j]:
                st.image(io.imread(image_files[index]), caption=file_names[index])