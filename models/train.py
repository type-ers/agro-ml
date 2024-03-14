import pandas as pd
import os
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier
from PIL import Image, UnidentifiedImageError 

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

from joblib import dump


def train_fertilizer():
    data = pd.read_csv('data/fertilizer.csv')

    y = data['Fertilizer Name'].copy()
    X = data.drop('Fertilizer Name', axis=1).copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)

    nominal_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder())
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('nominal', nominal_transformer, ['Soil Type', 'Crop Type'])
    ], remainder='passthrough')

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier())
    ])

    model.fit(X_train, y_train)

    dump(model, "fertilizer.pkl")

def train_market():
    data = pd.read_csv('data/market.csv')

    data['Date'] = pd.to_datetime(data['Date']).apply(lambda x: x.toordinal())

    commodity_data = {}

    for _, row in data.iterrows():
        commodity = row['Commodity']

        if commodity not in commodity_data:
            commodity_data[commodity] = {'X': [], 'y': []}

        commodity_data[commodity]['X'].append([row['Date']])
        commodity_data[commodity]['y'].append(row['Average'])

    models = {}
    for commodity, data in commodity_data.items():
        X_train, X_test, y_train, y_test = train_test_split(data['X'], data['y'], test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        models[commodity] = model
        dump(model, f'market/{commodity}_model.pkl')

def train_disease():
    data_dir = 'data/disease/'
    disease_labels = {
        "apple": ["alternaria_leaf_spot", "brown_spot", "frogeye_leaf_spot", "gray_spot", "healthy", "mosaic", "powdery_mildew", "rust", "scab"]
    }

    input_shape = (255, 255, 3)
    num_epochs = 10
    batch_size = 32

    for crop, diseases in disease_labels.items():
        train_datagen = ImageDataGenerator(
            rescale=1.0/255.0,
            validation_split=0.2
        )

        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=(input_shape[0], input_shape[1]),
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            classes=[crop]
        )

        validation_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=(input_shape[0], input_shape[1]),
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            classes=[crop]
        )

        num_classes = len(diseases)

        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(num_classes, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size,
            epochs=num_epochs
        )

        model.save(f'disease/{crop}.keras')

if __name__ == "__main__":
    train_disease()
    print("DISEASE MODEL = DONE")
    train_fertilizer()
    print("FERTILIZER MODEL = DONE")
    train_market()
    print("MARKET MODEL = DONE")