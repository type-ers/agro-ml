import pandas as pd
import numpy as np

from flask import *

from os.path import abspath, join
from os import listdir, environ
from joblib import load
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import VGG16, preprocess_input
from PIL import Image
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


fertilizer_model_dir = "models/fertilizer.pkl"

d_model_apple_dir = "models/disease/apple.h5"

market_dir = 'models/market'