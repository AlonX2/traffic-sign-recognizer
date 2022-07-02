import dataHandler as dh
from model import Model
import warnings
import numpy as np
import tensorflow as tf
import eel
from PIL import Image
import tensorflow.keras as keras
import os
from urllib import request
import dill as pickle



classes = { 0:'Speed limit: 20km/h',
            1:'Speed limit: 30km/h', 
            2:'Speed limit: 50km/h', 
            3:'Speed limit: 60km/h', 
            4:'Speed limit: 70km/h', 
            5:'Speed limit: 80km/h', 
            6:'End of speed limit: 80km/h', 
            7:'Speed limit: 100km/h', 
            8:'Speed limit: 120km/h', 
            9:'No overtaking', 
            10:'No overtaking for tracks', 
            11:'Right-of-way at intersection', 
            12:'Priority road', 
            13:'Yield', 
            14:'Stop', 
            15:'No vehicles', 
            16:'Trucks prohibited', 
            17:'No entry', 
            18:'General caution', 
            19:'Dangerous curve left', 
            20:'Dangerous curve right', 
            21:'Double curve left', 
            22:'Bumpy road', 
            23:'Slippery road', 
            24:'Road narrows on right', 
            25:'Road work', 
            26:'Traffic signals', 
            27:'Pedestrians', 
            28:'Children crossing', 
            29:'Bicycles crossing', 
            30:'Beware of ice',
            31:'Wild animals crossing', 
            32:'End speed and passing limits', 
            33:'Turn right ahead', 
            34:'Turn left ahead', 
            35:'Ahead only', 
            36:'Go straight or right', 
            37:'Go straight or left', 
            38:'Keep right', 
            39:'Keep left', 
            40:'Roundabout mandatory', 
            41:'End of no overtaking ', 
            42:'End of no overtaking for truck' }

#external method the UI calls in order to train a model
@eel.expose
def create_model(data_path, model_path, pickle_data): 
    try:
        warnings.filterwarnings('ignore')
        # np.random.seed(0)
        # tf.random.set_seed(0)

        #if the user wanted to used pickled data, this checks if such data exists.
        if(pickle_data and (os.path.isfile(data_path + '/pickle'))):
            try:
                eel.updateAction('Unpacking existing data', True)
                with open(data_path + '/pickle', 'rb') as f:
                    data = pickle.load(f)
                eel.nextStep()
            except:
                data = dh.process_data(data_path +"/")
        else:
            data = dh.process_data(data_path +"/")

        model = Model()
        model.build_model()
        model.train(data)

        loss, accuracy = model.evaluate(data)
        model.save(model_path)
        eel.showResults("{:.3f}".format(accuracy),"{:.3f}".format(loss))

    except Exception as e:
        print(e)
        eel.handleError("Failed to create model, please recheck your data and model paths")
    
#external method the UI calls in order to test a model
@eel.expose
def test_model(data_path, model_path, pickle_data):
    try:
        eel.updateAction("loading model", True)
        model = keras.models.load_model(model_path)

        #if the user wanted to used pickled data, this checks if such data exists.
        if(pickle_data and os.path.isfile(data_path + '/pickle')):
            try:
                eel.updateAction('Unpacking existing data', True)
                with open(data_path + '/pickle', 'rb') as f:
                    data = pickle.load(f)
                eel.nextStep()
                eel.nextStep()
            except:
                data = dh.process_data(data_path +"/")

        else:
            data = dh.process_data(data_path +"/")

        eel.updateAction('Evaluating', True)
        loss, accuracy = model.evaluate(data.x_test, data.y_test)    
        eel.showResults("{:.3f}".format(accuracy),"{:.3f}".format(loss))

    except Exception as e:
        eel.handleError("Failed to test model, please recheck your data and model paths")
        print(e)

#internal method called in order to predict an image.
def predict(img):
    print('predicting...')
    img.convert('RGB')
    img = img.resize((32,32))
    img.save("test.png", 'png')
    imgarr = np.array(img)
    imgarr = imgarr/255
    res = network.predict(np.array([imgarr]))

    return classes[res[0].tolist().index(res[0].max())]

#internal method called in order to convert image filetypes
def handle_other_filetypes(path):
        im = Image.open(path).convert('RGB')
        im.save('temp.png', 'png')
        os.remove(path)

#external method called by the UI in order to set the network to predict with
@eel.expose
def set_network(path):
    try:
        global network
        network = keras.models.load_model(path)
    except:
        eel.handleError("Failed to load model")


#external method called by the UI in order to predict an image.    
@eel.expose
def handle_and_predict(img_data_uri):
    if network is None:
        return 'Error;;Model not loaded.'
    try:
        header = img_data_uri.split("_", 1) #getting the image uri header
        ext = header[0].split('/')[1].split(';')[0] # getting the extention of the file

        #saving the file uri as a normal image file
        with request.urlopen(img_data_uri) as response:
            data = response.read()
        with open('temp.' + ext, 'wb') as stream:
            stream.write(data)

        if ext != 'png':
            handle_other_filetypes('temp.' + ext)
        
        class_str = predict(Image.open('temp.png'))
        os.remove('temp.png')

        return class_str
    except Exception as e:
        return 'Error;;' + str(e)

#external method called by the UI in order to check the validity of the model or data paths
@eel.expose
def check_paths(model_path = None, data_path = None):
    try:
        warnings = []
        if(model_path is not None and not os.path.isdir(model_path)):
            warnings.append('The model path does not lead to a valid directory')
        if(data_path is not None and not os.path.isdir(data_path)):
            warnings.append('The data path does not lead to a valid directory')
        elif(data_path is not None and not ( os.path.isdir(data_path + '/Train') or os.path.isfile(data_path + '/pickle'))):
            warnings.append('The data path does not appear to lead to the GTSRB dataset or a packed data file.')
        # elif(not checksumdir.dirhash(os.path.abspath("data")) == checksumdir.dirhash(data_path)):
        #     warnings.append('The data path does not appear to lead to the complete GTSRB dataset')
        return warnings
    except Exception as e:
        print(e)
        return ["Python errors occured, there could be an issue with the setup."]

if __name__ == "__main__":
    eel.init('frontend')
    eel.start('html/index.html')
