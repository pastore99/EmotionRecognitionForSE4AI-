from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
from dvclive import Live
from sklearn.metrics import precision_score, recall_score, classification_report, f1_score
import yaml
import numpy as np

params = yaml.safe_load(open("params.yaml"))["test"]
seed = params["seed"]
testDataGenerator = ImageDataGenerator(rescale=1./255)
test_dir = "data/preprocessed/test"
#batch size set to 64 because the whole set doesn't fit in memory
test_data = testDataGenerator.flow_from_directory(test_dir, target_size=(48, 48), shuffle=False, color_mode='grayscale', class_mode='categorical', seed=seed)
# Load the model
with open('model/emotion_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)

model.load_weights('model/emotion_model.h5')
model.compile(loss='categorical_crossentropy', metrics=[f1_score])

#Evaluate model
print(test_data.n)
predictions = model.predict_generator(test_data)
predicted_labels = np.argmax(predictions, axis=1)

# Get true labels
true_labels = test_data.classes
class_labels = list(test_data.class_indices.keys())

#extract overall metrics
f1_score = f1_score(y_true=true_labels, y_pred=predicted_labels, average="micro")
precision = precision_score(y_true=true_labels, y_pred=predicted_labels, average="macro")
recall = recall_score(y_true=true_labels, y_pred=predicted_labels, average="macro")
report = classification_report(y_true=true_labels, y_pred=predicted_labels, target_names=class_labels, output_dict=True)

with Live(resume=True) as live:
    live.summary = live.read_latest()
    live.summary['test'] = {}
    live.summary['test']['precision'] = precision
    live.summary['test']['recall'] = recall
    live.summary['test']['f1_score'] = f1_score

    live.log_sklearn_plot("confusion_matrix", true_labels, predicted_labels)

with Live(dir="dvc_extra_metrics") as live:
    live.summary['test_report'] = report