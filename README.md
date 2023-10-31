## Object Detection Project  


An object detection project that utilizes a FLIR Lepton 3.5 thermal sensor that detects people, dogs, cars, and bicycles, run the captured images through a TensorFlow lite model on a low-power microcontroller, and post the results to AWS cloud.

### Getting Started

#### Dependencies

* Hardware requirements
    * FLIR Lepton 3.5 
    * [OpenMV Cam H7 Plus](https://openmv.io/products/openmv-cam-h7-plus)
    * [WiFi Shield](https://openmv.io/products/wifi-shield-1)
* Pretrained Yolov8 model on a custom FLIR ADAS dataset, converted to TensorFlow lite
* AWS IoT Core
    * A topic `OpenMVModel` (`mqtt_topic` variable in `main.py`)
    * A rule with an action that dumps data in this topic to an S3 bucket
    * AWS IoT Certificates

#### Installing

##### Steps:

1. AWS Iot Core
  * Create an AWS Iot Thing
  * Create and attach an AWS IoT Policy to the Thing
  * An S3 bucket with a rule that dumps the data published from Thing via MQTT
    
2. Load AWS certificates and keys to the OpenMV board
3. Load the custom TensorFlow lite model to the OpenMV board
4. Update the following constants in the `main.py` file
    * `ssid`: Network ssid that is accessable to the board
    * `key`: Security key for the netowrk
    * `key_path`: Path to the file containing ssl key
    * `cert_path`: Path to the file containing ssl certificate
5. Load `main.py` and `mqtt_publisher.pq` scripts to the OpenMV board. These should be stored in the root folder.



#### Executing

Use [OpenMV](https://docs.openmv.io/openmvcam/tutorial/openmvide_overview.html) IDE to execute the `main.py` script.



### Credits
https://www.cardinalpeak.com/blog/building-edge-ml-ai-applications-using-the-openmv-cam
