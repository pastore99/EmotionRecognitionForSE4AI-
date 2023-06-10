from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model, model_from_json
from keras import backend as K
import yaml
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

params = yaml.safe_load(open("params.yaml"))["test"]
seed = params["seed"]
testDataGenerator = ImageDataGenerator(rescale=1./255)
test_dir = "data/FER2013/test"
#batch size set to 64 because the whole set doesn't fit in memory
test_data = testDataGenerator.flow_from_directory(test_dir, batch_size=64, target_size=(48, 48), shuffle=False, color_mode='grayscale', class_mode='categorical', seed=seed)
# Load the model
with open('emotion_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)

model.load_weights('emotion_model.h5')
model.compile(loss='categorical_crossentropy', metrics=[f1_score])

#Evaluate model
loss, acc = model.evaluate(test_data)