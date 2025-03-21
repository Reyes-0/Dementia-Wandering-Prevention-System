from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
from azure.identity.aio import DefaultAzureCredential
import os
from config import(
    model_ENDPOINT,
    model_prediction_key,
    model_project_id,
    model_publish_iteration_name,
    model_iteration_id,
    prediction_probability_threshold,
)

ENDPOINT = model_ENDPOINT
prediction_key = model_prediction_key
project_id = model_project_id
publish_iteration_name = model_publish_iteration_name
iteration_id = model_iteration_id

# trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

def prediction(image):
    classes=[]
    with open(os.path.join (image), "rb") as image_contents:
        results = predictor.detect_image(
            project_id, publish_iteration_name, image_contents.read())

        for prediction in results.predictions:
            if prediction.probability >= prediction_probability_threshold:
                classes.append(prediction.tag_name)
                print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, \
                    bbox.width = {3:.2f}, bbox.height = {4:.2f}".format(prediction.probability * 100, \
                        prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, \
                            prediction.bounding_box.height))
    print("\n")
    unique_classes = set(classes)
    return unique_classes