# !pip install nemo_toolkit['all']

from fastapi import FastAPI
import time

from imageai.Classification import ImageClassification
import os
import torch
import torchvision.models as models

execution_path = os.getcwd()

# Download and save the ResNet50 model
model = models.resnet50(pretrained=True)
torch.save(model.state_dict(), os.path.join(execution_path, "resnet50-19c8e357.pth"))

# Create an instance of ImageClassification
prediction = ImageClassification()
prediction.setModelTypeAsResNet50()

# Load the ResNet50 model
prediction.setModelPath(os.path.join(execution_path, "resnet50-19c8e357.pth"))
prediction.loadModel()

input_path = "D:\\AI\\OpenAI\\Pictures\\Normolized\\"

app = FastAPI()

@app.get("/")
def get_image_type(query):
    a = time.time()
    responce = "Nan"
    
    # Classify the image
    # predictions, probabilities = prediction.classifyImage(os.path.join(execution_path, f'{query}.jpg'), result_count=5)
    predictions, probabilities = prediction.classifyImage(os.path.join(input_path, f'{query}.jpg'), result_count=5)
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        if eachPrediction == "mailbag":
            responce = eachPrediction, ":", eachProbability
            print(responce)   
    
    return {"status": "success", "responce": responce, "executionTime": f"{round((time.time() - a) * 1000, 2)} ms"}