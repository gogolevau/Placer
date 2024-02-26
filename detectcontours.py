import cv2
import numpy as np
import matplotlib.pyplot as plt

# параметры цветового фильтра
hsv_min = np.array([160, 50, 120])
hsv_max = np.array([175, 255, 255])


# получаем путь, по которому надо сохранить файл с контуром для многоугольника
def take_path_polygon(num):
    numstr = str(num)
    path = 'contours/polygon_' + numstr + '_contour.jpg'
    return path


# находим контур многоугольника на фотографиях с основного датасета
def find_polygon_contour(num, img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    canny_img = cv2.Canny(binary, 50, 100)
    contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # определяем номер контура с максимальной площадью (то есть белого листа)
    max_area = 0
    max_area_num = 0
    for i in range(hierarchy.shape[1]):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            max_area = area
            max_area_num = i

    approx_list = []
    # получаем контур многоугольника
    # по всем найденным внури белого листа контурам
    for i in range(max_area_num, hierarchy.shape[1]):
        # подсчитываем площадь очередного контура
        area = cv2.contourArea(contours[i])
        # ищем первый контур внутри белого листа
        # 4 - максимальная толщина линии, ограничивающей белый лист
        # 20 - контуры случайных "мусорных" точек
        if area < max_area - 4 and area > 20:
            # аппроксимируем контурр (уменьшаем число вершин) для упрощения размещения предмета
            approx = cv2.approxPolyDP(contours[i], 0.012 * cv2.arcLength(contours[i], True), True)
            cv2.drawContours(img, [approx], 0, (255, 255, 0), 5)
            approx_list.append(approx)

            #plt.imshow(img)
            #plt.show()
            #cv2.imwrite(take_path_polygon(num), img)
            return area, approx_list

    return 0, 0


# находим контуры предметов
def find_objects_contour(num, img):
    # меняем цветовую модель с BGR на HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    # ищем контуры и складируем их в переменную contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_area_num = 0
    paper_area = 0
    paper_area_num = 0
    # находим внешний контур изображения и его площадь
    for k in range(hierarchy.shape[1]):
        area = cv2.contourArea(contours[k])
        if area > max_area:
            max_area = area
            max_area_num = k

    # находим контур листа бумаги и его площадь, чтобы искать предметы вне его
    if max_area_num == 0:
        for k in range(hierarchy.shape[1]):
            area = cv2.contourArea(contours[k])
            if area > paper_area and area < max_area - 100:
                paper_area = area
                paper_area_num = k
    else:
        paper_area = max_area
        paper_area_num = max_area_num

    approx_list = []
    count = 0
    sum_area = 0
    # ищем контуры предметов
    for i in range(0, paper_area_num):
        # проверяем что не взяли внутренний контур предмета (ножницы, скотч)
        if hierarchy[0][i][3] == max_area_num or hierarchy[0][i][3] == -1:
            area = cv2.contourArea(contours[i])
            # не рассматриваем слишком мелкие точки и контуры, очень близкие к контуру листа бумаги или контуру изображения
            if area > 600 and area < max_area - 1000 and area < paper_area - 100:
                approx = cv2.approxPolyDP(contours[i], 0.009 * cv2.arcLength(contours[i], True), True)
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
                approx_list.append(approx)
                count = count + 1
                sum_area = sum_area + area

    plt.imshow(img)
    plt.show()
    #cv2.imwrite(take_path_polygon(num), img)

    return count, sum_area, approx_list
