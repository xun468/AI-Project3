import numpy as np
import cv2


def draw_agent(position, moves, goal, pix, img):
    x = position[0] + int(pix/2)
    y = position[1] + int(pix/2)
    x_goal = goal[1]*pix
    y_goal = goal[0]*pix
    for i in range(len(moves)):
        if y == y_goal and x == x_goal:
            break
        if moves[i] == 1:
            cv2.line(img, (x, y), (x, y - pix), (255, 0, 0), 5)
            y = y - pix
        elif moves[i] == 2:
            cv2.line(img, (x, y), (x + pix, y), (255, 0, 0), 5)
            x = x + pix
        elif moves[i] == 3:
            cv2.line(img, (x, y), (x, y + pix), (244, 0, 0), 5)
            y += pix
        elif moves[i] == 4:
            cv2.line(img, (x, y), (x - pix, y), (255, 0, 0), 5)
            x -= pix


def draw_maze(maze_arr, ag1):
    pix = 50
    img = np.zeros((len(maze_arr) * pix, len(maze_arr[0]) * pix, 3), np.uint8)

    for i in range(len(maze_arr)):
        start, init = -1, -1
        flag_h = False
        flag_v = False
        for j in range(len(maze_arr[0])):
            if not maze_arr[i][j] and not flag_h:
                start = j
                flag_h = True
            elif maze_arr[i][j]:
                if flag_h and j > 1:
                    for k in range(pix):
                        cv2.line(img, (start * pix, i * pix + k), (j * pix, i * pix + k), (255,255,255), 5)
                flag_h = False
            if not maze_arr[j][i] and not flag_v:
                init = j
                flag_v = True
            elif maze_arr[j][i]:
                if flag_v and j - init > 1:
                    for k in range(pix):
                        cv2.line(img, (i * pix + k, init * pix), (i * pix + k, j * pix), (255,255,255), 5)
                flag_v = False
        if flag_h:
            for k in range(pix):
                cv2.line(img, (start * pix, i * pix + k), (j * pix, i * pix + k), (255,255,255), 5)
        if flag_v:
            for k in range(pix):
                cv2.line(img, (i * pix + k, init * pix), (i * pix + k, j * pix), (255,255,255), 5)
    draw_agent(ag1[0], ag1[1], ag1[2], pix, img)
    cv2.imshow('image', img)
    cv2.waitKey(0)

#
# maze = [[True, True, True, True, True, True, True, True, True],
#         [True, False, False, False, True, False, False, False, True],
#         [True, False, True, False, True, True, True, False, True],
#         [True, False, True, False, False, False, True, False, True],
#         [True, False, True, False, True, True, True, False, True],
#         [True, False, False, False, False, False, True, False, True],
#         [True, False, True, True, True, True, True, False, True],
#         [True, False, False, False, False, False, False, False, True],
#         [True, True, True, True, True, True, True, True, True]]
# ag1 = ([0, 0], [3, 1, 2, 2, 2, 2, 2, 4, 1, 3, 3, 2, 2, 3, 3, 4, 4, 4, 2, 3],[4,4])
# draw_maze(maze, ag1)
