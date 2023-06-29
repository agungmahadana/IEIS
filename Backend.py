import os
import joblib
import numpy as np
from skimage import io, color, util, transform
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def initialization(image):
    image = io.imread(image)
    # Periksa jika gambar tidak memiliki resolusi 48x48
    if (image.shape[0] != 48) or (image.shape[1] != 48):
        image = transform.resize(image, (48, 48))
    # Periksa jika gambar memiliki saluran Alpha
    if len(image.shape) == 3:
        image = image[:, :, :3]
        image = color.rgb2gray(image)
    image = util.img_as_ubyte(image)
    return image

# Hitung fitur GLCM
def compute_glcm(image, angles):
    glcm = graycomatrix(image, distances=[1], angles=angles, levels=256, symmetric=True, normed=True)
    return glcm

# Hitung matriks GLCM
def glcm_matrix(image):
    matrix = []
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
    metric_texture = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']
    for i in metric_texture:
        row = []
        for j in angles:
            row.append(graycoprops(compute_glcm(image, [j]), prop=i)[0][0])
        matrix.append(row)
    return np.array(matrix).flatten()

# Prediksi model
def model_predict(features):
    model = joblib.load("models/best_model")
    prediction = model.predict([features])
    return prediction[0]

def get_sentiment(image):
    image = initialization(image)
    new_features = glcm_matrix(image)
    prediction = model_predict(new_features)
    return prediction