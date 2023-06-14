import shutil
import sys
import os

import cv2
import yaml
from operator import itemgetter
from PIL import Image
import numpy as np
import imgaug.augmenters as iaa

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython prepare.py data-file\n")
    sys.exit(1)

augmenter = iaa.SomeOf([
    iaa.Affine(rotate=(-10, 10)),
    iaa.Fliplr(0.5),
    iaa.GaussianBlur(sigma=(0, 1.0))
])
data_dir = os.path.join("data", "FER2013", "train")
test_dir = os.path.join("data", "FER2013", "test")
params = yaml.safe_load(open("params.yaml"))["prepare_phase"]
seed = params["seed"]

preprocessed_folder = os.path.join("data", "preprocessedV1")
out_train = os.path.join("data", "preprocessedV1", "train")
out_test = os.path.join("data", "preprocessedV1", "test")
if os.path.exists(preprocessed_folder):
    shutil.rmtree(preprocessed_folder)

shutil.copytree(data_dir, out_train)
shutil.copytree(test_dir, out_test)

#compute directory with most examples and remove from candidate augmentation
category_folders = [os.path.join(out_train, x) for x in os.listdir(data_dir)]
category_tuples = [(x, len(os.listdir(x))) for x in category_folders]
max_category = max(category_tuples, key=itemgetter(1))

category_tuples.remove(max_category)

for folder_tuple in category_tuples:

    folder = folder_tuple[0]
    numImgs = folder_tuple[1]
    numToMaxImgs = max_category[1]-numImgs

    print("--- sono in cartella "+folder+"---")
    images = []
    for file_path in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, file_path))
        images.append(img)

    images = np.array(images)
    augmented_images = augmenter(images=images,seed=seed)

    for i, augmented_image in enumerate(augmented_images):
        file_name = os.path.join(folder, f"augmented_image_{i}.jpeg")
        cv2.imwrite(file_name, augmented_image)

    print("--- finito preprocessing " + folder + "---")