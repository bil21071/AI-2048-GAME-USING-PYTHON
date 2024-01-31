import numpy as np


POSSIBLE_MOVES_COUNT = 4
CELL_COUNT = 4
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])


def initialize_game():
    board = np.zeros((NUMBER_OF_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(
        NUMBER_OF_SQUARES, 2, replace=False)
    board[initial_twos] = 2
    board = board.reshape((CELL_COUNT, CELL_COUNT))
    return board


def push_board_right(board):
    new = np.zeros((CELL_COUNT, CELL_COUNT), dtype="int")
    done = False
    for row in range(CELL_COUNT):
        count = CELL_COUNT - 1
        for col in range(CELL_COUNT - 1, -1, -1):
            if board[row][col] != 0:
                new[row][count] = board[row][col]
                if col != count:
                    done = True
                count -= 1
    return (new, done)


def merge_elements(board):
    score = 0
    done = False
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT - 1, 0, -1):
            if board[row][col] == board[row][col-1] and board[row][col] != 0:
                board[row][col] *= 2
                score += board[row][col]
                board[row][col-1] = 0
                done = True
    return (board, done, score)


def move_up(board):
    rotated_board = np.rot90(board, -1)
    pushed_board, has_pushed = push_board_right(rotated_board)
    merged_board, has_merged, score = merge_elements(pushed_board)
    second_pushed_board, _ = push_board_right(merged_board)
    rotated_back_board = np.rot90(second_pushed_board)
    move_made = has_pushed or has_merged
    return rotated_back_board, move_made, score


def move_down(board):
    board = np.rot90(board)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -1)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_left(board):
    board = np.rot90(board, 2)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -2)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_right(board):
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    move_made = has_pushed or has_merged
    return board, move_made, score


def fixed_move(board):
    move_order = [move_left, move_up, move_down, move_right]
    for func in move_order:
        new_board, move_made, _ = func(board)
        if move_made:
            return new_board, True
    return board, False


def random_move(board):
    move_made = False
    move_order = [move_right, move_up, move_down, move_left]
    while not move_made and len(move_order) > 0:
        move_index = np.random.randint(0, len(move_order))
        move = move_order[move_index]
        board, move_made, score = move(board)
        if move_made:
            return board, True, score
        move_order.pop(move_index)
    return board, False, score


def add_new_tile_by_user(board):
    # --------by user--------
    index_list = []
    while True:
        print('--------------------------------')
        tile_row_values, tile_col_values = np.nonzero(np.logical_not(board))
        combo = np.column_stack((tile_row_values, tile_col_values))
        print("Avaliable positions to place new tiles are as:")

        i = 0
        for index in combo:
            i += 1
            index_list.append(i)
            # print(index_list)
            print(f'Index: {i} [{index[0]+1} {index[1]+1}]')
        
        try:
            selected_index = int(input('Enter an Index: '))
        except:
            None
        # trc = np.array([tile_row_options, tile_col_options])
        print('--------------------------------')
        try:
            if selected_index in index_list:
                tile_row_options = combo[selected_index-1][0]
                tile_col_options = combo[selected_index-1][1]
                while True:
                    tile_value = int(
                        input('Enter either 2 or 4 for the tile value: '))
                    if tile_value in [2, 4]:
                        board[tile_row_options, tile_col_options] = tile_value
                        print('**** TILE GENERATED ****')
                        return board
                    else:
                        print('Value entered is not correct')
            else:
                print(
                    "Enter from the available indices!!")
        except:
            tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
            tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
            tile_loc = np.random.randint(0, len(tile_row_options))
            board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
            return board

def add_new_tile_by_random(board):
    # --------by random--------
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(
        0, len(NEW_TILE_DISTRIBUTION))]
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    tile_loc = np.random.randint(0, len(tile_row_options))
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return board


def check_for_win(board):
    tile_row_values, tile_col_values = np.nonzero(np.logical_not(board))
    combo = np.column_stack((tile_row_values, tile_col_values))
    if 2048 in board:
        print("2048 Achieved!!!")
        return 2048 in board
    if len(combo.tolist()) == 0:
        print('Game lost\nNo more moves :(')
