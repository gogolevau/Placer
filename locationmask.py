import cv2
import numpy as np
import matplotlib.pyplot as plt


# Area(approx) > Area(approx_obj)
# получаем положение предметов относительно друг друга
def location_by_mask(img,approx, approx_obj):
    mask = np.zeros(img.shape, np.uint8)
    mask_approx = cv2.drawContours(mask.copy(), [approx], -1, 255, -1)
    mask_approx_obj = cv2.drawContours(mask.copy(), [approx_obj], -1, 255, -1)

    # находим пересечение масок предметов
    cross = cv2.bitwise_and(mask_approx, mask_approx_obj)

    # если пересечение - нулевой массив,
    # то предметы не пересекаются
    if (cross == mask).all():
        return 0

    # если пересечение совпадает с маской меньшего предмета,
    # то меньший предмет полностью находится внутри большего
    elif (cross == mask_approx_obj).all():
        return 1
    else:
        return -1


# проверяем положение предмета относительно других объектов и многоугольника
def check_by_mask(num, img, approx_obj_list, approx_poly):
    for i in range(0, num):
        if location_by_mask(img, approx_obj_list[i], approx_obj_list[num]) != 0:
            return 0

    if location_by_mask(img, approx_poly, approx_obj_list[num]) == 1:
        return 1

    return 0
