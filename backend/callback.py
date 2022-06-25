import tensorflow.keras as keras
import eel

#callback that updates the UI while the model is training.
class eelCallback(keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        eel.updateAction("Training Epoch " + str(epoch))

    def on_epoch_end(self, epoch, logs=None):
        eel.updateStats("{:.3f}".format(logs['val_accuracy']),"{:.3f}".format(logs['val_loss']))

    def on_train_batch_end(self, batch, logs=None):
        eel.updateProgress(batch, 980)

    def on_train_end(self, logs=None):
        eel.nextStep()
    