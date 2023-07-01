import streamlit as st
import joblib
import pandas as pd
import Backend as be

st.set_page_config(page_title="IEIS", page_icon="🖼️")
st.title("Welcome to IEIS! 👋")
st.caption("Image Emotion Identification System (IEIS) is a web-based application that can analyze the sentiment of the image. This app utilizes the GLCM method for texture analysis, and the K-Nearest Neighbors (KNN) algorithm to classify the image's sentiment with more than 2,000 dataset. It is important to note that the uploaded images should have a resolution of 48x48 pixels, a 1:1 aspect ratio and be properly aligned with the face.")

uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

if len(uploaded_file) == 0:
    button = st.button("Predict", disabled=True)

else:
    button = st.button("Predict", disabled=False)

    if button:
        sentiment = []
        emoji = []

        for image in uploaded_file:
            sentiment.append(be.get_sentiment(image))
            if be.get_sentiment(image) == 1:
                emoji.append("🤓")
            else:
                emoji.append("😭")

        happy = sentiment.count(1)
        sad = sentiment.count(0)
        happy_percentage = (happy / len(sentiment)) * 100
        sad_percentage = (sad / len(sentiment)) * 100

        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:

            data_df1 = pd.DataFrame({"happy": [happy_percentage]})
            st.data_editor(
                data_df1,
                column_config={
                    "happy": st.column_config.ProgressColumn(
                        label="Happy",
                        help="The number of happy images",
                        width="large",
                        format="%.0f%%",
                        min_value=0,
                        max_value=100,
                    ),
                },
                disabled=True,
                hide_index=True,
            )

            data_df2 = pd.DataFrame({"sad": [sad_percentage]})
            st.data_editor(
                data_df2,
                column_config={
                    "sad": st.column_config.ProgressColumn(
                        label="Sad",
                        help="The number of sad images",
                        width="large",
                        format="%.0f%%",
                        min_value=0,
                        max_value=100,
                    ),
                },
                disabled=True,
                hide_index=True,
            )

        num_images = len(uploaded_file)
        max_columns = 4

        for i in range(0, num_images, max_columns):
            cols = st.columns(min(num_images - i, max_columns))
            for j in range(min(num_images - i, max_columns)):
                with cols[j]:
                    st.image(
                        uploaded_file[i + j],
                        caption=uploaded_file[i + j].name + " " + emoji[i + j],
                        use_column_width=True
                    )