from locationmask import *


# проверяем, находится точка под или над прямой
def check_point_over_line(x1, y1, x2, y2, x3, y3):
    d = (x3 - x1) * (y2 - y1) - ((y3 - y1) * (x2 - x1))
    # 1 и 2 - координаты прямой, 3 - координаты точки которую проверяем
    # !!! x1 < x2
    # d == 0 - на прямой
    # d > 0 -  выше прямой
    # d < 0 - ниже прямой прямой
    return d


# определяем, лежит ли точка предмета внутри предмета, ограниченного контуром approx
def point_location(approx, x, y):
    under = 0
    over = 0

    # строим воображаемую прямую, параллельную оси у, через точку предмета, которую проверяем
    # смотрим, какие стороны многоугольника пересекает эта прямая (для выпуклого многоугольника таких сторон будет две)
    # для пересекаемых сторон смотрим, лежит ли точка предмета над или под прямой, содержащей эту сторону
    # если для одной прямой точка лежит под ней, а для другой над ней, то точка лежит внутри многоугольнкика
    for i in range(1, len(approx)):
        if approx[i][0][0] >= x and approx[i - 1][0][0] <= x:  # a[i-1] <= x <= a[i]
            d = check_point_over_line(approx[i - 1][0][0], approx[i - 1][0][1], approx[i][0][0], approx[i][0][1], x, y)
            if d >= 0:
                under = under + 1
            elif d < 0:
                over = over + 1

        if approx[i][0][0] <= x and approx[i - 1][0][0] >= x:  # a[i] <= x <= a[i-1]
            d = check_point_over_line(approx[i][0][0], approx[i][0][1], approx[i - 1][0][0], approx[i - 1][0][1], x, y)
            if d >= 0:
                under = under + 1
            elif d < 0:
                over = over + 1

    # проверяем линию между последней и нулевой точкой контура
    if approx[0][0][0] >= x and approx[len(approx) - 1][0][0] <= x:  # a[i-1] <= x <= a[i]
        d = check_point_over_line(approx[len(approx) - 1][0][0], approx[len(approx) - 1][0][1],
                                  approx[0][0][0], approx[0][0][1], x, y)
        if d >= 0:
            under = under + 1
        elif d < 0:
            over = over + 1

    if approx[0][0][0] <= x and approx[len(approx) - 1][0][0] >= x:  # a[i] <= x <= a[i-1]
        d = check_point_over_line(approx[0][0][0], approx[0][0][1], approx[len(approx) - 1][0][0],
                                  approx[len(approx) - 1][0][1], x, y)
        if d >= 0:
            under = under + 1
        elif d < 0:
            over = over + 1

    if under == 1 and over == 1:
        return 1  # точка внутри
    else:
        return 0  # точка снаружи


def check_place(num, img, approx_obj_list, approx_poly):
    # проверяем, находятся ли точки предмета внутри многоугольника и не внутри других предметов
    for point in approx_obj_list[num]:
        if point_location(approx_poly, point[0][0], point[0][1]):
            for j in range(0, num):
                if point_location(approx_obj_list[j], point[0][0], point[0][1]):
                    return 0
        else:
            return 0

    # провека точек намного быстрее проверки с помощью масок предметов, однако не дает точного результата,
    # так как не все точки контура проверяются.
    # Поэтому проверять положение с помощью масок будем только в случае успеха проверки точек

    # дополнительно проверяем наложением масок предметов друг на друга и проверкой на пересечение
    if check_by_mask(num, img, approx_obj_list, approx_poly) == 1:
        return 1
    return 0
