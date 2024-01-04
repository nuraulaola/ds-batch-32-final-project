# -*- coding: utf-8 -*-
"""Final Project AlgoWizard

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Tj7rG9X6YnKs9Q3Yxgzkq-ZjcMfO3KR

# 1. Import Libraries
"""

!pip install streamlit
import pandas as pd  # Data manipulation and analysis
import numpy as np  # Numerical operations on data
import matplotlib.pyplot as plt  # Data visualization
import seaborn as sns  # Data visualization

from sklearn.preprocessing import StandardScaler  # Perform scaling
from sklearn.model_selection import train_test_split  # Split data into training and testing sets

# ML model
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, LocalOutlierFactor
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, classification_report  # Measure model accuracy and display summary statistics of model performance
import streamlit as st  # Model deployment

from imblearn.over_sampling import SMOTE

import itertools

"""# 2. Exploratory Data Analysis (EDA) & Data Preprocessing

PIC : July, Ola, Osha, Faza

## 2.1 Membaca Dataset
"""

url = "https://raw.githubusercontent.com/nuraulaola/ds-batch-32-final-project/main/datasets/Dataset1_Customer_Churn.csv"
df = pd.read_csv(url)
df.head()

"""Data Description

Data Set Story:
- Jumlah total baris (10000 entries) dan rentang indeks barisnya (dari 0 hingga 9999) serta memiliki total 7 kolom.  
- Variabel independen adalah Gender, Age, CreditScore, EstimatedSalary, HasCrCard yang berisi informasi tentang pelanggan.
- Variabel dependen adalah Exited yang mengacu pada pelanggan yang menginggalkan layanan.


Features:
- CustomerId: ID unik untuk setiap pelanggan.
- Gender: Jenis kelamin pelanggan (Female / Male).
- Age: Usia pelanggan.
- CreditScore: Skor kredit dari pelanggan.
- EstimatedSalary: Perkiraan gaji pelanggan.
- HasCrCard: Menunjukkan apakah pelanggan memiliki kartu kredit (1 untuk ya, 0 untuk tidak).
- Exited: Variabel target yang menunjukkan apakah pelanggan keluar dari layanan (1 untuk ya, 0 untuk tidak).

"""

dependent_variable_name = "Exited"

"""## 2.2 EDA

### 2.2.1 Analisis Missing Values
"""

# Memeriksa missing values
missing_values = df.isnull().sum()

# Menampilkan jumlah missing values
print("Jumlah missing values:")
print(missing_values)

"""### 2.2.2 Analisis Nilai-Nilai Yang Duplikat"""

# Memeriksa nilai-nilai yang duplikat
duplicate_rows = df[df.duplicated()]

# Menampilkan baris yang merupakan duplikat
print("Duplikat dalam DataFrame:")
print(duplicate_rows)

"""### 2.2.3 Overview Tipe Data dari Setiap Kolom"""

# Memeriksa tipe data dari setiap kolom
column_data_types = df.dtypes

# Menampilkan tipe data dari setiap kolom
print("Tipe data dari setiap kolom:")
print(column_data_types)

"""### 2.2.4 Informasi Umum DataFrame"""

# Menampilkan informasi umum mengenai DataFrame
print("Informasi umum mengenai DataFrame:")
df.info()

"""### 2.2.5 Rangkuman Statistik Deskriptif"""

# Menampilkan statistik deskriptif singkat
print("Statistik deskriptif dari kolom numerik DataFrame:")
df.describe()

"""### 2.2.6 Plot Distribusi"""

# 1
# Menampilkan distribusi variabel dependen terhadap beberapa variabel independen
fig, axarr = plt.subplots(2, 3, figsize=(18, 6))

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'Gender'
sns.countplot(x='Gender', hue='Exited', data=df, ax=axarr[0, 0])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'Age'
sns.countplot(x='Age', hue='Exited', data=df, ax=axarr[0, 1])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'CreditScore'
sns.countplot(x='CreditScore', hue='Exited', data=df, ax=axarr[0, 2])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'EstimatedSalary'
sns.countplot(x='EstimatedSalary', hue='Exited', data=df, ax=axarr[1, 0])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'HasCrCard'
sns.countplot(x='HasCrCard', hue='Exited', data=df, ax=axarr[1, 1])

# Menghitung jumlah nilai 0 (tidak Exited) dan nilai 1 (Exited) pada variabel dependen 'Exited'
zero_count, one_count = df['Exited'].value_counts()
print("Distribusi variabel dependen:")
print("Exited 0 count:", zero_count)
print("Exited 1 count:", one_count)

fig.suptitle('Distribusi Variabel Dependen', fontsize=18)

# Menampilkan plot
plt.show()

# 2
# Menampilkan distribusi variabel numerik dalam DataFrame
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_num_cols = df.select_dtypes(include=numerics)
columns = df_num_cols.columns[: len(df_num_cols.columns)]

fig = plt.figure()
fig.set_size_inches(18, 15)
length = len(columns)

for i, j in zip(columns, range(length)):
    plt.subplot(int(length / 2), 3, j + 1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols[i].hist(bins=20, edgecolor='black')
    plt.title(i)

fig.suptitle('Struktur Variabel Numerik', fontsize=18)
plt.show()

# 3
# Menampilkan distribusi variabel dependen terhadap variabel lainnya
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_dependent_var = df[df['Exited']==1]
df_num_cols = df_dependent_var.select_dtypes(include=numerics)
columns = df_num_cols.columns[:len(df_num_cols.columns)]
fig = plt.figure()
fig.set_size_inches(18, 15)
length = len(columns)
for i, j in zip(columns, range(length)):
    plt.subplot(int(length/2), 3, j+1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols[i].hist(bins=20, edgecolor='black')
    plt.title(i)
fig.suptitle('Distribusi Variabel Dependen Terhadap Variabel Lainnya', fontsize=18)
plt.show()

# 4
# Menampilkan distribusi variabel kategorikal 'Gender' terhadap variabel dependen
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='Gender', hue='Exited', data=df, ax=ax)
ax.set_title('Distribusi Variabel Kategorikal Gender Terhadap Variabel Dependen')
plt.show()

"""### 2.2.7 Analisis Nilai-Nilai Unik"""

# Menampilkan jumlah nilai unik dari setiap variabel dalam dataframe
def show_unique_count_variables(df):
    for index, value in df.nunique().items():
        print(str(index) + "\n\t\t\t:" + str(value))

show_unique_count_variables(df)

"""## 2.3 Data Preprocessing

### 2.3.1 Mempersiapkan data
"""

#Mempersiapkan data
def data_prepare(df):
    df_prep = df.copy()

    # Encode variabel kategorikal
    df_prep = pd.get_dummies(df_prep, columns=['Gender'], drop_first=True)

    # Handle imbalance data menggunakan SMOTE
    smote = SMOTE(sampling_strategy='auto')
    X_smote, y_smote = smote.fit_resample(df_prep.drop('Exited', axis=1), df_prep['Exited'])

    # Menggabungkan hasil oversampling ke dalam DataFrame
    df_prep = pd.concat([pd.DataFrame(X_smote, columns=df_prep.drop('Exited', axis=1).columns), pd.Series(y_smote, name='Exited')], axis=1)

    return df_prep

# Menyimpan DataFrame yang telah dipersiapkan
df = data_prepare(df)

df

# Plot target_column
sns.countplot(x='Exited', data=df)
plt.title('Count Plot of Target Column after SMOTE')
plt.show()

# 1
# Menampilkan distribusi variabel dependen terhadap beberapa variabel independen
fig, axarr = plt.subplots(2, 3, figsize=(18, 6))

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen
sns.countplot(x='Gender_Male', hue='Exited', data=df, ax=axarr[0, 0])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'Age'
sns.countplot(x='Age', hue='Exited', data=df, ax=axarr[0, 1])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'CreditScore'
sns.countplot(x='CreditScore', hue='Exited', data=df, ax=axarr[0, 2])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'EstimatedSalary'
sns.countplot(x='EstimatedSalary', hue='Exited', data=df, ax=axarr[1, 0])

# Menampilkan distribusi variabel dependen 'Exited' terhadap variabel independen 'HasCrCard'
sns.countplot(x='HasCrCard', hue='Exited', data=df, ax=axarr[1, 1])

# Menghitung jumlah nilai 0 (tidak Exited) dan nilai 1 (Exited) pada variabel dependen 'Exited'
zero_count, one_count = df['Exited'].value_counts()
print("Distribusi variabel dependen:")
print("Exited 0 count:", zero_count)
print("Exited 1 count:", one_count)

fig.suptitle('Distribusi Variabel Dependen', fontsize=18)

# Menampilkan plot
plt.show()

# 2
# Menampilkan distribusi variabel numerik dalam DataFrame
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_num_cols = df.select_dtypes(include=numerics)
columns = df_num_cols.columns[: len(df_num_cols.columns)]

fig = plt.figure()
fig.set_size_inches(18, 15)
length = len(columns)

for i, j in zip(columns, range(length)):
    plt.subplot(int(length / 2), 3, j + 1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols[i].hist(bins=20, edgecolor='black')
    plt.title(i)

fig.suptitle('Struktur Variabel Numerik', fontsize=18)
plt.show()

# 3
# Menampilkan distribusi variabel dependen terhadap variabel lainnya
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_dependent_var = df[df['Exited']==1]
df_num_cols = df_dependent_var.select_dtypes(include=numerics)
columns = df_num_cols.columns[:len(df_num_cols.columns)]
fig = plt.figure()
fig.set_size_inches(18, 15)
length = len(columns)
for i, j in zip(columns, range(length)):
    plt.subplot(int(length/2), 3, j+1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols[i].hist(bins=20, edgecolor='black')
    plt.title(i)
fig.suptitle('Distribusi Variabel Dependen Terhadap Variabel Lainnya', fontsize=18)
plt.show()

# 4
# Menampilkan distribusi variabel kategorikal terhadap variabel dependen
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x='Gender_Male', hue='Exited', data=df, ax=ax)
ax.set_title('Distribusi Variabel Kategorikal Gender_Male Terhadap Variabel Dependen')
plt.show()

"""### 2.3.2 Handling Missing Values"""

def process_and_display_data(df):
    print("=== Informasi nilai-nilai yang hilang ===")
    # Menangani nilai yang hilang
    missing_value_len = df.isnull().any().sum()
    if missing_value_len == 0:
        print("Tidak ada nilai yang hilang.")
    else:
        print(f"Investigasi nilai yang hilang. Jumlah nilai yang hilang: {missing_value_len}")
    print("\n")

    print("=== Jumlah unik untuk setiap variabel ===")
    # Menampilkan jumlah unik untuk setiap variabel yang telah dipersiapkan
    for index, value in df.nunique().items():
        print(f"{index}\n\t\t\t:{value}")
    return df

result_df = process_and_display_data(df)

"""### 2.3.3 Handling Outliers"""

def handle_outliers(df):
    # Deteksi outlier dengan metode LOF
    lof = LocalOutlierFactor()
    outliers = lof.fit_predict(df.drop('Exited', axis=1))
    # Hapus baris yang teridentifikasi outlier
    df_no_outliers = df.loc[outliers != -1]

    return df_no_outliers

df = handle_outliers(df)

# Menampilkan informasi setelah handling outliers
result_df = process_and_display_data(df)

# Sebelum Penanganan Outlier
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_num_cols_before = df.select_dtypes(include=numerics)
columns_before = df_num_cols_before.columns[: len(df_num_cols_before.columns)]

fig_before = plt.figure()
fig_before.set_size_inches(18, 15)
length_before = len(columns_before)

for i, j in zip(columns_before, range(length_before)):
    plt.subplot(int(length_before / 2), 3, j + 1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols_before[i].hist(bins=20, edgecolor='black')
    plt.title(f'Sebelum Penanganan Outlier - {i}')

fig_before.suptitle('Perbandingan Distribusi Fitur Numerik Sebelum dan Sesudah Penanganan Outlier', fontsize=18)
plt.show()

# Setelah Penanganan Outlier
df_no_outliers = handle_outliers(df)

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_num_cols_after = df_no_outliers.select_dtypes(include=numerics)
columns_after = df_num_cols_after.columns[: len(df_num_cols_after.columns)]

fig_after = plt.figure()
fig_after.set_size_inches(18, 15)
length_after = len(columns_after)

for i, j in zip(columns_after, range(length_after)):
    plt.subplot(int(length_after / 2), 3, j + 1)
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    df_num_cols_after[i].hist(bins=20, edgecolor='black')
    plt.title(f'Setelah Penanganan Outlier - {i}')

fig_after.suptitle('Perbandingan Distribusi Fitur Numerik Sebelum dan Sesudah Penanganan Outlier', fontsize=18)
plt.show()

# Sebelum Penanganan Outlier
fig_before_box = plt.figure()
fig_before_box.set_size_inches(18, 8)
sns.set(style="whitegrid")

for i, column in enumerate(columns_before):
    plt.subplot(2, 3, i + 1)
    sns.boxplot(x=df_num_cols_before[column], color='skyblue')
    plt.title(f'Boxplot Sebelum Penanganan Outlier - {column}')

fig_before_box.suptitle('Perbandingan Boxplot Fitur Numerik Sebelum Penanganan Outlier', fontsize=18)
plt.show()

# Setelah Penanganan Outlier
fig_after_box = plt.figure()
fig_after_box.set_size_inches(18, 8)

for i, column in enumerate(columns_after):
    plt.subplot(2, 3, i + 1)
    sns.boxplot(x=df_num_cols_after[column], color='lightcoral')
    plt.title(f'Boxplot Setelah Penanganan Outlier - {column}')

fig_after_box.suptitle('Perbandingan Boxplot Fitur Numerik Setelah Penanganan Outlier', fontsize=18)
plt.show()

"""# 3. Model Training

PIC : Timmy, Eko

## 3.1 Splitting Data
"""

def model_prepare(df_model):
    y = df_model[dependent_variable_name]
    X = df_model.loc[:, df_model.columns != dependent_variable_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform (X_test)
    return X_train, X_test, y_train, y_test

"""## 3.2 Scaling

## 3.3 Model Training
"""

def data_training(X_train, X_test, y_train, y_test):

    models = []
    models.append(('LOGR', LogisticRegression()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('RF', RandomForestClassifier()))
    models.append(('GBM', GradientBoostingClassifier()))
    models.append(('XGBoost', XGBClassifier()))
    models.append(('LightGBM', LGBMClassifier()))
    models.append(('SVM', SVC()))
    models.append(('AdaBoost', AdaBoostClassifier()))

    res_cols = ["model", "accuracy_score", "0_precision", "0_recall", "1_precision", "1_recall"]
    df_result = pd.DataFrame(columns=res_cols)
    index = 0
    for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, digits=2, output_dict=True)
        zero_report = class_report['0']
        one_report = class_report['1']

        idx_res_values = [name, score, zero_report['precision'], zero_report['recall'], one_report['precision'], one_report['recall']]
        # df_result.at[index, res_cols] = idx_res_values
        df_result.loc[index, res_cols] = idx_res_values
        index += 1
    return df_result.sort_values('accuracy_score', ascending=False)
    # df_result = df_result.sort_values("accuracy_score", ascending=False).reset_index(drop=True)
    # return df_result

# Model_prepare test, train split 0.2
X_train, X_test, y_train, y_test = model_prepare(df_model=df_encoded)

"""## 3.3.1 | Logistic Regression"""

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression(C=1, penalty='l2', solver='liblinear', max_iter=200)
log_reg.fit(X_train, y_train)

from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def predict_and_plot(model, inputs, targets, name=''):
    preds = model.predict(inputs)
    accuracy = accuracy_score(targets, preds)
    print("Accuracy: {:.2f}%".format(accuracy * 100))

    cf = confusion_matrix(targets, preds, normalize='true')
    plt.figure()
    sns.heatmap(cf, annot=True)
    plt.xlabel('Prediction')
    plt.ylabel('Target')
    plt.title('{} Confusion Matrix'.format(name))

    return preds

# Predict and plot on the training data
train_preds = predict_and_plot(log_reg, X_train, y_train, 'Train')

# Predict and plot on the validation data
val_preds = predict_and_plot(log_reg, X_test, y_test, 'Validation')

"""## 3.3.2 | KNN"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a KNN classifier (you can adjust the number of neighbors 'n_neighbors')
knn_model = KNeighborsClassifier(n_neighbors=5)

# Fit the KNN model to the training data
knn_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred = knn_model.predict(X_train)

# Make predictions on the validation data
y_val_pred = knn_model.predict(X_val)

# Calculate the training and validation accuracies
train_accuracy = accuracy_score(y_train, y_train_pred)
val_accuracy = accuracy_score(y_val, y_val_pred)

print("Training Accuracy:", train_accuracy)
print("Validation Accuracy:", val_accuracy)

# Create a confusion matrix for validation data
confusion = confusion_matrix(y_val, y_val_pred)

# Plot the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Validation)')
plt.show()

"""<a id="3.3.2"></a>
> <span style='font-size:15px; font-family:Verdana;color: #254E58;'><b> Hyperparameter Tuning of KNN </b></span>
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# Define the hyperparameter grid to search
param_grid = {
    'n_neighbors': [1, 3, 5, 7, 9]  # Adjust the number of neighbors to explore
}

# Create the KNN classifier
knn_model = KNeighborsClassifier()

# Perform GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(knn_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best estimator with tuned hyperparameters
best_model = grid_search.best_estimator_

# Make predictions on the training data using the best model
y_train_pred = best_model.predict(X_train)

# Make predictions on the validation data using the best model
y_val_pred = best_model.predict(X_val)

# Calculate the training and validation accuracies
train_accuracy = accuracy_score(y_train, y_train_pred)
val_accuracy = accuracy_score(y_val, y_val_pred)

print("Training Accuracy with Best Hyperparameters:", train_accuracy)
print("Validation Accuracy with Best Hyperparameters:", val_accuracy)

"""## 3.3.3 | Decision Tree"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Create the Decision Tree model
decision_tree_model = DecisionTreeClassifier(random_state=42)

# Fit the model to the training data
decision_tree_model.fit(X_train, y_train)

# Evaluate the model on the training and validation data
train_accuracy = decision_tree_model.score(X_train, y_train)
val_accuracy = decision_tree_model.score(X_test, y_test)

# Print the results
print("Training Accuracy:", train_accuracy)
print("Validation Accuracy:", val_accuracy)

"""<a id="3.3.3"></a>
> <span style='font-size:15px; font-family:Verdana;color: #254E58;'><b> Hyperparameter Tuning Of Decision Tree </b></span>
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10, 15, 20, 25],
    'min_samples_leaf': [1, 3, 5, 7],
    'criterion': ['gini', 'entropy']  # Add criterion hyperparameter
}

# Create the Decision Tree model
decision_tree_model = DecisionTreeClassifier(random_state=42)

# Perform GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(decision_tree_model, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best estimator with tuned hyperparameters
best_model = grid_search.best_estimator_

# Fit the final model to the training data
best_model.fit(X_train, y_train)

# Evaluate the final model on the training and validation data
train_accuracy = best_model.score(X_train, y_train)
val_accuracy = best_model.score(X_test, y_test)

# Print the results
print("Training Accuracy:", train_accuracy)
print("Validation Accuracy:", val_accuracy)

"""## 3.3.4 | Random Forest"""

from sklearn.ensemble import RandomForestClassifier
model_2 = RandomForestClassifier(n_jobs =-1, random_state = 42)
model_2.fit(X_train,y_train)

model_2.score(X_train,y_train)

def predict_and_plot(model, inputs,targets, name = ''):
    preds = model.predict(inputs)
    accuracy = accuracy_score(targets, preds)
    print("Accuracy: {:.2f}%".format(accuracy*100))

    cf = confusion_matrix(targets, preds, normalize = 'true')
    plt.figure()
    sns.heatmap(cf, annot = True)
    plt.xlabel('Prediction')
    plt.ylabel('Target')
    plt.title('{} Confusion Matrix'. format(name))

    return preds

# Predict and plot on the training data
train_preds = predict_and_plot(model_2, X_train, y_train, 'Train')

# Predict and plot on the validation data
val_preds = predict_and_plot(model_2, X_test, y_test, 'Validation')

"""<a id="3.3.4"></a>
> <span style='font-size:15px; font-family:Verdana;color: #254E58;'><b>Hyperparameter Tuning of Random Forest </b></span>
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

param_grid = {
    'n_estimators': [10, 20, 30],  # Adjust the number of trees in the forest
    'max_depth': [10, 20, 30],  # Adjust the maximum depth of each tree
    'min_samples_split': [2, 5, 10, 15, 20],  # Adjust the minimum samples required to split a node
    'min_samples_leaf': [1, 2, 4, 6, 8]  # Adjust the minimum samples required in a leaf node
}

# Create the Random Forest model
random_forest_model = RandomForestClassifier(random_state=42, n_jobs=-1)

# Perform GridSearchCV for hyperparameter tuning
grid_search = GridSearchCV(random_forest_model, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Get the best estimator with tuned hyperparameters
best_model = grid_search.best_estimator_

# Fit the final model to the training data
best_model.fit(X_train, y_train)

# Evaluate the model on the training and validation data
train_accuracy = best_model.score(X_train, y_train)
val_accuracy = best_model.score(X_test, y_test)

# Print the results
print("Training Accuracy:", train_accuracy)
print("Validation Accuracy:", val_accuracy)

"""## 3.3.5 | Support Vector Classifier"""

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

svm_model = SVC(kernel='linear')

# Fit the SVM model to the training data
svm_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred = svm_model.predict(X_train)

# Make predictions on the validation data
y_val_pred = svm_model.predict(X_val)

# Calculate the training accuracy
train_accuracy = accuracy_score(y_train, y_train_pred)

# Calculate the validation accuracy
val_accuracy = accuracy_score(y_val, y_val_pred)

print("Training Accuracy:", train_accuracy)
print("Validation Accuracy:", val_accuracy)

# Create confusion matrices
train_confusion = confusion_matrix(y_train, y_train_pred)
val_confusion = confusion_matrix(y_val, y_val_pred)

# Plot the confusion matrices
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.heatmap(train_confusion, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Training)')

plt.subplot(1, 2, 2)
sns.heatmap(val_confusion, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Validation)')
plt.show()

"""## 3.3.6 | AdaBoost Classifier"""

from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Create an AdaBoost classifier
adaboost_model = AdaBoostClassifier(n_estimators=50, random_state=42)

# Fit the AdaBoost model to the training data
adaboost_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred_adaboost = adaboost_model.predict(X_train)

# Make predictions on the validation data
y_val_pred_adaboost = adaboost_model.predict(X_val)

# Calculate the training accuracy
train_accuracy_adaboost = accuracy_score(y_train, y_train_pred_adaboost)

# Calculate the validation accuracy
val_accuracy_adaboost = accuracy_score(y_val, y_val_pred_adaboost)

# Print the training and validation accuracies
print("AdaBoost Training Accuracy:", train_accuracy_adaboost)
print("AdaBoost Validation Accuracy:", val_accuracy_adaboost)

# Create a confusion matrix for validation
confusion_adaboost = confusion_matrix(y_val, y_val_pred_adaboost)

# Plot the confusion matrix
plt.figure()
sns.heatmap(confusion_adaboost, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('AdaBoost Confusion Matrix (Validation)')
plt.show()

"""## 3.3.7 | Gradient Boosting Classifier"""

from sklearn.ensemble import GradientBoostingClassifier

# Create a Gradient Boosting classifier
gbm_model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)

# Fit the GBM model to the training data
gbm_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred_gbm = gbm_model.predict(X_train)

# Make predictions on the validation data
y_val_pred_gbm = gbm_model.predict(X_val)

# Calculate the training accuracy
train_accuracy_gbm = accuracy_score(y_train, y_train_pred_gbm)

# Calculate the validation accuracy
val_accuracy_gbm = accuracy_score(y_val, y_val_pred_gbm)

# Print the training and validation accuracies
print("GBM Training Accuracy:", train_accuracy_gbm)
print("GBM Validation Accuracy:", val_accuracy_gbm)

"""## 3.3.8 | XGBoost Classifier"""

from xgboost import XGBClassifier

# Create an XGBoost classifier
xgboost_model = XGBClassifier(n_estimators=100, max_depth=3, random_state=42)

# Fit the XGBoost model to the training data
xgboost_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred_xgboost = xgboost_model.predict(X_train)

# Make predictions on the validation data
y_val_pred_xgboost = xgboost_model.predict(X_val)

# Calculate the training accuracy
train_accuracy_xgboost = accuracy_score(y_train, y_train_pred_xgboost)

# Calculate the validation accuracy
val_accuracy_xgboost = accuracy_score(y_val, y_val_pred_xgboost)

# Print the training and validation accuracies
print("XGBoost Training Accuracy:", train_accuracy_xgboost)
print("XGBoost Validation Accuracy:", val_accuracy_xgboost)

"""<a id="3.3.8"></a>
> <span style='font-size:15px; font-family:Verdana;color: #254E58;'><b>Hyperparameter Tuning of XGBoost</b></span>
"""

xgb_model=XGBClassifier(
    learning_rate=0.23, max_delta_step=5,
    objective='reg:logistic', n_estimators=92,
    max_depth=5, eval_metric="logloss", gamma=3, base_score=0.5)

xgb_model.fit(X_train, y_train)
y_pred = xgb_model.predict(X_test)
print(classification_report(y_test, y_pred, digits=2))
print("Accuracy score of Tuned XGBoost Regression: ", accuracy_score(y_test, y_pred))

"""## 3.3.9 | LightGBM Classifier"""

from lightgbm import LGBMClassifier

# Create a Gradient Boosting classifier
lgbm_model = LGBMClassifier(n_estimators=100, max_depth=3, random_state=42)

# Fit the GBM model to the training data
lgbm_model.fit(X_train, y_train)

# Make predictions on the training data
y_train_pred_lgbm = lgbm_model.predict(X_train)

# Make predictions on the validation data
y_val_pred_lgbm = lgbm_model.predict(X_val)

# Calculate the training accuracy
train_accuracy_lgbm = accuracy_score(y_train, y_train_pred_lgbm)

# Calculate the validation accuracy
val_accuracy_lgbm = accuracy_score(y_val, y_val_pred_lgbm)

# Print the training and validation accuracies
print("LightGBM Training Accuracy:", train_accuracy_lgbm)
print("LightGBM Validation Accuracy:", val_accuracy_lgbm)

"""<a id="3.3.9"></a>
> <span style='font-size:15px; font-family:Verdana;color: #254E58;'><b>Hyperparameter Tuning of LightGBM</b></span>
"""

lgbm_model = LGBMClassifier(
    silent = 0, learning_rate = 0.09, max_delta_step = 2,
    n_estimators = 100, boosting_type = 'gbdt',
    max_depth = 10, eval_metric = "logloss",
    gamma = 3, base_score = 0.5
)

lgbm_model.fit(X_train, y_train)
y_pred = lgbm_model.predict(X_test)
print(classification_report(y_test, y_pred, digits=2))
print("Accuracy score of tuned LightGBM model: ", accuracy_score(y_test, y_pred))

training_result = data_training(X_train, X_test, y_train, y_test)
training_result

"""# 4. Model Deployment

PIC : Kemas

## 4.1 Streamlit App
"""

import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd
import numpy as np

with open('model/Random_Forest_model.pkl','rb') as file:
    Random_Forest_Model = pickle.load(file)

def main():
    # stc.html(html_temp)
    st.title("Customer Churn Prediction App")
    st.caption("This app is created by Algowizard Team for Final Project of Data Science Bootcamp")

    menu = ["Home","Machine Learning"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.header("Home")
        st.caption("Aplikasi prediksi churn memanfaatkan pembelajaran mesin dan kecerdasan buatan untuk menganalisis data pelanggan dan mengidentifikasi mereka yang berisiko pergi. Hal ini memungkinkan bisnis untuk secara proaktif melibatkan pelanggan ini dengan intervensi yang ditargetkan dan strategi retensi, meminimalkan churn dan meningkatkan nilai umur pelanggan.")

        st.markdown("""
            <p style="font-size: 16px; font-weight: bold">Sekilas tentang Dataset yang digunakan</p>
            """, unsafe_allow_html=True)

        df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
        st.table(df)


    elif choice == "Machine Learning":
        st.header("Prediction Model")
        run_ml_app()

    col1, col2, col3 = st.columns([1, 10, 1])  # Center column takes up most of the width
    with col2:
        images = ["1. Ola.png", "2. July.png", "3. Faza.png","4. Timmy.png",
              "5. Kemas.png", "6. Eko.png", "7. Osha.png"]
        st.image(images, width=80)  # Set width for each image

def run_ml_app():
    # design = """<div style='padding:15px;">
    #                 <h1 style='color:#fff'>Loan Eligibility Prediction</h1>
    #             </div>"""
    # st.markdown(design, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size: 16px; font-weight: bold">Insert Data</p>
    """, unsafe_allow_html=True)

    left, right = st.columns((2,2))
    gender = left.selectbox('Gender',
                            ('Male', 'Female'))
    age = left.number_input('Age', 1, 100)
    credit_score = left.number_input('Credit Score',0,1000)
    estimated_salary = right.number_input('Estimated Salary',0.0,100000000.00)
    has_credit_card = right.selectbox('Credit Card',('Yes','No'))

    # married = right.selectbox('Married', ('Yes','No'))
    # dependent = left.selectbox('Dependents', ('None', 'One', 'Two', 'Three'))
    # education = right.selectbox('Education', ('Graduate', 'Non-Graduate'))
    # self_employed = left.selectbox('Self-Employed', ('Yes', 'No'))
    # applicant_income = right.number_input('Applicant Income')
    # coApplicant_income = left.number_input(
    #     'Co - Applicant Income')
    # loan_amount = right.number_input('Loan Amount')
    # loan_amount_term = left.number_input('Loan Tenor (In Months)')
    # credit_history = right.number_input('Credit History', 0.0, 1.0)
    # property_area = st.selectbox('Property Area', ('Semiurban','Urban', 'Rural'))
    button = st.button('Predict')

    #if button is clicked (ketika button dipencet)
    if button:
        #make prediction
        result = predict(gender,age,credit_score,estimated_salary,has_credit_card)
        if result == 'Eligible':
            st.success(f'You are {result} for the loan')
        else:
            st.warning(f'You are {result} for the loan')


def predict(gender,age,credit_score,estimated_salary,has_credit_card):
    #processing user input
    gen = 0 if gender == 'Male' else 1
    cre = 0 if has_credit_card == 'No' else 1
    # mar = 0 if married == 'Yes' else 1
    # dep = float(0 if dependent == 'None' else 1 if dependent == 'One' else 2 if dependent == 'Two' else 3)
    # edu = 0 if education == 'Graduate' else 1
    # sem = 0 if self_employed == 'Yes' else 1
    # pro = 0 if property_area == 'Semiurban' else 1 if property_area == 'Urban' else 2
    # lam = loan_amount/1000
    # cap = coApplicant_income / 1000

    #Making prediction
    prediction = Random_Forest_Model.predict([[gen, cre, age, credit_score,
                                               estimated_salary]])
    result = 'Stayed' if prediction == 0 else 'Exited'

    return result

if __name__ == "__main__":
    main()