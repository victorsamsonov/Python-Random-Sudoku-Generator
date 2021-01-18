import pygame
from Sudoku import complete_sudoku, is_valid, generate_random_sudoku, show_sudoku, is_empty
import time
from Board import Board


class Game(Board):
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Victor Samsonov Sudoku")
    # Allows to deselect the boxes
    prev_val = None
    # left margin
    lm = 70
    # top margin
    tm = 100

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        # Difficulty menu state
        self.difficulty_state = False
        # Start section state
        self.start_state = False
        self.w, self.h = 1080, 1000
        self.display = pygame.Surface((self.w, self.h))
        self.window = pygame.display.set_mode((self.w, self.h))
        self.font = '8-BIT WONDER.TTF'
        self.black_font = (0, 0, 0)
        self.white_font = (255, 255, 255)
        self.board = Board(9, 9, 540, 540, Board.m1)
        self.chances = 6
        self.strikes = 0
        self.key = None
        self.menu_state = True
        # General cursor
        self.cursor_rect = pygame.font.SysFont("8-BIT-WONDER", 55).render("X", 1, (76, 175, 80, 1))
        # Current difficulty cursor
        self.difficulty_cursor_y = self.h // 2 + 60 - 125
        self.cursor_x = self.w // 2 - 200
        self.cursor_y = self.h // 2 + 60 - 125
        self.cursor_state = 's'
        self.diff_cursor_y = self.cursor_y
        self.difficulty_cursor_state = '10'
        self.start_cursor_state = 'm1'
        # avoid multiple menu selections in a row
        self.transition = False
        self.empty = None
        self.menu_bg_color = (176,190,197 ,1)

    # Renders the window where the game takes place
    def redraw_window(self, time):
        lm = 70

        self.window.fill(self.menu_bg_color)
        pygame.draw.circle(self.window, (0, 0, 0, 1), (1015, 50), 30)
        pygame.draw.rect(self.window, (0, 0, 0, 1), pygame.Rect(985, 50, 60, self.chances * 67.5))
        pygame.draw.circle(self.window, (0, 0, 0, 1), (1015, int(self.chances * 67.5 + 50)), 30)
        fnt = pygame.font.SysFont("comicsans", 55)
        fnt2 = pygame.font.SysFont('comicsans', 70)
        time = fnt.render("Time " + self.format_time(time), 1, (76, 175, 80, 1))
        menu = fnt.render("M = Back to Menu", 1, (255, 255, 255, 1))
        complete = fnt.render("Press C to complete the board", 1, (0, 0, 0, 1))
        pygame.draw.circle(self.window, (0, 0, 0, 1), (110, 920), 80)
        pygame.draw.circle(self.window, (0, 0, 0, 1), (int(self.w // 1.11), 920), 80)
        pygame.draw.rect(self.window, (0, 0, 0, 1), pygame.Rect(100, 840, 880, 160))

        self.window.blit(time, (105, 900))
        self.window.blit(menu, (self.w // 1.65, 900))
        self.window.blit(complete, (260, 120))
        error = fnt2.render("X ", 2, (255, 0, 0))
        chance = fnt2.render("X ", 2, (76, 175, 80, 1))
        position = []
        position2 = []
        # Updates the chances and strikes
        for i in range(self.chances):
            position2.append((1000, 40 + (i * 50) + lm))
            self.window.blit(chance, position2[i])
        for i in range(self.strikes):
            position.append((1000, 40 + (i * 50) + lm))
            self.window.blit(error, position[i])
        self.board.render(self.window)

    # Renders main menu
    def render_menu(self):
        # self.w // 2 x centered
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 85)
        fnt2 = pygame.font.SysFont("8-BIT-WONDER", 35)
        fn3 = pygame.font.SysFont("8-BIT-WONDER", 105)
        Sudoku = fn3.render("Sudoku", 1, (255, 255, 255, 255))
        MainMenu = fnt.render("Main Menu ", 1, (255, 255, 255, 255))
        Start = fnt.render("Start ", 1, (255, 255, 255, 255))
        Difficulty = fnt.render("Difficulty ", 1, (255, 255, 255, 255))
        Info = fnt2.render("Use arrow keys or w/s to navigate and press enter to select", 1, (255, 255, 255, 255))
        Quit = fnt.render("Quit ", 1, (255, 255, 255, 255))
        self.window.blit(Sudoku, (self.w // 2 - 105, 40))
        self.window.blit(MainMenu, (self.w // 2 - 130, 125))
        self.window.blit(Start, (self.w // 2 - 70, self.h // 2 + y_const - 130))
        self.window.blit(Difficulty, (self.w // 2 - 130, self.h // 2 + 2 * y_const - 130))
        self.window.blit(Quit, (self.w // 2 - 67, self.h // 2 + 3 * y_const - 130))
        self.window.blit(self.cursor_rect, (self.cursor_x, self.cursor_y))
        self.window.blit(Info, (180, self.h / 1.1))

    # renders difficulty menu
    def render_difficulty(self):
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 85)
        Difficulty = fnt.render("Difficulty Menu ", 1, (255, 255, 255, 255))
        if self.chances == 10:
            ten_Chances = fnt.render("10 Chances ", 1, (76, 175, 80, 1))
        else:
            ten_Chances = fnt.render("10 Chances ", 1, (255, 255, 255, 255))
        if self.chances == 6:
            six_Chances = fnt.render("6 Chances ", 1, (76, 175, 80, 1))
        else:
            six_Chances = fnt.render("6 Chances ", 1, (255, 255, 255, 255))
        if self.chances == 3:
            three_Chances = fnt.render("3 Chances ", 1, (76, 175, 80, 1))
        else:
            three_Chances = fnt.render("3 Chances ", 1, (255, 255, 255, 255))
        MainMenu = fnt.render("Main Menu ", 1, (255, 255, 255, 255))
        self.window.blit(Difficulty, (self.w // 2 - 180, 125))
        self.window.blit(ten_Chances, (self.w // 2 - 120, self.h // 2 + y_const - 130))
        self.window.blit(six_Chances, (self.w // 2 - 110, self.h // 2 + 2 * y_const - 130))
        self.window.blit(three_Chances, (self.w // 2 - 110, self.h // 2 + 3 * y_const - 130))
        self.window.blit(MainMenu, (self.w // 2 - 110, self.h // 2 + 4 * y_const - 130))
        self.window.blit(self.cursor_rect, (self.cursor_x, self.cursor_y))

    # renders start
    def render_start(self):
        y_const = 85
        self.window.fill(self.menu_bg_color)
        fnt = pygame.font.SysFont("8-BIT-WONDER", 85)
        Select = fnt.render("Select A Map ", 1, (255, 255, 255, 255))
        map1 = fnt.render("Sudoku 1 ", 1, (255, 255, 255, 255))
        map2 = fnt.render("Sudoku 2 ", 1, (255, 255, 255, 255))
        random = fnt.render("Random ", 1, (255, 255, 255, 255))
        MainMenu = fnt.render("Main Menu ", 1, (255, 255, 255, 255))
        self.window.blit(Select, (self.w // 2 - 150, 125))
        self.window.blit(map1, (self.w // 2 - 110, self.h // 2 + y_const - 130))
        self.window.blit(map2, (self.w // 2 - 110, self.h // 2 + 2 * y_const - 130))
        self.window.blit(random, (self.w // 2 - 110, self.h // 2 + 3 * y_const - 130))
        self.window.blit(MainMenu, (self.w // 2 - 110, self.h // 2 + 4 * y_const - 130))
        self.window.blit(self.cursor_rect, (self.cursor_x, self.cursor_y))

    # Stops all loops
    def close_game(self):
        self.menu_state = False
        self.running = False
        self.difficulty_state = False
        self.playing = False
        self.start_state = False

    def cursor_position(self):
        # menu state cursor logic
        if self.menu_state:
            if self.cursor_state == 's':
                self.cursor_y = self.h // 2 + 85 - 125
            elif self.cursor_state == 'd':
                self.cursor_y = self.h // 2 + 170 - 125
            elif self.cursor_state == 'q':
                self.cursor_y = self.h // 2 + 255 - 125
        # difficulty state cursor logic
        elif self.difficulty_state:
            if self.difficulty_cursor_state == '10':
                self.cursor_y = self.h // 2 + 85 - 125
            elif self.difficulty_cursor_state == '6':
                self.cursor_y = self.h // 2 + 170 - 125
            elif self.difficulty_cursor_state == '3':
                self.cursor_y = self.h // 2 + 255 - 125
            elif self.difficulty_cursor_state == 'mm':
                self.cursor_y = self.h // 2 + 340 - 125
        # start state cursor logic
        elif self.start_state:
            if self.cursor_state == 'm1':
                self.cursor_y = self.h // 2 + 85 - 125
            elif self.cursor_state == 'm2':
                self.cursor_y = self.h // 2 + 170 - 125
            elif self.cursor_state == 'r':
                self.cursor_y = self.h // 2 + 255 - 125
            elif self.cursor_state == 'mm':
                self.cursor_y = self.h // 2 + 340 - 125

    # Displays time spent in a game
    def format_time(self, secs):
        sec = secs % 60
        minute = secs // 60
        time = " " + str(minute) + ":" + str(sec)
        return time

    # Manages all user inputs/ events for the playing mode
    def main_event_handler(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.START_KEY = 1
                # Move the cursor down with w or down key
                if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    if self.menu_state:
                        if self.cursor_state == 's':
                            self.cursor_state = 'd'
                        elif self.cursor_state == 'd':
                            self.cursor_state = 'q'
                    elif self.difficulty_state:
                        if self.difficulty_cursor_state == '10':
                            self.difficulty_cursor_state = '6'
                        elif self.difficulty_cursor_state == '6':
                            self.difficulty_cursor_state = '3'
                        elif self.difficulty_cursor_state == '3':
                            self.difficulty_cursor_state = 'mm'
                    if self.start_state:
                        if self.cursor_state == 'm1':
                            self.cursor_state = 'm2'
                        elif self.cursor_state == 'm2':
                            self.cursor_state = 'r'
                        elif self.cursor_state == 'r':
                            self.cursor_state = 'mm'
                # Move the cursor up with w or down key
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    if self.menu_state:
                        if self.cursor_state == 'd':
                            self.cursor_state = 's'
                        elif self.cursor_state == 'q':
                            self.cursor_state = 'd'
                    elif self.difficulty_state:
                        if self.difficulty_cursor_state == '6':
                            self.difficulty_cursor_state = '10'
                        elif self.difficulty_cursor_state == '3':
                            self.difficulty_cursor_state = '6'
                        elif self.difficulty_cursor_state == 'mm':
                            self.difficulty_cursor_state = '3'
                    elif self.start_state:
                        if self.cursor_state == 'm2':
                            self.cursor_state = 'm1'
                        elif self.cursor_state == 'r':
                            self.cursor_state = 'm2'
                        elif self.cursor_state == 'mm':
                            self.cursor_state = 'r'
                # Back to menu
                if e.key == pygame.K_m and self.playing:
                    self.playing = False
                    self.menu_state = True
                    self.cursor_state = 's'
                # Inserting temporary value handler
                if e.key == pygame.K_1:
                    self.key = 1
                    self.menu_state = False
                    self.difficulty_state = False
                    self.playing = True
                if e.key == pygame.K_2:
                    self.key = 2
                if e.key == pygame.K_3:
                    self.key = 3
                if e.key == pygame.K_4:
                    self.key = 4
                if e.key == pygame.K_5:
                    self.key = 5
                if e.key == pygame.K_6:
                    self.key = 6
                if e.key == pygame.K_7:
                    self.key = 7
                if e.key == pygame.K_8:
                    self.key = 8
                if e.key == pygame.K_9:
                    self.key = 9
                if e.key == pygame.K_DELETE:
                    self.board.clear()
                    self.key = None
                # Completes Sudoku if C is pressed
                if e.key == pygame.K_c:
                    if self.playing == True:
                        while self.empty:
                            self.board.complete_GUI(self.empty)
                            if self.empty:
                                self.empty.pop(0)

                if e.key == pygame.K_RETURN:
                    # Enter while playing handler
                    if self.playing == True:
                        i, j = self.board.clicked
                        if self.board.squares[i][j].temp_value != 0:
                            if self.board.insert(self.board.squares[i][j].temp_value):
                                print("Success")
                            else:
                                print("Wrong")
                                self.strikes += 1
                            self.key = None
                            if self.board.victory_state():
                                print("Game over")
                                self.playing = False
                    # Go into the start menu
                    elif self.cursor_state == 's':
                        self.menu_state = False
                        self.start_state = True
                        self.transition = True
                        self.cursor_state = 'm1'
                    # Go into difficulty menu
                    elif self.cursor_state == 'd':
                        self.menu_state = False
                        self.difficulty_state = True
                    # Stops the game from running on quit
                    elif self.cursor_state == 'q':
                        self.menu_state = False
                        self.running = False
                    # Go difficulty menu handling
                    if self.difficulty_state == True:
                        if self.difficulty_cursor_state == 'mm':
                            self.difficulty_state = False
                            self.menu_state = True
                            self.cursor_state = 's'
                            self.difficulty_cursor_state = '6'
                        elif self.difficulty_cursor_state == '10':
                            self.chances = 10
                            self.difficulty_cursor_y = self.difficulty_cursor_y
                        elif self.difficulty_cursor_state == '6':
                            self.chances = 6
                            self.difficulty_cursor_y = self.difficulty_cursor_y
                        elif self.difficulty_cursor_state == '3':
                            self.chances = 3
                            self.difficulty_cursor_y = self.difficulty_cursor_y
                    # start handler
                    if self.start_state == True:
                        if self.cursor_state == 'mm':
                            self.start_state = False
                            self.menu_state = True
                            self.cursor_state = 's'
                        # Sudoku 1
                        elif self.cursor_state == 'm1' and self.transition == False:
                            m1 = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
                                  [6, 0, 0, 0, 7, 5, 0, 0, 9],
                                  [0, 0, 0, 6, 0, 1, 0, 7, 8],
                                  [0, 0, 7, 0, 4, 0, 2, 6, 0],
                                  [0, 0, 1, 0, 5, 0, 9, 3, 0],
                                  [9, 0, 4, 0, 6, 0, 0, 0, 5],
                                  [0, 7, 0, 3, 0, 0, 0, 1, 2],
                                  [1, 2, 0, 0, 0, 7, 4, 0, 0],
                                  [0, 4, 9, 2, 0, 6, 0, 0, 7]]

                            self.board = Board(9, 9, 600, 600, m1)
                            self.empty = self.board.is_empty_game()
                            self.start_state = False
                            self.playing = True
                        # Sudoku 2
                        elif self.cursor_state == 'm2' and self.transition == False:
                            m2 = [[8, 1, 0, 0, 3, 0, 0, 2, 7],
                                  [0, 6, 2, 0, 5, 0, 0, 9, 0],
                                  [0, 7, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 9, 0, 6, 0, 0, 1, 0, 0],
                                  [1, 0, 0, 0, 2, 0, 0, 0, 4],
                                  [0, 0, 8, 0, 0, 5, 0, 7, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 8, 0],
                                  [0, 2, 0, 0, 1, 0, 7, 5, 0],
                                  [3, 8, 0, 0, 7, 0, 0, 4, 2]]

                            self.board = Board(9, 9, 600, 600, m2)
                            self.empty = self.board.is_empty_game()
                            self.start_state = False
                            self.playing = True
                            # Random Sudoku
                        elif self.cursor_state == 'r' and self.transition == False:
                            self.board = Board(9, 9, 600, 600, generate_random_sudoku())
                            self.empty = self.board.is_empty_game()
                            self.start_state = False
                            self.playing = True
                        self.transition = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = self.board.click(pos)
                if clicked:
                    self.board.clicked_handler(clicked[0], clicked[1])
                    self.key = None

    # Manages different states
    def state_handler(self):
        pygame.display.set_caption("Victor Samsonov Sudoku")
        self.key = None
        self.strikes = 0
        # General Loop
        while self.running:
            if self.playing:
                start = time.time()
                # Playing state loop
                while self.playing:
                    play_time = round(time.time() - start)
                    self.main_event_handler()
                    if self.board.clicked and self.key != None:
                        self.board.temp(self.key)
                    if self.chances == self.strikes:
                        self.playing = False
                        self.menu_state = True
                        self.cursor_state = 's'
                        self.strikes = 0
                        pygame.display.update()
                    self.redraw_window(play_time)
                    pygame.display.update()
            # Main menu loop
            elif self.menu_state:
                while self.menu_state:
                    self.render_menu()
                    self.main_event_handler()
                    self.cursor_position()
                    pygame.display.update()
            # Difficulty menu loop
            elif self.difficulty_state:
                while self.difficulty_state:
                    self.render_difficulty()
                    self.main_event_handler()
                    self.cursor_position()
                    pygame.display.update()
            # Start loop
            elif self.start_state:
                while self.start_state:
                    self.render_start()
                    self.main_event_handler()
                    self.cursor_position()
                    pygame.display.update()


g = Game()
g.state_handler()
