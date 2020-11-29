import cv2
import numpy as np
import csv
import os

FONT = cv2.FONT_HERSHEY_SIMPLEX
COLOUR = (50, 200, 0)


def video_analyze(video_path):

    #yolo_weights = "yolov3-tiny_final.weights"
    #yolo_cfg = "yolov3_tiny.cfg"
    #coco_names = "coco_tiny.names"
    yolo_weights = "yolov3.weights"
    yolo_cfg = "yolov3.cfg"
    coco_names = "coco.names"

    net = cv2.dnn.readNet(yolo_weights, yolo_cfg)

    classes = []
    with open(coco_names, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layers_names = net.getLayerNames()
    layers_output = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    video = cv2.VideoCapture(video_path)

    result = cv2.VideoWriter('output.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             10, (int(video.get(3)), int(video.get(4))))

    total_vehicles = []
    total_cars = []
    total_trucks = []
    total_two_wheelers = []

    frame = 0
    while frame < 100:
        frame+=1
        success, img = video.read()

        blob_results = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, False)
        img_height, img_width, img_channels = img.shape
        net.setInput(blob_results)
        outs = net.forward(layers_output)

        class_ids = []
        confidences = []
        boxes = []

        vehicles_number = 0
        cars_number = 0
        two_wheelers_number = 0
        trucks_number = 0

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detevted
                    center_x = int(detection[0] * img_width)
                    center_y = int(detection[1] * img_height)
                    width = int(detection[2] * img_width)
                    height = int(detection[3] * img_height)

                    #  Rectangle
                    x = int(center_x - width / 2)
                    y = int(center_y - height / 2)

                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)
        for i in indexes:
            i = int(i)

            #if class_ids[i] in [1, 2, 3, 7]:
            if class_ids[i] in [0,1,2]:
                vehicles_number += 1
                x, y, width, height = boxes[i]
                label = classes[class_ids[i]].upper()
                conf = str(round(confidences[i] * 100, 1)) + "%"
                cv2.rectangle(img, (x, y), (x + width, y + height), COLOUR, 2)
                cv2.putText(img, label, (x + 5, y + 15), FONT, 0.5, COLOUR, 1)
                cv2.putText(img, conf, (x + 5, y + height - 5), FONT, 0.5, COLOUR, 1)
            if class_ids[i] in [1, 3]:
                two_wheelers_number += 1
            elif class_ids[i] == 2:
                cars_number += 1
            elif class_ids == 7:
                trucks_number += 1

        total_vehicles.append(vehicles_number)
        total_cars.append(cars_number)
        total_trucks.append(trucks_number)
        total_two_wheelers.append(two_wheelers_number)

        cv2.putText(img, str(frame), (20, 20), FONT, 0.5, COLOUR, 2)
        # cv2.imshow("Video", img)
        result.write(img)
        print(".", end='')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    result.release()
    cv2.destroyAllWindows()

    write_timestamps(video_path, total_vehicles, total_cars, total_two_wheelers, total_trucks)


def write_timestamps(video_path, vehicles, cars, two_wheelers, trucks):
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    calc_timestamps = [0.0]

    while (cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC))
            calc_timestamps.append(calc_timestamps[-1] + 1000 / fps)
        else:
            break

    cap.release()"""

    cameraCapture = cv2.VideoCapture(video_path)

    success, frame = cameraCapture.read()
    fps = cameraCapture.get(cv2.CAP_PROP_FPS)

    total_timestamp = []

    count = 0
    #with open('protagonist.csv', 'w', newline='') as file:
    while success:
        if cv2.waitKey(1) == 27:
            break
        success, frame = cameraCapture.read()
        count += 1

        """milliseconds = cameraCapture.get(cv2.CAP_PROP_POS_MSEC)

        seconds = milliseconds // 1000
        milliseconds = milliseconds % 1000
        minutes = 0

        if seconds >= 60:
            minutes = seconds // 60
            seconds = seconds % 60

        if minutes >= 60:
            minutes = minutes % 60

        time_stamp = str(int(minutes)) + ":" + str(int(seconds)) + ":" + str(int(milliseconds))"""
        time_stamp = count/fps


        total_timestamp.append(time_stamp)
            #writer = csv.writer(file)
            #writer.writerow([time_stamp])
    cv2.destroyAllWindows()
    cameraCapture.release()

    with open('time_stamp.csv', 'w', newline='') as file:
        #for i in len(total_timestamp):
        for i in range(9):
            writer = csv.writer(file)
            writer.writerow([total_timestamp[i], vehicles[i], cars[i], two_wheelers[i], trucks[i]])
