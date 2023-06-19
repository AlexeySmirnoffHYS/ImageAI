import datetime
import time
import VideoFrameCapture
import uuid
import os
import Norm
import shutil

work_flag = True
start_time = datetime.time(11, 55)
stop_time = datetime.time(12, 30)
match_count = 0

# Download ANN
from imageai.Classification import ImageClassification
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

while True:
    current_time = datetime.datetime.now().time()
          
    while work_flag:        
        if current_time > stop_time:
            break           

        if current_time >= start_time and current_time <= stop_time and datetime.datetime.now().weekday() < 5:
            # Get frame from flow
            url = "rtsp://192.168.11.16"  # URL stream flow
            filename = f'{datetime.datetime.now()}.jpg'.replace(":", "_")
            output_filename = os.path.join(os.getcwd(), f'Pictures\\Source\\{filename}')              
            VideoFrameCapture.capture_frame(url, output_filename)         
                        
            # Crop the frame
            input_image_path = output_filename
            output_image_path = os.path.join(os.getcwd(), f'Pictures\\Normolized\\{filename}')
            left = 501
            top = 85
            right = 786
            bottom = 190
            Norm.crop_image(input_image_path, output_image_path, left, top, right, bottom)
            
            # Classify the image            
            predictions, probabilities = prediction.classifyImage(output_image_path, result_count=5)
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                if eachPrediction == "mailbag" or eachPrediction == "punching bag" or eachPrediction == "bulletproof vest":
                    responce = eachPrediction, ":", eachProbability
                    print(responce) 
                    match_count += 1  
                    break            
            
            print("---")
            for eachPrediction, eachProbability in zip(predictions, probabilities):
                responce = eachPrediction, ":", eachProbability
                print(responce)
            print("---")                
                        
            if match_count >= 3:
                match_count = 0                
                source_file = input_image_path
                destination_folder = os.path.join(os.getcwd(), 'Pictures\\Matched\\')
                shutil.copy(source_file, destination_folder) 
                work_flag = False

            if not work_flag:               
                break      
            
        time.sleep(30) # Waitin 30 seconds
        current_time = datetime.datetime.now().time()
   
    # Получаем следующий рабочий день
    next_datetime = datetime.datetime.now()  
    next_datetime += datetime.timedelta(days=1)
    # If next_datetime is saturday or sunday
    while next_datetime.weekday() >= 5:  # 5 и 6 соответствуют субботе и воскресенью
        next_datetime += datetime.timedelta(days=1)
    # Изменяем время на start_time
    next_datetime = next_datetime.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
    
    # Расчет времени до следующего запуска
    time_delta = (next_datetime - datetime.datetime.now()).total_seconds()
    
    print(time_delta)
    print(f'Next day to start is {datetime.datetime.now() + datetime.timedelta(seconds=time_delta)}')

    # Задержка до следующего запуска
    time.sleep(time_delta)
    work_flag = True
