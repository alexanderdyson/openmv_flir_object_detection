# Object detection FLIR ADAS
#
# This project uses a pre-trained TFlite model.

import sensor
import image
import time
import os
import tf
import json
import ubinascii
from mqtt_publisher import AWSIOTCoreMQTTClient

sensor.reset()
# Set grayscale with 120x160 size
sensor.set_color_palette(sensor.PALETTE_IRONBOW)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)

labels = {
    0: "bicycle",
    1: "car",
    2: "dog",
    3: "person"
}

ssid = ''  # Network ssid
key = ''  # Network key
key_path = ''
cert_path = ''
server = ''
client_id = "openmvboard"
mqtt_topic = "OpenMVModel"


net = tf.load("best_float.tflite", load_to_fb=True)
print("Loaded model" % (net))


mqtt_client = AWSIOTCoreMQTTClient(ssid, key, key_path, cert_path, client_id, server)
print("MQTT client instantiated")


clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # default settings just do one detection... change them to search the image...
    for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        scores = net.classify(img, roi=obj)[0].output()
        max_idx = scores.index(max(scores))
        print("Object: %s = %f" % (labels[max_idx], scores[max_idx]))
        img.draw_rectangle(obj, color=(255,0,0))
        img.draw_string(obj[0] + 3, obj[1] - 1, labels[max_idx], mono_space=False, color=(255,0,0))

        # Send data to AWS IOT Core VIA MQTT
        data = {"timestamp": time.time(), "object": LABELS[max_idx], "score": scores[max_idx]}

        mqtt_client.publish(mqtt_topic, json.dumps(data))

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    print(clock.fps())
