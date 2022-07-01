import os
from progress.bar import ChargingBar
from PIL import Image
import numpy as np
import pandas as pd
import tensorflow.keras as keras
import eel
import dill as pickle
from sklearn.utils import *
from sklearn.model_selection import train_test_split


#internal method that is called in order to read images from a folder, resize them, and transform them into a numpy pixel array.
def read_to_list(path, df, list, bar = None, bar_label = 'processing data'):
    if(bar is None):
        bar = ChargingBar(bar_label, max=len(df.Path))

    counter = 0
    for i in df.Path:
        img = Image.open(path+i)       # reading image
        img = img.resize((32,32))     # reasizing image
        list.append(np.array(img)) # saving image as array to train
        counter += 1
        eel.updateProgress(counter, len(df.Path))
        bar.next()


#method that is called in order to read data from file, normalize it, one hot encode it, resize it and pack it in an object
def process_data(data_path): 

    print("initializing data")

    #reading train and test datasets into memory and transforming the images into numpy arrays.
    train_df = pd.read_csv(data_path+'Train.csv')
    train_df.head()

    eel.updateAction("Processing train data")

    x_train =[] #list of images to train with
    read_to_list(data_path, train_df, x_train, bar_label= 'processing train data')

    y_train = np.array(train_df.ClassId) #list of labels to train with
    x_train = np.array(x_train)

    test_df = pd.read_csv(data_path+'Test.csv')
    test_df.head()

    eel.updateAction("Processing test data")

    x_test =[] #list of images to test with
    read_to_list(data_path, test_df, x_test, bar_label= 'processing test data')

    eel.nextStep()
    eel.updateAction("Finalizing data and preparing model")

    y_test = np.array(test_df.ClassId)#list of lables to test with
    x_test = np.array(x_test)
    
    # Normalization
    normalize = lambda x: x/255

    x_train = normalize(x_train)
    x_test = normalize(x_test)

    eel.updateProgress(1, 5)

    # One Hot encoding
    print("\nOne Hot Encoding...")
    y_train = keras.utils.to_categorical(y_train)
    y_test = keras.utils.to_categorical(y_test)

    eel.updateProgress(2, 5)

    ## Splitting into train and validation data
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=0, shuffle=True)

    eel.updateProgress(3, 5)

    ##returning anonymous object with the data
    Object = lambda **kwargs: type("Object", (), kwargs) #anonymous object "class"
    data = Object(x_train = x_train, x_val= x_val, x_test = x_test, y_train = y_train, y_val = y_val, y_test = y_test)

    #saving the processed data in a pickle file for future use
    with open(data_path + '\\pickle', 'wb') as f: 
        pickle.dump(data, f)

    eel.updateProgress(4, 5)
    return data

