import numpy as np
from itertools import permutations
from OS1 import OrderedSet
from time import time
import csv

t = time()

'''
012   
345
678
'''
transformations = (
  [6, 3, 0, 7, 4, 1, 8, 5, 2], # rotation 90 clockwise
  [8, 7, 6, 5, 4, 3, 2, 1, 0], # rotate 180
  [2, 5, 8, 1, 4, 7, 0, 3, 6], # rotation 90 anti clockwise
  [2, 1, 0, 5, 4, 3, 8, 7, 6], # reflect in vertical
  [6, 7, 8, 3, 4, 5, 0, 1, 2], # reflect in horizontal
  [0, 3, 6, 1, 4, 7, 2, 5, 8], # reflect in diagonal
  [8, 5, 2, 7, 4, 1, 6, 3, 0]) # reflect in other diagonal

wins = (
  [0, 1, 2], # top row win
  [3, 4, 5], # middle row win
  [6, 7, 8], # bottom row win
  [0, 3, 6], # first column win
  [1, 4, 7], # middle column win
  [2, 5, 8], # final column win
  [0, 4, 8], # diagonal win
  [2, 4, 6]) # diaognal win


def remove_transformations(boards):
  ''' takes in an ordered set of boards
  returns a list of boards with transforamtions removed'''
  new_boards = list()
  for board in boards:
    transformed_boards = [tuple(board[i] for i in t) for t in transformations]
    if not any(t in new_boards for t in transformed_boards):
      new_boards.append(board)
  return new_boards


def remove_wins(boards):
  ''' takes in an ordered set of boards
  returns a list of boards with wins removed'''
  new_boards = boards[:]
  for board in boards:
    for piece in 'xo':
      if any(all(board[i] is piece for i in win) for win in wins):
        try:
          new_boards.remove(board)
        except:
          pass
  return new_boards


board0 = ('','','','','','','','','')
board1 = OrderedSet(permutations(['o','x','','','','','','',''],9))
board2 = OrderedSet(permutations(['o','o','x','x','','','','',''],9))
board3 = OrderedSet(permutations(['o','o','o','x','x','x','','',''],9))
all_boards = []
board1 = remove_transformations(board1)
board2 = remove_transformations(board2)
board3 = remove_wins(remove_transformations(board3))
all_boards += [board0] + board1 + board2 + board3


def find_board_number(board):
  transformed_boards = [tuple(board[i] for i in t) for t in transformations]
  for t in transformed_boards:
    if t in all_boards:
      return all_boards.index(t)


def get_free_spaces(board):
  spaces = []
  move = len(''.join(board))/2
  for i,space in enumerate(board):
    if not space:
      spaces.append(i)
  return spaces


def get_total_symmetries(board):
  count = 0
  transformed_boards = [tuple(board[i] for i in t) for t in transformations]
  for t in transformed_boards:
    if t == board:
      count += 1
  return count


def get_trans_lists(board):
  ''' with a baord, returns all its symmetries that are equivalent boards'''
  trans_list = []
  transformed_boards = [tuple(board[i] for i in t) for t in transformations]
  for i,t in enumerate(transformed_boards):
    if t == board:
      trans_list.append(transformations[i])
  return trans_list


def get_initial_state(board):
  ''' expects a board as input
  returns the board but with integers representing the number of beads to go
  in each space
  '''
  spaces = get_free_spaces(board)
  beads = 2**((len(spaces)-3)//2) # 8 beads per space, then 4 beads per space, then 2 beads per space...
  trans_list = get_trans_lists(board)
  board = list(board)
  move_dict = {}
  if 4 in spaces:
    board[4] = beads
    spaces.remove(4)
  if trans_list:
    for space in spaces:
      #adds a board to the dict after a potential move
      temp_board = board[:]
      temp_board[space] = beads
      move_dict[space] = tuple(temp_board)
    removed_spaces = set()
    for current_space in spaces:
      if current_space not in removed_spaces:
        transformed_boards = [tuple(move_dict[current_space][i] for i in t) for t in trans_list]
        for transformed_board in transformed_boards:
          for move, move_board in move_dict.items():
            if move_board == transformed_board and move is not current_space:
              removed_spaces.add(move)
    spaces = [space for space in spaces if space not in removed_spaces]
  for i,space in enumerate(board):
    if i in spaces:
      board[i] = beads
  return tuple(board)
 
 
def create_csv(all_boards):
  ''' from a list of all_boards
  creates a csv file of these boards'''
  with open("matchboxes.csv", 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    for i,board in enumerate(all_boards):
      writer.writerow([i])
      for row in np.array(board).reshape(3,3):
        writer.writerow(row)
      writer.writerow([])
      writer.writerow([])




all_boards_initial_states = []
for board in all_boards:
  all_boards_initial_states.append(get_initial_state(board))


def display_initial_states(all_boards_initial_states):
  print('[',end ='')
  for board in all_boards_initial_states:
    print(board, end = ', ')
  print(']')


def display_beads_in_positions(all_boards_initial_states):
  ''' shows how many beads of each type will be required'''
  bead_dict = {i:0 for i in range(9)}
  
  for board in all_boards_initial_states:
    for i, element in enumerate(board):
      if type(element) is int:
        bead_dict[i] += element
  print(bead_dict)
  
  print(sum(bead_dict[i] for i in range(9)))


#display_initial_states(all_boards_initial_states)
      