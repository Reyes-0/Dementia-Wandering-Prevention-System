import os, time, uuid
import cv2
import base64
import asyncio
from azure_blob_storage.blob_storage import upload_blob_file
from sinch_sms.sms_api import sms
from azure_custom_vision.model import prediction
from config import (
    azure_blob_storage_account_url,
    azure_blob_storage_credential,
    image_directory,
    image_name
)

def main():
    vid = cv2.VideoCapture(0) #chnage the camera/webcam accordingly
    global base64Frames
    base64Frames = []
    account_url = azure_blob_storage_account_url
    credential = azure_blob_storage_credential

    if not vid.isOpened():
        print("Error: Unable to open webcam.")
        exit()

    while True:
        ret, frame = vid.read()

        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Process the frame here (e.g., resize, convert color)
        processed_frame = frame  # Replace this with your processing logic

        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        
        cv2.imshow('frame', processed_frame)
        # Save the processed frame as an image file
        if len(base64Frames) % 30 == 0: #decided to do every 30th frame due to hardware restriction and to hasten prediction time
            
            directory = image_directory

    # Specify the filename of your image
            filename = image_name

            if not os.path.exists(directory):
                os.makedirs(directory)

            # Combine the directory and filename to get the full path of the image
            image_path = os.path.join(directory, filename)

            cv2.imwrite(image_path, processed_frame)
                    
            unique_classes = prediction(image_path)
        
            print("Classes detected:", unique_classes)
            print('\n')
            
            if 'patient' and 'nurse'  in unique_classes:
                print('No SMS')
                
            elif 'patient' in unique_classes:               
                await upload_blob_file(account_url, credential, "video", directory, filename)
                sms()
                time.sleep(1)

        if len(base64Frames) % 400 == 0:
            del base64Frames[:100]
        
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break


    vid.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    asyncio.run(main())