import cv2
import matplotlib.pyplot as plt
from detectcontours import *
from placer import *
from rotate import *
import globalvar
import time
from PIL import Image


def save_res(num):
    num_str = str(num)
    path = 'output/' + num_str + '_res.jpg'
    return path


def main_func(num, img):
    # получаем список точек контуров
    poly_area, approx_poly_list = find_polygon_contour(num, img)
    count_obj, sum_area, approx_obj_list = find_objects_contour(num, img)

    # обрабатываем ошибки
    if poly_area == 0:
        print('     FALSE: нет многоугольников')
        print('NO')
        return

    if count_obj == 0:
        print('     FALSE: нет предметов')
        print('NO')
        return

    if poly_area < sum_area:
        print('NO')
        return

    # распологаем контуры предметов в порядке уменьшения площади
    approx_obj_list = sorted(approx_obj_list, reverse=True, key=cv2.contourArea)

    # получаем крайние точки поля
    top, bottom, left, right = extreme_points(approx_poly_list[0])
    globalvar.p_top = top[1]
    globalvar.p_bottom = bottom[1]
    globalvar.p_left = left[0]
    globalvar.p_right = right[0]

    # составляем таблицу значений контуров при повороте предметов в начале коорднат, чтобы не рассчитывать их каждый раз заново
    globalvar.rotate_center_table.clear()
    for i in range(0, count_obj):
        globalvar.rotate_center_list.clear()
        make_rotate_center_list(approx_obj_list[i])
        globalvar.rotate_center_table.append(np.array(globalvar.rotate_center_list))

    # с помощью рекурсивной функции размещаем предметы
    res = recursive_placer(0, img, count_obj, approx_obj_list, approx_poly_list)

    #cv2.imwrite(save_res(num), img)


    if res == 1:
        plt.imshow(img)
        plt.show()
        print("YES")
        return
    else:
        print("NO")
        return


# Функция обрабатывает .input изображения с основного датасета
def check_image():
    for num in range(2, 22):
        time_start = time.time()
        path = 'input/polygon_' + str(num) + '.jpg'
        img = cv2.imread(path)
        main_func(num, img)
        print(num, 'Time:', "{0:.2f}".format(time.time() - time_start))



