from game_functions import initialize_game, random_move,\
    move_down, move_left,\
    move_right, move_up,\
    check_for_win, add_new_tile_by_random, add_new_tile_by_user
import numpy as np

NUMBER_OF_MOVES = 4


def ai_move(board, searches_per_move, search_length):
    possible_first_moves = [move_left, move_up, move_down, move_right]
    first_move_scores = np.zeros(NUMBER_OF_MOVES)
    for first_move_index in range(NUMBER_OF_MOVES):
        first_move_function = possible_first_moves[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(
            board)
        if first_move_made:
            board_with_first_move = add_new_tile_by_random(
                board_with_first_move)
            first_move_scores[first_move_index] += first_move_score
        else:
            continue
        for _ in range(searches_per_move):
            move_number = 1
            search_board = np.copy(board_with_first_move)
            game_valid = True
            while game_valid and move_number < search_length:
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    search_board = add_new_tile_by_random(search_board)
                    first_move_scores[first_move_index] += score
                    move_number += 1
    best_move_index = np.argmax(first_move_scores)
    best_move = possible_first_moves[best_move_index]
    search_board, game_valid, score = best_move(board)
    return search_board, game_valid
