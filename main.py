import cv2
import numpy as np
import csv
import os
import time

class Traffic_Analyzer:

    def __init__(self, video_path):
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.COLOUR = (50, 200, 0)
        self.max_frames = 10
        self.video_path = video_path
        self.dir_path = os.path.dirname(self.video_path)
        self.output_video_file = ""
        self.output_csv_file = ""
        self.yolo_weights = "IO_Project/yolov3.weights"
        self.yolo_cfg = "IO_Project/yolov3.cfg"
        self.coco_names = "IO_Project/coco.names"
        # self.yolo_weights = "yolov3-tiny_final.weights"
        # self.yolo_cfg = "yolov3_tiny.cfg"
        # self.coco_names = "coco_tiny.names"
        #self.yolo_weights = "yolov3_320.weights"
        #self.yolo_cfg = "yolov3_320.cfg"

    def video_analyze(self):

        t = time.localtime()
        self.current_time = time.strftime("%H_%M_%S", t)
        self.output_video_file = self.current_time + "_" + os.path.split(self.video_path)[1]

        net = cv2.dnn.readNet(self.yolo_weights, self.yolo_cfg)
        classes = []
        with open(self.coco_names, "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layers_names = net.getLayerNames()
        layers_output = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        video = cv2.VideoCapture(self.video_path)

        result = cv2.VideoWriter(self.output_video_file,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 10, (int(video.get(3)), int(video.get(4))))

        self.total_vehicles = []
        self.total_unknown = []
        self.total_cars = []
        self.total_trucks = []
        self.total_two_wheelers = []

        self.frame = 0
        while self.frame < self.max_frames:
            self.frame+=1
            unknown_number = 0
            vehicles_number = 0
            cars_number = 0
            two_wheelers_number = 0
            trucks_number = 0

            if self.frame%3 == 1:
                success, img = video.read()

                blob_results = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, False)
                img_height, img_width, img_channels = img.shape
                net.setInput(blob_results)
                outs = net.forward(layers_output)

                class_ids = []
                confidences = []
                boxes = []


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

                if class_ids[i] in [0, 1, 2, 3, 5, 7]:
                    vehicles_number += 1
                    x, y, width, height = boxes[i]
                    label = classes[class_ids[i]].upper()
                    conf = str(round(confidences[i] * 100, 1)) + "%"
                    cv2.rectangle(img, (x, y), (x + width, y + height), self.COLOUR, 2)
                    cv2.putText(img, label, (x + 5, y + 15), self.FONT, 0.5, self.COLOUR, 1)
                    cv2.putText(img, conf, (x + 5, y + height - 5), self.FONT, 0.5, self.COLOUR, 1)
                if class_ids[i] == 0:
                    unknown_number += 1
                if class_ids[i] in [1, 3]:
                    two_wheelers_number += 1
                elif class_ids[i] == 2:
                    cars_number += 1
                elif class_ids in [5, 7]:
                    trucks_number += 1

            self.total_vehicles.append(vehicles_number)
            self.total_cars.append(cars_number)
            self.total_trucks.append(trucks_number)
            self.total_two_wheelers.append(two_wheelers_number)
            self.total_unknown.append(unknown_number)

            cv2.putText(img, str(self.frame), (20, 20), self.FONT, 0.5, self.COLOUR, 2)
            # cv2.imshow("Video", img)
            result.write(img)
            print(".", end='')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        result.release()
        cv2.destroyAllWindows()



    def write_timestamps(self):

        self.output_csv_file = self.current_time + "_" + os.path.split(self.video_path)[1].split(".")[0] + ".csv"
        cameraCapture = cv2.VideoCapture(self.video_path)

        success, frame = cameraCapture.read()
        fps = cameraCapture.get(cv2.CAP_PROP_FPS)

        total_timestamp = []

        count = 0
        while success:
            if cv2.waitKey(1) == 27:
                break
            success, frame = cameraCapture.read()
            count += 1
            time_stamp = count/fps
            total_timestamp.append(time_stamp)

        cv2.destroyAllWindows()
        cameraCapture.release()

        with open(self.output_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp klatki", "liczba pojazdów", "liczba samochodów", "liczba jednośladów", "liczba samochodów wielkogabarytowych", "liczba obiektów nierozpoznanych"])
            for i in range(len(self.total_vehicles)):
                writer = csv.writer(file)
                writer.writerow([total_timestamp[i], self.total_vehicles[i], self.total_cars[i], self.total_two_wheelers[i], self.total_trucks[i], self.total_unknown[i]])

    def get_current_analysis_state(self):
        x = round(self.frame/self.max_frames)
        return x
