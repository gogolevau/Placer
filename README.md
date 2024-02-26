## Постановка задачи
На вход поступает фотография в формате .jpg, на которой на однотонной горизонтальной поверхности изображены один или несколько предметов, выбранных из заранее заготовленных и отснятых (см. пункт "Список предметов"), а также нарисованный на белом листе бумаги А4 многоугольник. Необходимо определить, можно ли данные предметы поместить в данный многоугольник одновременно так, чтобы никакая часть предметов не выходила за границы многоугольника. В качестве выходных данных в консоль выводится результат в виде одного из слов:

Yes - предметы можно разместить в многоугольнике

No - предметы нельзя разместить в прямоугольнике или входные данные неверные

## Список предметов
1. Замазка
2. Расческа
3. Скотч
4. Ножницы
5. Флешка
6. Набор закладок
7. Транспортир
8. Клубок ниток
9. Губная помада
10. Игрушка

## Фотографии предметов
Примеры предметов находятся в документе "Data.md"

## Набор входных данных для тестирования
Набор входных данных вместе с ожидаемым результатом работы находится в документе "Data.md"

## Требования
### К фотографиям
1. Формат фотографий - .jpg 
2. Условия съемки: 
Фотографии сделаны отчетливо, без бликов или интенсивных теней, на одну и ту же камеру.
Цвет фона - однотонный, темнее листа бумаги.
Расположение камеры - сверху перпендикулярно предмету без существенных отклонений (не более 10 градусов).
Ориентация фотографий может быть произвольной.

### К предметам:
Предметы по размеру не могут быть больше листа бумаги А4.
Предметы не сливаются с листом бумаги и не накладываются друг на друга.
Границы предмета чёткие.
Предмет на фотографии может быть только в единственном экземпляре.

### К поверхности:
Поверхность горизонтальная, темнее листа бумаги, однотонная.
На поверхности полностью помещается лист бумаги и предметы.
Поверхность выбирается однажды и не меняется для каждой фотографии.

### К исходным данным
В качестве исходных данных используются фотографии, на которых в центре белого листа А4 расположен по очереди каждый предмет. Всего предметов 10. Лист помещается на фотографию полностью. Фотографии сделаны согласно всем требованиям к фотографии. 

### К входным данным
В качестве входных данных подаётся фотография, сделанная по всем требованиям. 
На фотографии находится белый лист бумаги А4, на котором отчетливо маркером нарисован многоугольник, а так же один или несколько предметов.
Предметы выбранны из заранее заготовленных и находятся в непосредственной близости от листа бумаги. Лист полностью помещается на фотографию.
Лист бумаги и предметы не перекрывают друг друга.

