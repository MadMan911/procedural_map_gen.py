import pygame as p
from pygame.locals import *
import random


def near_water(cells, i, j):
    # границ нет, то есть идешь вправо -> появляешься слева
    for y in range(-1, 2):
        for x in range(-1, 2):
            if cells[(i + y) % len(cells)][(j + x) % len(cells[0])] <= 0.2:
                return 1
    return 0

def near_full_grass(cells, i, j):
    # границ нет, то есть идешь вправо -> появляешься слева
    count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if cells[(i + y) % len(cells)][(j + x) % len(cells[0])] <= 0.2:
                count += 1
    if count == 4:
        return 1
    else:
        return 0

sr = 4
stepen = 2
w, h = 600,600 # w и h должны делиться на 12
WHITE = (255,255,255)
BLACK = (0,0,0)
GRASS = (63,155,11)
SAND = (252,222,124)
SNOW = (252,247,247)
WATER = (47,155,254)
DEEPWATER = (0,31,143)
a = 10 # tiles должны быть маленького размера для большей дитализации

# шум Перлина
# создадим 4 сетки разных размеров
# первая сетка, самые маленькие клеточки
cells0 = []
for i in range(h // a):
    cells0.append([])
    for _ in range(w // a):
        cells0[i].append(random.randrange(0,100)/100)

# print(cells)
# вторая сетка, почти самые маленькие клеточки
cells1 = []
randl = []
# for i in range(w//a // 3):
#     for j in range(3):
#         randl.append(random.randrange(0,100)/100)
c = 0
for i in range((h//a)):
    cells1.append([])
    if (c % 3) == 0:
        randl = []
        for _ in range((w // a) // 3):
            r = random.randrange(0, 100) / 100
            for _ in range(3):
                randl.append(r)
    c += 1
    # print('randl',randl)
    for j in range(len(randl)):
        cells1[i].append(randl[j])

# for i in range(len(cells1)):
#     print(cells1[i])
# print(cells1)

# создаем третью сетку, с почти самыми большими клетками
cells2 = []
randl = []
c = 0
for i in range(h // a):
    cells2.append([])
    if (c % (h//a // 3)) == 0:
        randl = []
        for _ in range((w//a)//(h//a // 3)):
            r = random.randrange(0, 100) / 100
            for _ in range((h//a // 3)):
                randl.append(r)
    c += 1
    for j in range(len(randl)):
        cells2[i].append(randl[j])

# for i in range(len(cells2)):
#     print(cells2[i])

# создаем четвертую сетку, самые большие клеточки
cells3 = []
randl = []
c = 0
for i in range(h//a):
    cells3.append([])
    if ( c % (h//a//2)) == 0:
        randl = []
        for _ in range((w//a)//(h//a//2)):
            r = random.randrange(0, 100) / 100
            for _ in range((h // a // 2)):
                randl.append(r)
    c += 1
    for j in range(len(randl)):
        cells3[i].append(randl[j])

# for i in range(len(cells3)):
#     print(cells3[i])

cells = []
for i in range(len(cells0)):
    cells.append([])
    for j in range(len(cells0[i])):
        cells[i].append(((cells0[i][j]+cells1[i][j]+cells2[i][j]+cells3[i][j])/sr)**stepen)

for i in range(len(cells)):
    print(cells[i])

# создаем поле
root = p.display.set_mode((w, h))
# основная логика
while True:
    # заполняем поле белым
    root.fill(SAND)
    # проверяем на закрытие проги, чтобы шиндоус не думал, что она не отвечает
    for i in p.event.get():
        if i.type == QUIT:
            quit()

    for i in range(len(cells)):
        for j in range(len(cells[i])):
            h = cells[i][j]
            # if h <= 0.05 and not (0.25 < cells[i%len(cells)][(j-1)%len(cells[i])] and 0.25 < cells[i%len(cells)][(j+1)%len(cells[i])] and 0.25 <cells[(i-1)%len(cells)][j%len(cells[i])] and 0.25 <cells[(i+1)%len(cells)][j%len(cells[i])]):
            #     p.draw.rect(root, DEEPWATER,[j * a, i * a, a, a])
            if h <= 0.2: #0.05 <
                p.draw.rect(root, WATER, [j * a, i * a, a, a])
            elif 0.2 < h <= 0.25 and not (near_full_grass(cells,i,j)) and near_water(cells,i,j):
                p.draw.rect(root, SAND, [j * a, i * a, a, a])
            elif 0.25 < h <= 0.7 and not near_water(cells,i,j):
                p.draw.rect(root, GRASS, [j * a, i * a, a, a])
            elif 0.25 < h <= 0.7:
                p.draw.rect(root, SAND, [j * a, i * a, a, a])
            elif 0.9 < h :
                p.draw.rect(root, WHITE, [j * a, i * a, a, a])

    p.display.update()
