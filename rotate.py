from extremepoints import *
# from locationmask import *
from location import *
from globalvar import *
import globalvar
import cv2
import numpy as np
import matplotlib.pyplot as plt
import collections


# переводим из декартовых в полярные координаты
def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


# переводим из полярных в декартовы координаты
def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


# делаем список контуров повернутого предмета при его нахождении в начале координат,
# для того чтобы не производить вычисления каждый раз при повороте предмета, 
# а брать данные из таблицы
def make_rotate_center_list(approx):
    global angle_base

    # находим центр предмета
    moment = cv2.moments(approx)
    px = int(moment['m10'] / moment['m00'])
    py = int(moment['m01'] / moment['m00'])

    # перемещаем центр предмета в точку начала координат
    approx_norm = approx - [px, py]

    # конвертируем координаты в полярные
    coordinates = approx_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cart2pol(xs, ys)

    for i in range(0, 360 // angle_base):
        angle = angle_base * i
        thetas_copy = thetas

        #  производим поворот
        thetas_copy = np.rad2deg(thetas_copy)
        thetas_copy = (thetas_copy + angle) % 360
        thetas_copy = np.deg2rad(thetas_copy)

        # конвертируем координаты в декартовы
        xs, ys = pol2cart(thetas_copy, rhos)
        approx_norm[:, 0, 0] = xs
        approx_norm[:, 0, 1] = ys

        # сохраняем контур в список
        globalvar.rotate_center_list.append(approx_norm.tolist())

    return 1


# производим поворот предмета относительно его центра
def rotate_center(num, img, approx_obj_list, approx_poly):
    # находим центр предмета
    moment = cv2.moments(approx_obj_list[num])
    px = int(moment['m10'] / moment['m00'])
    py = int(moment['m01'] / moment['m00'])

    # если центр находится внутри другого предмета
    for j in range(0, num):
        if point_location(approx_obj_list[j], px, py):
            return 0, approx_obj_list[num]

    for i in range(0, 360 // angle_base):

        # берем конутур таблицы и из начала координат перемещаем центр предмета в изначальное место
        approx_obj_list[num] = globalvar.rotate_center_table[num][i] + [px, py]
        approx_obj_list[num] = approx_obj_list[num].astype(np.int32)

        # проверяем, удалось ли разместить предмет
        if check_place(num, img, approx_obj_list, approx_poly):
            return 1, approx_obj_list[num]

    return 0, approx_obj_list[num]
