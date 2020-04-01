import math
import random
import ctypes
import pygame

sudoku_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# A function that generate valid Sudoku board
def generate_board(board):
    for diagonal in range(9):
        board[diagonal][diagonal] = random.randrange(1, 10)
        if diagonal % 3 == 1:
            if board[diagonal - 1][diagonal - 1] == board[diagonal][diagonal]:
                board[diagonal][diagonal] = 0
        elif diagonal % 3 == 2:
            if board[diagonal - 1][diagonal - 1] == board[diagonal][diagonal] or board[diagonal - 2][diagonal - 2] == \
                    board[diagonal][diagonal]:
                board[diagonal][diagonal] = 0
    solve_board(board)
    numbers_removed = 50
    while numbers_removed > 0:
        random_row = random.randrange(0, 9)
        random_column = random.randrange(0, 9)
        if board[random_row][random_column] != 0:
            board[random_row][random_column] = 0
            numbers_removed -= 1


# A function that prints board in the right format
def print_board(board):
    print("")
    for i in range(len(board[0])):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")
    print("")


# Solve Sudoku board
def solve_board(board):
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    else:
        row, column = empty_cell
    for possible_number in range(1, 10):
        if valid_position(board, possible_number, (row, column)):
            board[row][column] = possible_number
            if solve_board(board):
                return True
            board[row][column] = 0
    return False


# A function find the empty cells in the board
def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j  # row, column
    return None


# A function check if the entered number is valid in this position or not
def valid_position(board, number, empty_position):
    # Check row
    for row in range(len(board[0])):
        if board[empty_position[0]][row] == int(number) and empty_position[1] != row:
            return False
    # Check column
    for column in range(len(board)):
        if board[column][empty_position[1]] == int(number) and empty_position[0] != column:
            return False
    # Check small block
    size_of_block = int(math.sqrt(len(board[0])))
    row_index = int(empty_position[1] // size_of_block)
    column_index = int(empty_position[0] // size_of_block)
    for row in range(column_index * size_of_block, column_index * size_of_block + size_of_block):
        for column in range(row_index * size_of_block, row_index * size_of_block + size_of_block):
            if board[row][column] == int(number) and empty_position != (row, column):
                return False
    return True


# To draw lines between each three rows
def draw_x_border(x_axis, y_axis, color):
    for j in range(4):
        pygame.draw.line(window, color, (x_axis + j * (5 + width) * 3, y_axis),
                         (x_axis + j * (5 + width) * 3, y_axis + 495), 5)


# To draw lines between each three columns
def draw_y_border(x_axis, y_axis, color):
    for j in range(4):
        pygame.draw.line(window, color, (x_axis, y_axis + j * (5 + width) * 3),
                         (x_axis + 495, y_axis + j * (5 + width) * 3), 5)


# Set initial grid
def set_grid(x_axis, y_axis, width, height, color):
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(window, color, (x_axis, y_axis, width, height))
            rectangle_list.append(pygame.Rect(x_axis, y_axis, width, height))
            if not(sudoku_board[i][j] == 0):
                generated_list.append((i, j))
                label = myfont.render(str(sudoku_board[i][j]), 0, (0, 0, 0))
                window.blit(label, (x_axis + 20, y_axis + 20))
            x_axis += width + 5
        y_axis += height + 5
        x_axis = 25


# Check a column
def check_column(board, cell, x, y):
    for i in range(9):
        if board[i][y] == cell and x != i:
            return False
    return True


# Check a row
def check_row(board, cell, x, y):
    for i in range(9):
        if board[x][i] == cell and y != i:
            return False
    return True


# Check each block in the grid
def check_block(board):
    for k in range(0, 9, 3):
        sum = 0
        for i in range(k, k + 3):
            for j in range(k, k + 3):
                sum += board[i][j]
        if sum != 45:
            return False
    return True


# Check the whole grid
def check_board(board):
    for i in range(9):
        for j in range(9):
            if not(check_row(board, board[i][j], i, j)):
                return False
    for i in range(9):
        for j in range(9):
            if not(check_column(board, board[i][j], i, j)):
                return False
    if not(check_block(board)):
        return False
    return True


generated_list = []
rectangle_list = []
pygame.init()
window = pygame.display.set_mode((800, 520))
pygame.display.set_caption("Sudoku Game")
generate_board(sudoku_board)

start = False
run = True
while run:
    pygame.time.delay(80)
    myfont = pygame.font.SysFont("freesansbold.ttf", 40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    window.fill((40, 40, 40))
    x_axis = 25
    y_axis = 20
    width = 50
    height = 50
    set_grid(x_axis, y_axis, width, height, (255, 255, 255))
    x_axis = 20
    y_axis = 15
    draw_x_border(x_axis, y_axis, (51, 1, 212))
    draw_y_border(x_axis, y_axis, (51, 1, 212))

    first_time = False
    if not first_time:
        for i in rectangle_list:
            if i.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.lines(window, (255, 5, 0), True,
                ((i[0], i[1]), (i[0] + height, i[1]), (i[0] + height, i[1] + width), (i[0], i[1] + width)), 4)

    if pygame.mouse.get_pressed() == (True, False, False):
        for i in rectangle_list:
            if i.collidepoint(pygame.mouse.get_pos()):
                x, y = i[0], i[1]
                if not((i[1] // 55, i[0] // 55) in generated_list):
                    pygame.draw.lines(window, (25, 5, 70), True,
                    ((i[0], i[1]), (i[0] + height, i[1]), (i[0] + height, i[1] + width), (i[0], i[1] + width)), 4)
                    num = 0
                    while not(event.type == pygame.KEYDOWN):
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                    num = 1
                                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                    num = 2
                                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                                    num = 3
                                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                                    num = 4
                                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                    num = 5
                                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                                    num = 6
                                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                                    num = 7
                                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                                    num = 8
                                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                                    num = 9
                                else:
                                    continue
                                label = myfont.render(str(num), 0, (150, 70, 0))
                                window.blit(label, (i[0] + 20, i[1] + 20))
                                sudoku_board[i[1] // 55][i[0] // 55] = num
                                start = True
                else:
                    pygame.draw.lines(window, (255, 105, 0), True,
                    ((i[0], i[1]), (i[0] + height, i[1]), (i[0] + height, i[1] + width), (i[0], i[1] + width)), 4)
                first_time = True
    pygame.draw.rect(window, (200, 80, 160), (600, 200, 165, 50))
    label = myfont.render("New Game", 0, (0, 0, 0))
    window.blit(label, (600 + 15, 200 + 10))
    tmpx, tmpy = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (
            True, False, False) and tmpx > 600 and tmpx < 600 + 165 and tmpy > 200 and tmpy < 200 + 50:
        sudoku_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        generate_board(sudoku_board)
        generated_list = []
        start = False
    if not start:
        pygame.draw.rect(window, (200, 120, 160), (600, 250, 165, 50))
        label = myfont.render("Solution", 0, (0, 0, 0))
        window.blit(label, (600 + 15, 250 + 10))
        tmpx, tmpy = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (
                True, False, False) and tmpx > 600 and tmpx < 600 + 165 and tmpy > 250 and tmpy < 250 + 50:
            solve_board(sudoku_board)
            set_grid(x_axis, y_axis, width, height, (255, 255, 255))
            pygame.display.update()
            ctypes.windll.user32.MessageBoxW(0, "Try harder next time", "Solution", 0)
            break

    if not find_empty(sudoku_board):
        if check_board(sudoku_board):
            ctypes.windll.user32.MessageBoxW(0, "Congratulations!", "WIN", 1)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Game Over", "LOSE", 1)
        break
    pygame.display.update()
pygame.quit()
