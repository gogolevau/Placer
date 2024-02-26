# находим крайние точки предметов
def extreme_points(approx):
    top = approx[0][0]
    bottom = approx[0][0]
    left = approx[0][0]
    right = approx[0][0]

    for i in range(1, len(approx)):
        if top[1] > approx[i][0][1]:
            top = approx[i][0]
        if bottom[1] < approx[i][0][1]:
            bottom = approx[i][0]
        if left[0] > approx[i][0][0]:
            left = approx[i][0]
        if right[0] < approx[i][0][0]:
            right = approx[i][0]

    return top, bottom, left, right
