# EmotionRecognitionForSE4AI-BeHappy
We aim to create a DL based system that uses a FER (Facial Emotion Recognition) model to assist a teacher's ability to assess students' emotions felt during the course of a lecture. We hope that by making the teacher more aware of possible negative feelings arising from students that him or her can act upon the reasons why students are feeling in a certain way (ex. prompting students to ask questions or explain a previously made argument more clearly).
# Dependencies
If anyone wants to contribute to better the scope or features of this system, then once you clone this project make sure to have python >= 3.10 installed. We are running our project using the IDE PyCharm, but the experience might be the same with any other IDE.
To run the development environment we additionally require you to download the following dependencies.
````
pip install flask
pip install tensorflow
pip install keras
pip install dvc[gdrive]
````
The following commands will download the latest versions of the libraries, in case of future incompatibility issues we report that the versions of the libraries we used are the following
- flask: 2.3.2
- tensorflow: 2.12.0
- keras: 2.12.0
- dvc[gdrive]: 2.58.1

The last library DVC (Data Version Control) is actually a versioning tool for datasets and ML models that works alongside Git and GitHub. We are using DVC to version the FER2013 dataset publicly available on kaggle at the following link:

````
https://www.kaggle.com/datasets/msambare/fer2013
````

The version of DVC that we are using allows us to use a Google Drive folder as a data repository that can be easily shared among all team members of our project. If it is necessary to show the contents of the data repository, please ask any of the team members for the necessary credentials. Otherwise, download the dataset and train your own model!

# GitHub Work-Flow

All development activities must be performed on the "development" branch. All development related work must be appropriately tracked via the GitHub Issues mechanism. Therefore, if any feature or bug must be resolved, we will:
- create an issue
- specify the issue number when committing

If deemed necessary (ex. to not hinder development of other features), we might create a short-lived branch for specific feature or bug. At the end of the development stage, we will align the "development" and main branches.  