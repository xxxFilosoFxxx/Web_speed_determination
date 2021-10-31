# pylint: disable=no-else-return, fixme
"""
Основные действия для нахождения скорости после
детектирования и идентификации объектов
"""
from collections import OrderedDict
import math
import copy
import numpy as np
import os

# Дельта скорости объекта
DELTA = os.environ.get('DELTA', 0)


class SearchSpeed:
    """ Основной класс для нахождения скорости объекта """
    def __init__(self):
        self.track = dict()
        self.speed = OrderedDict()
        self.centroids = OrderedDict()
        self.last_centroids = OrderedDict()

    def save_centroids(self, objects):
        """
            Функция для запоминания координат
            центроидов настоящего и прошлого кадра
        Args:
            objects: упорядоченный словарь

        Returns:
            копии (копию) упорядоченного словаря
        """
        if not self.centroids:
            self.centroids = copy.deepcopy(objects)
            return self.centroids

        if not self.last_centroids and self.centroids:
            self.last_centroids = copy.deepcopy(objects)
            return self.last_centroids

        self.centroids = copy.deepcopy(self.last_centroids)
        self.last_centroids = copy.deepcopy(objects)
        return self.last_centroids

    def search_speed(self, i, matrix, ratio_width):
        """
            Основаня функция для поиска скорости объекта
        Args:
            i: идентификатор объекта
            matrix: обратная матрица фактического расстояния плоскости
            ratio_width: отношение разрешения формата видео
        Returns:
            скорость объекта
        """
        # по расстоянию Евклида на основе локационной привязки определить скорость объекта
        if i in self.centroids and i in self.last_centroids:
            inverse_matrix = np.matrix(matrix)
            centroids_matrix = np.matrix([[self.centroids[i][0]], [self.centroids[i][1]], [1]])
            last_centroids_matrix = np.matrix([[self.last_centroids[i][0]], [self.last_centroids[i][1]], [1]])
            old_place_matrix = inverse_matrix * centroids_matrix
            new_place_matrix = inverse_matrix * last_centroids_matrix
            old_place = [old_place_matrix.A1[0] / old_place_matrix.A1[2],
                         old_place_matrix.A1[1] / old_place_matrix.A1[2]]
            new_place = [new_place_matrix.A1[0] / new_place_matrix.A1[2],
                         new_place_matrix.A1[1] / new_place_matrix.A1[2]]
            d_speed = math.sqrt(math.pow(new_place[0] - old_place[0], 2) +
                                math.pow(new_place[1] - old_place[1], 2))
            speed = (d_speed * 3.6) / ratio_width
            return int(round(speed))  # Средняя скорость идущего человека 5-6 км/ч, бег 10-15 км/ч
        else:
            return 0

    def search_delta_speed(self, i, matrix, ratio_width):
        """
            Функция для записи текущей скорости и высчитывание дельты
        Args:
            i: идентификатор объекта
            matrix: обратная матрица фактического расстояния плоскости
            ratio_width: отношение разрешения формата видео
        """
        speed = self.search_speed(i, matrix, ratio_width)
        if i in self.speed:
            delta = speed - self.speed[i]
            if abs(delta) > DELTA:  # Дельта скорости объекта
                self.speed[i] = speed
        else:
            self.speed[i] = speed

    @staticmethod
    def save_speed(filename, timestamp, object_id, speed):
        """
            Функция сохраняет скорость объекта в файл
        Args:
            filename: Имя файла
            timestamp: Метка времени
            object_id: id объекта
            speed: скорость объекта
        """
        with open(filename, mode="a", encoding='utf-8') as file:
            file.write("{};{};{}\r\n".format(timestamp, object_id + 1, speed))
