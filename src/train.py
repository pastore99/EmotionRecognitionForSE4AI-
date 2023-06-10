import os
import shutil

import cv2
import yaml
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
train_data_gen = ImageDataGenerator(rescale=1./255)  #prende ogni valore nella matrice i/255
validation_data_gen = ImageDataGenerator(rescale=1./255)


# Preprocess all test images
train_generator = train_data_gen.flow_from_directory(
        'data/FER2013/train',
        target_size=(48, 48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical',
        seed=seed)


# Preprocess all train images
validation_generator = validation_data_gen.flow_from_directory(
        'data/FER2013/test',
        target_size=(48, 48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical',
        seed=seed)
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

cv2.ocl.setUseOpenCL(False)

print(type(decay), type(learning_rate))


emotion_model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=learning_rate, decay=float(decay)), metrics=[f1_score])

# Train the neural network/model
emotion_model_info = emotion_model.fit_generator(
        train_generator,
        steps_per_epoch=28709 // batch_size,
        epochs=n_epoch,
        validation_data=validation_generator,
        validation_steps=7178 // batch_size)

# save model structure in jason file
if os.path.exists("model"): shutil.rmtree("model")

os.mkdir("model")
model_json = emotion_model.to_json()
with open("model/emotion_model.json", "w") as json_file:
    json_file.write(model_json)

# save trained model weight in .h5 file
emotion_model.save_weights('model/emotion_model.h5')