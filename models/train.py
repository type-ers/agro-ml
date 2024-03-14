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

from keras.models import Model
from keras.optimizers import Adam
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Dropout, Flatten
from pathlib import Path
from keras.callbacks import ModelCheckpoint

import numpy as np

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
    disease_labels = {
        "apple": ["brown_spot", "healthy", "mosaic"],   
    }

    train_generator = ImageDataGenerator(
        rotation_range=90,
        width_shift_range=0.5,
        height_shift_range=0.5,
        horizontal_flip=True,
        vertical_flip=True,
        validation_split=0.15,
        preprocessing_function=preprocess_input
    )
    
    img_height = 224
    img_width = 224
    train_data_dir = 'data/disease/'
    
    classes = sorted(os.listdir('test/'))
    print(classes)
    
    train_gen = train_generator.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size = 32,
        class_mode = 'categorical',
        shuffle=True,
        classes = classes,
    
    )
    
    valid_gen = train_generator.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=32,
        class_mode='categorical',
        shuffle=True,
        classes=classes,
    )
    
    conv_base = VGG16(
        include_top=False,
        weights='imagenet',
        input_shape=[img_height, img_width] + [3]
    )
    
    for layer in conv_base.layers:
        layer.trainable = False
    
    
    x = Flatten()(conv_base.output)
    prediction = Dense(3, activation='softmax')(x)
    top_model = Model(inputs=conv_base.input, outputs=prediction)
    top_model.summary()
    
    top_model = Model(inputs = conv_base.input, outputs = prediction)
    top_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
    
    checkpoint = ModelCheckpoint(
        filepath='apple2.h5',
        verbose=2, save_best_only=True, monitor='val_loss'
    )
    callbacks = [checkpoint]
    
    
    model_history=top_model.fit_generator(
        train_gen,
        validation_data=valid_gen,
        epochs=10,
        steps_per_epoch=5,
        validation_steps=32,
        callbacks=callbacks,
        verbose=2
    )
    

if __name__ == "__main__":
    train_disease()
    print("DISEASE MODEL = DONE")
    train_fertilizer()
    print("FERTILIZER MODEL = DONE")
    train_market()
    print("MARKET MODEL = DONE")