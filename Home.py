import streamlit as st
import pandas as pd
from skimage import io, color, util, transform
import Backend as be

st.set_page_config(page_title="IEIS", page_icon="🖼️")
st.title("Welcome to IEIS! 👋")
st.caption("Image Emotion Identification System (IEIS) is a web-based application that can analyze the colors and textures of images based on various techniques. This app allows users to analyze more than 4,000 image samples for color analysis (such as converting an image to a pixel matrix, generating a color histogram, and calculating first-order statistics) and texture analysis (such as generating the Gray Level Co-occurrence Matrix (GLCM) of an image and creating a texture histogram). This app was created by a [student](https://github.com/agungmahadana/) using Python and Streamlit. PASTIKAN GAMBAR YANG KAMU UPLOAD MEMILIKI RASIO 1:1 DAN MEMILIKI RESOLUSI 48x48 DAN TEPAT DI DEPAN WAJAHNYA.")

uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
k = st.number_input("Enter the value of k", min_value=1)

if uploaded_file is None:
    button = st.button("Predict", disabled=True)

else:
    button = st.button("Predict", disabled=False)
    if button:
        image = io.imread(uploaded_file)
        
        if (image.shape[0] > 48) or (image.shape[1] > 48):
            image = transform.resize(image, (48, 48))

        img = image

        if len(img.shape) == 3:  # Periksa jika gambar memiliki saluran warna
            img = img[:, :, :3]  # Hapus saluran Alpha
            img = color.rgb2gray(img)

        img = util.img_as_ubyte(img)
        new_features = be.glcm_matrix(img)
        prediction = be.knn_predict(new_features, k)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption=uploaded_file.name, use_column_width=True)

        with col2:
            sentiment = "Happy 😊" if prediction[0] == 1 else "Sad 😔"
            data_df1 = pd.DataFrame({"sentiment": [sentiment]})
            data_df2 = pd.DataFrame({"accuracy": [prediction[1]]})
            st.data_editor(
                data_df1,
                column_config={
                    "sentiment": st.column_config.TextColumn(
                        label="Sentiment",
                        help="The sentiment of the image",
                        width="medium",
                    )
                },
                hide_index=True,
            )
            st.data_editor(
                data_df2,
                column_config={
                    "accuracy": st.column_config.ProgressColumn(
                        label="Accuracy",
                        help="The accuracy of the model",
                        width="medium",
                        format="%.2f%%",
                        min_value=0,
                        max_value=100,
                    ),
                },
                hide_index=True,
            )