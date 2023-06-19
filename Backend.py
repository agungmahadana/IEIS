import os
import numpy as np
from skimage import io, color, util
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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

X = []  # Features
y = []  # Labels

# Load citra dengan ekspresi happy
positive_images = os.listdir("dataset/happy/")
for img_path in positive_images:
    image = io.imread("dataset/happy/" + img_path)
    features = glcm_matrix(image)
    X.append(features)
    y.append(1)  # Sentimen positif

# Load citra dengan ekspresi sad
negative_images = os.listdir("dataset/sad/")
for img_path in negative_images:
    image = io.imread("dataset/sad/" + img_path)
    features = glcm_matrix(image)
    X.append(features)
    y.append(0)  # Sentimen negatif

# Pisahkan data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def knn_predict(features, n):
    # Inisialisasi model KNN
    knn = KNeighborsClassifier(n_neighbors=n)
    # Latih model
    knn.fit(X_train, y_train)
    # Prediksi sentimen
    prediction = knn.predict([features])
    # Evaluasi model
    accuracy = knn.score(X_test, y_test)
    accuracy_percentage = accuracy * 100
    return prediction[0], accuracy_percentage

def knn_score(n):
    # Inisialisasi model KNN
    knn = KNeighborsClassifier(n_neighbors=n)
    # Latih model
    knn.fit(X_train, y_train)
    # Evaluasi model
    accuracy = knn.score(X_test, y_test)
    accuracy_percentage = accuracy * 100
    return accuracy_percentage.round(2)

def get_data():
    return [len(X_train), len(X_test)]