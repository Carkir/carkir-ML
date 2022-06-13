# Carkir-ML

This repository contains the code to check the availibity of parking space which
is needed to generate output for Carkir project. The project aims to help its users
to find a vacant spot in a parking lot. 

Through research and exploration, we found one approach to the problem can be 
using CCTV to detect parking lot occupancy using OpenCV (Open Source Computer 
Vision) library in Python. 

## Overview
<!-- ![image](https://user-images.githubusercontent.com/105625833/173252399-09cd57d7-bc5e-4bd5-bac9-a2e9b68ce894.png) -->
![image](https://github.com/Carkir/carkir-ML/blob/064afc24740abf5a8ababb54b1c57b5b70a0e237/with_marking.jpg)

Program flow is as follows:
- We input a place name to get the video of it. From the video, we get 
a still image that can be proceeded.
- We then click 4 corners of each parking spot we want to track. Press 'esc' 
when all desired spots are marked.
- Video would start with boxes overlayed the video. Red box is meant for 
occupied spot, and green box is meant for available spot. In the video, we can 
also get how many available parking spot.

For this project, we first use a PKLot dataset and generate our own dataset.
We crop a few of occupied parking slot to get labeled as 'Occupied' and a few of
empty parking slot to get labeled as 'Empty'. From the datasets we create, we 
train our model and get 98% accuracy. Refers to [this code.](https://github.com/Carkir/carkir-ML/blob/for-apps/carkir_ModelGenerator.ipynb)

## Process
### Parking Slot Lining
First, after we get the video and a still image of parking lot. We would manually
draw rectangles to show which parking spots we are going to detect. 

<!-- ![image](https://user-images.githubusercontent.com/105625833/173252570-de8ff397-8407-4c73-93bf-f769ea779ab1.png) -->
![image](https://github.com/Carkir/carkir-ML/blob/064afc24740abf5a8ababb54b1c57b5b70a0e237/marked_spotBLK-HDPTZ12_1.jpg)
![image](https://github.com/Carkir/carkir-ML/blob/064afc24740abf5a8ababb54b1c57b5b70a0e237/marked_spotBrisk_Synergies_1.jpg)
![image](https://github.com/Carkir/carkir-ML/blob/064afc24740abf5a8ababb54b1c57b5b70a0e237/marked_spotTomas_Sak_1.jpg)

By clicking four corners of each parking spot we want to track, we automatically 
get the points of each spot that can be used to tell the exact place of its spot. After getting the points of each spot (data-slot repo), we convert the data into a json that will
POST to Android API (using requests library in Python).
```
file = open(json_name, "rb")
url = "https://android-api-btwe4mw5iq-et.a.run.app/ml/uploadSlot" #API Slot
response = requests.post(url, files={"file": file})
```

### Parking Slot Detection
We call back the points of each parking slots by using GET requests. Then, we 
examine the area of each retangle to see if whether there was a car in there or 
not. 

Here we need our training model to see there was a car in it or no. If the slot is
empty, it will show green box and occupancy data shows '1' which means it's empty.
If the slot is occupied, it will show red box and occupancy data shows '0' which
means there's a car in it.


The occupancy data then will be sent to Android API using POST requests. 
If there's a slight change in occupancy data, for example the occupied slot becomes
the empty slot, then the code automatically send the updated occupancy data to 
Android API.


## Directory Structure
1. **data-occupancy** folder contains json files, output of parking slot detection. There are 3 json files as we have three video.
2. **data-slot** folder contains json files, output of parking slot lining. The json shows points of each parking spot that has been marked.
3. **extract_detect** folder contains a bunch of final output images.
4. **parking_slot-lining** folder contains:
   - InputLocationCamera.py is to list down several camera into one folder and convert it into json.
   - Location-Camera.json is the output of InputLocationCamera.py
   - ExtractSetupImage.py is to generate the video from the camera and a still image from it.
   - SetupParkingSlot.py is to mark parking spot.
5. **setup_image** is the output of ExtractSetupImage.py and the input of SetupParkingSlot.py
6. **slot-detection** folder contains main code that will generate the final output of this project. There are 3 different code from 3 different place.
7. **Dockerfile** is for deployment.
8. **carkir_ModelGenerator.ipynb** is the training for our model with the dataset we create by ourselves from PKLot dataset.
9. **marked_spotTomas_Sak_1.jpg** is the example image of a still image we mark for slot line.
10. **requirements.txt** contains the main requirements for this project include:
    - Tensorflow
    - Tensorflow-keras
    - Python-OpenCV
    - Requests
    - etc.
 
 ## Branches in this repository
 There are 3 branch in this carkir-ML repository
    - for-apps, consist codes of the code and marking output to see the detection output but not for deployment
    - for-deployment, consist the needed codes, files, and images needed for deployment
    - for-development, consist of machine learning detection model generator and the datasets used
 


