import os
import shutil

import cv2
import yaml
from dvclive.keras import DVCLiveCallback
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.optimizers import Adam
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator

def recall_metric(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_metric(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_score(y_true, y_pred):
    precision = precision_metric(y_true, y_pred)
    recall = recall_metric(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


params = yaml.safe_load(open("params.yaml"))["train"]
seed = params["seed"]
n_epoch = params["n_epoch"]
learning_rate = params["learning_rate"]
decay = params["decay"]
batch_size = params["batch_size"]
# Initialize image data generator with rescaling
train_data_gen = ImageDataGenerator(rescale=1./255,          # rescale matrix values
                                    rotation_range=10,       # randomly rotate images by 10 degrees
                                    zoom_range=0.05,         # randomly zoom images by up to 20%
                                    horizontal_flip=True,    # randomly flip images horizontally
                                    fill_mode="constant",
                                    cval=0,
                                    validation_split=0.2)

training_data = train_data_gen.flow_from_directory("data/preprocessed/train", batch_size=64, target_size=(48, 48), shuffle=True, color_mode='grayscale', class_mode='categorical', subset='training',seed=seed)
validation_set = train_data_gen.flow_from_directory("data/preprocessed/train", batch_size=64, target_size=(48, 48), shuffle=True, color_mode='grayscale', class_mode='categorical', subset='validation', seed=seed-1)
# create model structure
emotion_model = Sequential()

emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))

emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))

print(type(decay), type(learning_rate))

cv2.ocl.setUseOpenCL(False)

emotion_model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=learning_rate, decay=float(decay)), metrics=[f1_score])

# Train the neural network/model
emotion_model_info = emotion_model.fit_generator(
        training_data,
        steps_per_epoch=training_data.n // batch_size,
        epochs=n_epoch,
        validation_data=validation_set,
        validation_steps=validation_set.n // batch_size,
        callbacks=[DVCLiveCallback()]
)

# save model structure in jason file
if not os.path.exists("model"): os.mkdir("model")
if os.listdir('model').__contains__('emotion_model.h5'):
    os.remove('model/emotion_model.json')
    os.remove('model/emotion_model.h5')

model_json = emotion_model.to_json()
with open("model/emotion_model.json", "w") as json_file:
    json_file.write(model_json)

# save trained model weight in .h5 file
emotion_model.save_weights('model/emotion_model.h5')