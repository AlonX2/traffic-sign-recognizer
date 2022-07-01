import tensorflow.keras as keras
from keras.layers import Conv2D, MaxPool2D, Dense, Dropout, Flatten, BatchNormalization
import eel
from callback import eelCallback
 
class Model:
    def __init__(self, model = None):
        self.model = model
    
    #method that builds and compiles the model
    def build_model(self):
        model = keras.models.Sequential()
        model.add(Conv2D(filters=32, kernel_size= (5,5), strides=2, activation='relu', padding='same', input_shape=(30,30,3)))
        model.add(MaxPool2D((2,2), padding='valid'))
        model.add(Dropout(0.2))

        model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
        model.add(MaxPool2D((2,2), padding='valid'))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dense(512, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(43, activation='softmax'))

        model.summary()

        self.model = model
        eel.updateProgress(5, 5)
        eel.nextStep()
        self.compile()

    #internal method thath compiles the model with sgd optimizer and categorical crossentropy loss
    def compile(self):
        print("Compiling model...")
        self.model.compile(optimizer='sgd',
             loss='categorical_crossentropy',
             metrics = ['accuracy'])
    
    #method to start training the model with an early stopping callback and a custom UI update callback
    def train(self, data):
        print("stating training...")
        earlystop_cb = keras.callbacks.EarlyStopping(patience=15, restore_best_weights =True) 
        self.model.fit(data.x_train, data.y_train, epochs=100, validation_data=(data.x_val, data.y_val), callbacks=[earlystop_cb, eelCallback()])

    #method to evaluate the model
    def evaluate(self, data):
        eel.updateAction("Evaluating", True)
        loss, accuracy = self.model.evaluate(data.x_test, data.y_test)
        print(f'Loss = {loss:.2f}\naccuracy = {accuracy*100:.2f}%')
        # eel.evalStateUpdate(1, ["{:.3f}".format(accuracy),"{:.3f}".format(loss) ])
        return loss, accuracy

    #wrapper method to save the model
    def save(self, path):
        self.model.save(path)

        



