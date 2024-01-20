#####################################
#
#  Visual object recognition based
#          Go bot interface
#
#                 by
#
#          Code Monkey King
#
#####################################

# Packages
import sys
import cv2
import numpy as np
import pyautogui as pg
import time
import pexpect
import random
import os

# Constants (modify according to your screenshot parameters)
CELL_SIZE = 28
MATCH_SIZE = int((CELL_SIZE - 12) / 2)
BOARD_TOP_COORD = 325 - CELL_SIZE * 2
BOARD_LEFT_COORD = 45 - CELL_SIZE * 2
GAMES = '../db/Cho_Chikun/'
COLOR = 'Black'
SINCE = 2000

# Go playing program
ENGINE = 'pachi'
BOARD_SIZE = 19
KOMI = 5.5

# Players
WHITE = 0
BLACK = 1

# Side to move
side_to_move = BLACK

# Game database
database = []

# Moves of the game
position = ''

# Coordinates of vertices
set_square = {}

# Array to convert board square indices to coordinates
get_square = [
  'A19', 'B19', 'C19', 'D19', 'E19', 'F19', 'G19', 'H19', 'J19', 'K19', 'L19', 'M19', 'N19', 'O19', 'P19', 'Q19', 'R19', 'S19', 'T19',
  'A18', 'B18', 'C18', 'D18', 'E18', 'F18', 'G18', 'H18', 'J18', 'K18', 'L18', 'M18', 'N18', 'O18', 'P18', 'Q18', 'R18', 'S18', 'T18',
  'A17', 'B17', 'C17', 'D17', 'E17', 'F17', 'G17', 'H17', 'J17', 'K17', 'L17', 'M17', 'N17', 'O17', 'P17', 'Q17', 'R17', 'S17', 'T17',
  'A16', 'B16', 'C16', 'D16', 'E16', 'F16', 'G16', 'H16', 'J16', 'K16', 'L16', 'M16', 'N16', 'O16', 'P16', 'Q16', 'R16', 'S16', 'T16',
  'A15', 'B15', 'C15', 'D15', 'E15', 'F15', 'G15', 'H15', 'J15', 'K15', 'L15', 'M15', 'N15', 'O15', 'P15', 'Q15', 'R15', 'S15', 'T15',
  'A14', 'B14', 'C14', 'D14', 'E14', 'F14', 'G14', 'H14', 'J14', 'K14', 'L14', 'M14', 'N14', 'O14', 'P14', 'Q14', 'R14', 'S14', 'T14',
  'A13', 'B13', 'C13', 'D13', 'E13', 'F13', 'G13', 'H13', 'J13', 'K13', 'L13', 'M13', 'N13', 'O13', 'P13', 'Q13', 'R13', 'S13', 'T13',
  'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12', 'J12', 'K12', 'L12', 'M12', 'N12', 'O12', 'P12', 'Q12', 'R12', 'S12', 'T12',
  'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'J11', 'K11', 'L11', 'M11', 'N11', 'O11', 'P11', 'Q11', 'R11', 'S11', 'T11',
  'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'J10', 'K10', 'L10', 'M10', 'N10', 'O10', 'P10', 'Q10', 'R10', 'S10', 'T10',
  'A9',  'B9',  'C9',  'D9',  'E9',  'F9',  'G9',  'H9',  'J9',  'K9',  'L9',  'M9',  'N9',  'O9',  'P9',  'Q9',  'R9',  'S9',  'T9',
  'A8',  'B8',  'C8',  'D8',  'E8',  'F8',  'G8',  'H8',  'J8',  'K8',  'L8',  'M8',  'N8',  'O8',  'P8',  'Q8',  'R8',  'S8',  'T8',
  'A7',  'B7',  'C7',  'D7',  'E7',  'F7',  'G7',  'H7',  'J7',  'K7',  'L7',  'M7',  'N7',  'O7',  'P7',  'Q7',  'R7',  'S7',  'T7',
  'A6',  'B6',  'C6',  'D6',  'E6',  'F6',  'G6',  'H6',  'J6',  'K6',  'L6',  'M6',  'N6',  'O6',  'P6',  'Q6',  'R6',  'S6',  'T6',
  'A5',  'B5',  'C5',  'D5',  'E5',  'F5',  'G5',  'H5',  'J5',  'K5',  'L5',  'M5',  'N5',  'O5',  'P5',  'Q5',  'R5',  'S5',  'T5',
  'A4',  'B4',  'C4',  'D4',  'E4',  'F4',  'G4',  'H4',  'J4',  'K4',  'L4',  'M4',  'N4',  'O4',  'P4',  'Q4',  'R4',  'S4',  'T4',
  'A3',  'B3',  'C3',  'D3',  'E3',  'F3',  'G3',  'H3',  'J3',  'K3',  'L3',  'M3',  'N3',  'O3',  'P3',  'Q3',  'R3',  'S3',  'T3',
  'A2',  'B2',  'C2',  'D2',  'E2',  'F2',  'G2',  'H2',  'J2',  'K2',  'L2',  'M2',  'N2',  'O2',  'P2',  'Q2',  'R2',  'S2',  'T2',
  'A1',  'B1',  'C1',  'D1',  'E1',  'F1',  'G1',  'H1',  'J1',  'K1',  'L1',  'M1',  'N1',  'O1',  'P1',  'Q1',  'R1',  'S1',  'T1',
];

# Build games database
def init_db():
  global side_to_move, COLOR
  for filename in os.listdir(GAMES):
    with open(GAMES + filename) as f:
      game = f.read()
      player = 'PB' if side_to_move == BLACK else 'PW'
      color = game.split(player + '[')[1].split(']')[0]
      if color == 'Cho Chikun':
        try: result = game.split('RE[')[1].split(']')[0][0]
        except: pass
        if result == COLOR[0]:
          moves = game.split('DT')[-1].split('\n\n')[-1][:-2].replace('\n', '')
          database.append(moves)
  print(len(database), 'Cho Chikun games loaded')

# Query database
def query_db(position):
  responses = set()
  for i in range(len(database)):
    if len(position) and position in database[i]:
      try:
        next_move = database[i].split(position)[-1].split(';')[1]
        if database[i][0:4] == position[0:4]: responses.add(next_move)
      except: pass
  return list(responses)

# Init square to coordinates array
def init_coords():
  # Board top left corner coords
  x = BOARD_LEFT_COORD + CELL_SIZE
  y = BOARD_TOP_COORD + CELL_SIZE

  # Loop over board rows
  for col in range(BOARD_SIZE):
    # Loop over board columns
    for row in range(BOARD_SIZE):
      # Init vertice
      square = row * BOARD_SIZE + col
      
      # Associate square with square center coordinates
      set_square.update({'ABCDEFGHJKLMNOPQRST'[row]+str(BOARD_SIZE-col): (int(x+CELL_SIZE/2), int(y+CELL_SIZE/2))})

      # Increment x coord by cell size
      x += CELL_SIZE + 1
    
    # Restore x coord, increment y coordinate by cell size
    x = BOARD_LEFT_COORD + CELL_SIZE
    y += CELL_SIZE + 1

# Convert screen to board coordinates
def locate_stone(color):
  # Take a screenshot to locate objects on
  screenshot = pg.screenshot()

  # Adjust colors
  screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

  # Locate stone on a screenshot
  try:
    stone = pg.locateOnScreen('../img/playok-' + color + '.png', confidence=0.9)
    col = int((stone.left - MATCH_SIZE - BOARD_LEFT_COORD) / CELL_SIZE) - 1
    row = int((stone.top - MATCH_SIZE - BOARD_TOP_COORD) / CELL_SIZE) - 1
    move = get_square[row*19+col]
    return move

  # Failed locate a stone
  except: return ''

# Init engine
def init_engine(ENGINE):
  # Start engine subprocess
  c = pexpect.spawnu(ENGINE)
  
  # Init commands
  init_commands = [
    'name',
    'version',
    'protocol_version',
    'komi ' + str(KOMI),
    'boardsize ' + str(BOARD_SIZE),
    'clear_board'
  ]
  
  # Init engine
  for command in init_commands:
    c.sendline(command)
    c.expect('= (.*)', timeout = -1)
    print(command + '\n' + c.after.strip())

  # Engine subprocess
  return c

# Print board
def print_board(c):
  # Print board
  c.sendline('showboard')
  c.expect('= (.*)', timeout = -1)
  print(c.after.split('=')[-1].replace('stones', '').replace('has', ''))

  # Estimate score
  c.sendline('score_est')
  c.expect('= (.*)', timeout = -1)
  print(c.after.split('=')[-1])

# Engine plays game
def play_game():
  global side_to_move, position
  # Start engine subprocess
  c = init_engine(ENGINE)

  # Init opening database
  init_db()

  # Make first move is side is BLACK
  if side_to_move == BLACK:
    random_game = random.choice(database)
    book_move = random_game.split(';')[1]
    position += ';' + book_move
    col = 'abcdefghjklmnopqrst'['abcdefghijklmnopqrs'.index(book_move[2])].upper()
    row = str(19 - 'abcdefghijklmnopqrs'.index(book_move[3]))
    best_move = col + row
    print(' Book move:', best_move)
    c.sendline('play ' + book_move[0] + ' ' + best_move)
    c.expect('= (.*)', timeout = -1)
    old_move = best_move
    print_board(c)
    pg.moveTo(set_square[best_move])
    pg.click()

  # Old move
  old_move = ''
  
  # Play game
  while True:
    # Pick up opponent's color
    color = 'white' if side_to_move == BLACK else 'black'

    # Wait for opponent's move
    move = ''
    move = locate_stone(color)
    if move == '' or move == old_move: continue
    
    # Update board with user move and make engine move
    try:
      # Sync engine
      c.sendline('play ' + color[0].upper() + ' ' + move)
      c.expect('= (.*)', timeout = -1)
      old_move = move
      print(' Parsed move:', move)
      print_board(c)

      # Generate move
      col = 'abcdefghijklmnopqrs'['abcdefghjklmnopqrst'.index(move[0].lower())]
      row = ' srqponmlkjihgfedcba'[int(move[1:])]
      position += ';' + color.capitalize()[0] + '[' + col + row + ']'
      responses = query_db(position)

      if len(responses):
        book_move = random.choice(responses)
        col = 'abcdefghjklmnopqrst'['abcdefghijklmnopqrs'.index(book_move[2])].upper()
        row = str(19 - 'abcdefghijklmnopqrs'.index(book_move[3]))
        best_move = col + row
        position += ';' + book_move
        print(' Book move:', best_move)
        c.sendline('play ' + book_move[0] + ' ' + best_move)
        c.expect('= (.*)', timeout = -1)
        print_board(c)
      else:
        c.sendline('genmove ' + ('B' if side_to_move == BLACK else 'W'))
        c.expect('\n= (.*)', timeout = -1)
        best_move = c.after.split("=")[-1].strip()
        print(' Generated move:', best_move)
        print_board(c)

      # Make engine move
      pg.moveTo(set_square[best_move])
      pg.click()
    
    # Error updating board
    except Exception as e:
      print('Game finished!')
      sys.exit(0)

# Calibrate screen coordinates (debug)
def calibrate():
  global side_to_move
  old_move = ''

  # Init engine
  c = init_engine(ENGINE)

  # Init opening database
  init_db()

  while True:
    # Parse move
    color = 'black' if side_to_move else 'white'
    move = locate_stone(color)

    # Follow move
    if move != '' and move != old_move:
      old_move = move
      print(color.capitalize() + ' moved to ' + move)
     
      # Sync engine
      c.sendline('play ' + color[0].upper() + ' ' + move)
      c.expect('= (.*)', timeout = -1)
      
      # Move cursor to last move
      pg.moveTo(set_square[move])

      # Change side
      side_to_move ^= 1

# Main driver
if __name__ == '__main__':
  init_coords()
  if len(sys.argv) == 2:
    side_to_move = BLACK if sys.argv[1] == 'black' else WHITE
    COLOR = sys.argv[1].capitalize()
    play_game()
  else:
    print('usage: "playok-go.py white" or "playok-go.py black"\n')
    print(' Now running in calibration mode...\n')
    print('1. Open web browser on half of the screen on the left')
    print('2. Open playok.com, choose any game played between players')
    print('3. Maximize board size using "+"')
    print('4. Mouse pointer should follow the last move made on board\n')
    print(' If it doesn\'t work:\n')
    print('1. Set BOARD_TOP_COORD = px from top screen edge to board top line')
    print('2. Set BOARD_LEFT_COORD = px from left screen edge to board left line')
    print('3. Set CELL_SIZE = distance between board cell vertices')
    print('4. Optionally create custom "white.png" and "black.png" images')
    print('5. Set MATCH_SIZE to your "black.png" width\n')
    print(' Calibrate until the mouse pointer pefectly matches the stone.')
    calibrate()
