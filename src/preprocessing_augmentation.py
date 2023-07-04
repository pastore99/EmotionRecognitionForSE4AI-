from keras.preprocessing.image import ImageDataGenerator
from keras.utils.image_utils import img_to_array, array_to_img, load_img
import shutil
import yaml
import os
def disgust_aug(filename, path, datagen):
    file_stem=filename.split('.')[0]
    img = load_img(path)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    print(f'{filename} is being augmented')
    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir="data/preprocessed/train/disgust", save_prefix=f'aug_{file_stem}', save_format='jpg', seed=seed):
        i += 1
        if i > 8:  # generate 10 augmented images
            break
    print(f'{filename} has been augmented')


data_dir = os.path.join("data", "FER2013", "train")
test_dir = os.path.join("data", "FER2013", "test")
params = yaml.safe_load(open("params.yaml"))["prepare_phase"]
seed = params["seed"]

preprocessed_folder = os.path.join("data", "preprocessed")
out_train = os.path.join("data", "preprocessed", "train")
out_test = os.path.join("data", "preprocessed", "test")
if os.path.exists(preprocessed_folder):
    shutil.rmtree(preprocessed_folder)
print('inizio copia del dataset')
shutil.copytree(data_dir, out_train)
shutil.copytree(test_dir, out_test)
print('fine copia del dataset')

datagen = ImageDataGenerator(
    rotation_range=20,      # randomly rotate images by 20 degrees
    zoom_range=0.1,         # randomly zoom images by up to 20%
    horizontal_flip=True,    # randomly flip images horizontally
    fill_mode="constant",
    cval=0
)

for filename in os.listdir('data/FER2013/train/disgust/'):
    disgust_aug(filename, os.path.join('data/preprocessed/train/disgust/', filename), datagen)