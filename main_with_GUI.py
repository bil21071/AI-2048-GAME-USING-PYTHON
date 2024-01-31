from logging import root
from tkinter import Frame, Label, CENTER
from tkinter import *
import pyfiglet


import game_ai
import game_functions
import threading


EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"

LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#a6bdbb"

EMPTY_COLOR = "#8eaba8"

TILE_COLORS = {2: "#daeddf", 4: "#9ae3ae", 8: "#6ce68d", 16: "#42ed71",
               32: "#17e650", 64: "#17c246", 128: "#149938",
               256: "#107d2e", 512: "#0e6325", 1024: "#0b4a1c",
                   2048: "#031f0a", 4096: "#000000", 8192: "#000000", }

LABEL_COLORS = {2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                   32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                   256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
                   2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0", }

print("++++++++++++++++++++++++++++++++++++")
f = pyfiglet.Figlet(font='larry3d')
print(f.renderText('2 0 4 8'))
print("++++++++++++++++++++++++++++++++++++")
print('2 new windows will be open one with actual gameplay and other with control buttons....')


class Display(Frame):
    def __init__(self):
        self.NEW_TILE_MODE = "COMPUTER"
        self.PLAYAI = False
        Frame.__init__(self)

        self.grid()
        self.master.title('2048 - Main GamePlay')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up,
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left,
                         RIGHT_KEY: game_functions.move_right,
                         AI_KEY: game_ai.ai_move,
                         }

        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()

        thread = threading.Thread(target=self.newWindow)
        thread.start()

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def newWindow(self):
        newWindow = Toplevel()
        newWindow.title("Controls for 2048 Game")
        newWindow.geometry('1000x600')
        l = Label(newWindow,
                  text='A 2048 that runs on AI')
        l.config(font=('Times', 20))

        l2 = Label(newWindow,
                   text="To initiate AI click the button or press p on 2048 gameplay window\nTo quit AI click the button or press q on 2048 gameplay window\nTo generate new tiles by user click the button\nuse w,a,s,d to play game\nEnjoy :)")
        l2.config(font=("Times", 15))
        self.toggle_button = Button(
            newWindow, text="INITIATE AI",  width=20, command=self.Simpletoggle)
        self.toggle_button.config(
            font=('Times', 17), background='grey', relief=RIDGE, fg='white')
        self.toggle_new_tile_button = Button(
            newWindow, text="Click to generate New Tiles by User", width=30, command=self.SimpletoggleNew)
        self.toggle_new_tile_button.config(
            font=('Times', 17), background='grey', relief=RIDGE, fg='white')
        self.next_btn = Button(
            newWindow, text="Let the AI play single very next move!!", width=30, command=self.verynext)
        self.next_btn.config(
            font=('Times', 17), background='grey', relief=RIDGE, fg='white')
        l.place(x=370, y=50)
        l2.place(x=250, y=80)
        self.toggle_button.place(x=380, y=220)
        self.toggle_new_tile_button.place(x=310, y=285)
        self.next_btn.place(x=310, y=350)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()

    def key_press(self, event):

        key = repr(event.char)
        if key == AI_PLAY_KEY:
            thread2 = threading.Thread(target=self.AIp)
            thread2.start()
        if key == AI_KEY:
            thread3 = threading.Thread(target=self.AIq)
            thread3.start()

        elif key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(
                event.char)](self.matrix)
            if move_made:
                self.draw_grid_cells()
                if self.NEW_TILE_MODE == "COMPUTER":
                    self.matrix = game_functions.add_new_tile_by_random(
                        self.matrix)
                if self.NEW_TILE_MODE == "USER":
                    self.matrix = game_functions.add_new_tile_by_user(
                        self.matrix)
                self.draw_grid_cells()
                move_made = False
            game_functions.check_for_win(self.matrix)

    def Simpletoggle(self):

        if self.toggle_button.config('text')[-1] == 'INITIATE AI':
            thread2 = threading.Thread(target=self.AIp)
            thread2.start()
        else:

            thread3 = threading.Thread(target=self.AIq)
            thread3.start()

    def SimpletoggleNew(self):
        if self.toggle_new_tile_button.config('text')[-1] == 'Click to generate New Tiles by User':
            self.toggle_new_tile_button.config(
                text='Click to generate New Tiles by Random')
            self.NEW_TILE_MODE = "USER"
            print('\nTiles will be generated by User!!!')
        else:
            self.toggle_new_tile_button.config(
                text='Click to generate New Tiles by User')
            self.NEW_TILE_MODE = "COMPUTER"
            print('\nTiles will be generated by computer!!!')

    def AIp(self):

        self.toggle_button.config(text='OFF THE AI')
        print('\nAI has been initiated!!!')
        valid_game = True
        self.PLAYAI = True
        move_count = 0

        while valid_game and self.PLAYAI == True:
            self.matrix, valid_game = game_ai.ai_move(self.matrix, 40, 40)
            if valid_game:
                self.draw_grid_cells()
                if self.NEW_TILE_MODE == "COMPUTER":
                    self.matrix = game_functions.add_new_tile_by_random(
                        self.matrix)
                if self.NEW_TILE_MODE == "USER":
                    self.matrix = game_functions.add_new_tile_by_user(
                        self.matrix)
                self.draw_grid_cells()
            move_count += 1

    def AIq(self):
        self.toggle_button.config(text='INITIATE AI')
        self.PLAYAI = False
        print('\nAI shutted down!!!')
        
        self.matrix, move_made = game_ai.ai_move(self.matrix, 40, 40)
        if move_made:
            if self.NEW_TILE_MODE == "COMPUTER":
                self.matrix = game_functions.add_new_tile_by_random(
                    self.matrix)
            if self.NEW_TILE_MODE == "USER":
                self.matrix = game_functions.add_new_tile_by_user(self.matrix)
            self.draw_grid_cells()
            move_made = False

    def verynext(self):
        move_count = 0
        self.matrix, valid_game = game_ai.ai_move(self.matrix, 40, 40)
        print("\nAI has played a single move!!")
        if valid_game:
            self.draw_grid_cells()
            if self.NEW_TILE_MODE == "COMPUTER":
                self.matrix = game_functions.add_new_tile_by_random(
                    self.matrix)
            if self.NEW_TILE_MODE == "USER":
                self.matrix = game_functions.add_new_tile_by_user(self.matrix)
            self.draw_grid_cells()
        move_count += 1


gamegrid = Display()
