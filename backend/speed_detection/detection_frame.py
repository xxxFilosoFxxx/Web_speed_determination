# pylint: disable=E0401, R0902, R0913, R0914, C0103, W0613, W0603
"""Основной функционал для распознавания и подсчета скорости объекта."""
# import threading
# from datetime import datetime
import os

from backend.app import app
from backend.speed_detection.idtracker.centroid_tracker import CentroidTracker
from backend.speed_detection.idtracker.trackable_object import TrackableObject
from backend.speed_detection.search_speed import SearchSpeed
from cv2 import cv2
import dlib
from imutils.video import FPS
import numpy as np


# процент распознавания
PERCENT = os.environ.get('PERCENT', 0.75)
# интервал времени, в котором выполняется поиск скорости
TIME = os.environ.get('TIME', 1)

# блокировка для передачи данных в поток
# LOCK = threading.Lock()


class DetectionPeople:
    """
    Основной класс для определения скорости объектов
    -> в реальном времени
    -> с сохранением в видеофайл
    """

    def __init__(self, video):
        self.cap = cv2.VideoCapture(video)
        path_prototxt = os.path.abspath(app.config['APP_DIR']) + '/MobileNetSSD/MobileNetSSD_deploy.prototxt'
        path_caffemodel = os.path.abspath(app.config['APP_DIR']) + '/MobileNetSSD/MobileNetSSD_deploy.caffemodel'

        self.net = cv2.dnn.readNetFromCaffe(str(path_prototxt),
                                            str(path_caffemodel))
        self.class_name = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird',
                           4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat',
                           9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog',
                           13: 'horse', 14: 'motorbike', 15: 'person', 16: 'pottedplant',
                           17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}
        self.percent = PERCENT
        self.centroids = SearchSpeed()
        self.frame_count = 0
        self.people_count = 0
        self.skip_frames = self.cap.get(cv2.CAP_PROP_FPS)
        # self.ret, self.frame = self.cap.read()
        # self.output_frame = self.frame
        # threading.Thread(target=self.translation_video, args=(filename,), daemon=True).start()

    def search_people(self, width, height, out, rgb, trackers):
        """
        Основная функция для детектирования объектов
        по назначенным классам
        """
        for i in range(0, out.shape[2]):
            confidence = out[0, 0, i, 2]
            if confidence > self.percent:
                class_id = int(out[0, 0, i, 1])
                if self.class_name[class_id] != "person":
                    continue

                # вычислить координаты ограничительной рамки для объекта
                box = out[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x_left_bottom, y_left_bottom, x_right_top, y_right_top) = box.astype("int")
                # Создаем прямоугольник объекта с помошью dlib из ограничивающего
                # Поле координат, а затем запустить корреляцию dlib трекер
                tracker_id = dlib.correlation_tracker()
                rect = dlib.rectangle(x_left_bottom, y_left_bottom, x_right_top, y_right_top)
                tracker_id.start_track(rgb, rect)
                # Добавить трекер в наш список трекеров, чтобы мы могли
                # Использовать его во время пропуска кадров
                trackers.append(tracker_id)

    @staticmethod
    def status_tracking(rect, rgb, frame, trackers):
        """
        Функция позволяет обновить позицию
        отслеживаемых объектов
        """
        for tracker in trackers:
            # Обновить трекер и получить обновленную позицию
            tracker.update(rgb)
            position = tracker.get_position()
            # Позиция объекта
            x_left_bottom, x_right_top = int(position.left()), int(position.right())
            y_left_bottom, y_right_top = int(position.top()), int(position.bottom())
            # добавить координаты ограничивающего прямоугольника в список прямоугольников
            rect.append((x_left_bottom, y_left_bottom, x_right_top, y_right_top))
            cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top),
                          (0, 255, 0))  # Определение контура человека

    def object_and_speed(self, filename, objects, frame, matrix, ratio_width):
        """
        Функция осуществляет отслеживание, идентификацию,
        подсчет скорости объектов и вывод инфо в заданный файл
        """
        # Добавление центроидов каждую секунду (или TIME) в упорядоченный словарь для нахождения скорости
        if self.frame_count % (self.skip_frames * TIME) < 1:
            self.centroids.save_centroids(objects)
        # цикл по отслеживанию объектов
        for (idx, (object_id, centroid)) in enumerate(objects.items()):
            # проверить, существует ли отслеживаемый объект для текущего идентификатора объекта
            add_object = self.centroids.track.get(object_id, None)
            # если не существует отслеживаемого объекта, создаем его
            if add_object is None:
                add_object = TrackableObject(object_id, centroid)
            else:
                add_object.centroids.append(centroid)
                if not add_object.counted:  # проверяем, был ли объект подсчитан
                    add_object.counted = True

            self.centroids.track[object_id] = add_object
            self.people_count = int(object_id + 1)
            cv2.putText(frame, str(object_id + 1), (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 5, (0, 0, 255), -1)

            # TODO: лучше настроить отслеживание объектов
            if self.frame_count % (self.skip_frames * TIME) < 1 or \
                    object_id not in self.centroids.speed:
                self.centroids.search_delta_speed(object_id, matrix, ratio_width)
                if self.frame_count % (self.skip_frames * TIME) < 1:
                    self.centroids.save_speed(filename, round(self.frame_count / self.skip_frames),
                                              object_id, self.centroids.speed[object_id])

            speed_label = str("%d" % self.centroids.speed[object_id]) + " km/hr"
            speed_label_size, base_line = cv2.getTextSize(speed_label,
                                                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            y_left_bottom = max(centroid[1], speed_label_size[1])
            cv2.rectangle(frame,
                          (centroid[0] + 50, centroid[1] - speed_label_size[1] - 100),
                          (centroid[0] - speed_label_size[1] - 35,
                           y_left_bottom + base_line - 100),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, speed_label, (centroid[0] - 50, y_left_bottom - 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
            info = "time {}: ID {}: {}".format(round(self.frame_count / self.skip_frames),
                                               int(object_id + 1), speed_label)
            cv2.putText(frame, info, (int(frame.shape[1] / 2), frame.shape[0] - ((idx * 50) + 50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 1, cv2.LINE_AA)

    def config(self, frame):
        """
        Функция для задания настроек видеофайла
        """
        width = frame.shape[1]
        height = frame.shape[0]

        # TODO: выбрать хороший фильтр
        blur = cv2.medianBlur(frame, 3)
        blob = cv2.dnn.blobFromImage(blur, 0.007843, (width, height), 127.5)
        self.net.setInput(blob)
        out = self.net.forward()

        return width, height, out

    @staticmethod
    def statistics_output(info, frame):
        """
        Функция позволяет выводить или сохранять
        заданную информацию в видеофайл
        """
        text = "{}".format("INFO VIDEO STREAM")
        cv2.putText(frame, text, (20, frame.shape[0] - 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2, cv2.LINE_AA)
        for (idx, (row, column)) in enumerate(info):
            info = "{}: {}".format(row, column)
            cv2.putText(frame, info, (20, frame.shape[0] - ((idx * 50) + 50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 1, cv2.LINE_AA)

    # def get_frame(self):
    #     return self.output_frame
    #
    # def translation_video(self, process_file):
    #     """
    #     Функция позволяет в реальном времени
    #     обработать видеозапись
    #     """
    #     fps = FPS().start()
    #     centroid_tracker = CentroidTracker(max_disappeared=50, max_distance=50)
    #     # fourcc = cv2.VideoWriter_fourcc(*'H264')
    #     # fourcc = cv2.VideoWriter_fourcc(*'avc1')
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Не лучший вариант, но на выше стоящие кодеки вызывается ошибка
    #     if not self.cap.isOpened():
    #         print("[INFO] failed to process video")
    #         raise
    #     filename = app.config['UPLOAD_FOLDER'] + '/output_video: %r.mp4' % datetime.now().strftime("%d-%m-%Y %H:%M")
    #     filename_csv = app.config['UPLOAD_FOLDER'] + '/csv: %s.csv' % str(process_file)
    #
    #     out_video = cv2.VideoWriter(filename, fourcc, self.skip_frames,
    #                                 (self.frame.shape[1], self.frame.shape[0]))
    #     with open(filename_csv, mode="w", encoding='utf-8') as file:
    #         file.write("timestamp;ID;speed\r\n")
    #     trackers = list()
    #
    #     while self.cap.isOpened():
    #         self.ret, self.frame = self.cap.read()
    #
    #         if self.ret:
    #             rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    #             rect = list()
    #             if self.frame_count % int(self.skip_frames) == 0:
    #                 trackers = list()
    #                 width, height, out = self.config(self.frame)
    #                 self.search_people(width, height, out, rgb, trackers)
    #             else:
    #                 self.status_tracking(rect, rgb, self.frame, trackers)
    #             objects = centroid_tracker.update(rect)
    #             self.object_and_speed(filename_csv, objects, self.frame)
    #
    #             info = [
    #                 ("Number of tracked objects", len(objects)),
    #                 ("Recognition percentage", self.percent),
    #                 ("Recognition object", self.class_name[15])
    #             ]
    #             self.statistics_output(info, self.frame)
    #             self.frame_count += 1
    #
    #             with LOCK:
    #                 self.output_frame = self.frame.copy()
    #             # _, buffer = cv2.imencode('.jpg', frame)
    #             # image = buffer.tobytes()
    #             # yield (b'--frame\r\n'
    #             #        b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    #
    #             # if cv2.waitKey(1) >= 0:  # Break with ESC
    #             #     break
    #             fps.update()
    #             out_video.write(self.frame)
    #         else:
    #             with LOCK:
    #                 self.output_frame = None
    #             break
    #     fps.stop()
    #     print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    #     print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    #     self.cap.release()
    #     out_video.release()
    #     return 0

    def save_frames(self, name, matrix, ratio_width):
        """
        Функция сохраняет видеозапись после обработки
        """
        fps = FPS().start()
        centroid_tracker = CentroidTracker(max_disappeared=100, max_distance=200)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Не лучший вариант, но на выше стоящие кодеки вызывается ошибка
        if not self.cap.isOpened():
            print("[INFO] failed to process video")
            raise
        ret, frame = self.cap.read()
        filename = f'{name}.mp4'
        folder = app.config['UPLOAD_FOLDER'] + '/' + filename
        filename_csv = app.config['UPLOAD_FOLDER'] + f'/CSV_{name}.csv'

        out_video = cv2.VideoWriter(folder, fourcc, self.skip_frames,
                                    (frame.shape[1], frame.shape[0]))
        with open(filename_csv, mode="w", encoding='utf-8') as file:
            file.write("timestamp;ID;speed\r\n")
        print("[INFO] video quality: {} {}".format(frame.shape[1], frame.shape[0]))
        trackers = list()
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rect = list()
                if self.frame_count % self.skip_frames < 1:
                    trackers = list()
                    width, height, out = self.config(frame)
                    self.search_people(width, height, out, rgb, trackers)
                else:
                    self.status_tracking(rect, rgb, frame, trackers)
                objects = centroid_tracker.update(rect)
                self.object_and_speed(filename_csv, objects, frame, matrix, ratio_width)

                info = [
                    ("Number of tracked objects", len(objects)),
                    ("Recognition percentage", self.percent),
                    ("Recognition object", self.class_name[15])
                ]
                self.statistics_output(info, frame)
                self.frame_count += 1

                fps.update()
                out_video.write(frame)
            else:
                break
        fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        self.cap.release()
        out_video.release()
        return str(filename)


# def generate(video):
#     while True:
#         with LOCK:
#             image = video.get_frame()
#             if image is None:
#                 break
#             _, buffer = cv2.imencode('.jpg', image)
#             encoded_image = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + encoded_image + b'\r\n')
