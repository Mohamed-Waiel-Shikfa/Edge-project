import pygame
from pygame.locals import *
import local_game_elements5 as el

pygame.init()


# erase a logic gate instance as well as its output line and delink the line from the next element in the logic circuit
def remove_inst(pos):
    for i in inst_logic_gate:
        for x in i:
            endpos = x.endpos
            if endpos[0] <= pos[0] <= endpos[0] + 50 and endpos[1] <= pos[1] <= endpos[1] + 25:
                for o in out_conn:
                    for oo in o:
                        for l in x.lines:
                            if oo.link_to == l:
                                oo.link_to = None
                i.remove(x)


# erase line and delink the line from the next element in the logic circuit
def remove_line(pos, tolerance=3):
    lines_to_remove = []
    for x in lines:
        x1, y1 = x.rect.x + 4, x.rect.y + 4
        x2, y2 = x.end_pos
        a = round((y2 - y1) / (x2 - x1), 3)
        b = round(y1 - a * x1, 3)
        if abs(pos[1] - (a * pos[0] + b)) < tolerance and min(x1, x2) <= pos[0] <= max(x1, x2) and min(y1, y2) <= pos[
            1] <= max(y1, y2):
            lines_to_remove.append(x)

    for x in lines_to_remove:
        lines.remove(x)


# draws every single element on the frame and update the frame, is called at the ened of thegame loop
def draw_game():
    # screen filler to erase everything on screen to draw next frame
    win.fill((0, 0, 0))

    # drawing playground
    pygame.draw.rect(win, (150, 150, 150), playground)

    # drawing input bits and their connector
    for x in range(2):
        for i in range(nb_bit):
            inbit[x][i].draw(win, img_bit_dflt, img_bit_hover, img_bit_clicked)
            in_conn[x][i].draw(win, coord_in_bit[x][0] + 37.5, coord_in_bit[x][1] + 37.5 * i + 10)
    inbit[2][0].draw(win, img_bit_dflt, img_bit_hover, img_bit_clicked)
    in_conn[2][0].draw(win, 87.5, 435)

    # drawing every output bit and their connector
    for i in range(nb_bit):
        out_bit[0][i].draw(win, img_bit_dflt, img_bit_clicked)
        out_conn[0][i].draw(win, coord_out_bit[0][0] - 27.5, coord_out_bit[0][1] + 37.5 * i + 10)
    for i in range(3):
        out_bit[1][i].draw(win, img_bit_dflt, img_bit_clicked)
        out_conn[1][i].draw(win, coord_out_bit[1][0] - 27.5, coord_out_bit[1][1] + 37.5 * i + 10)

    # drawing create button
    create_btn.draw(win)

    # drawing logic buttons
    for i in logic_btn:
        i.draw(win)

    # drawing menu buttons
    menu_btn.draw(win)

    # drawing input bit counter
    win.blit(big_font.render(str(sumx[0]), True, white), (20, 110))
    win.blit(big_font.render(str(sumx[1]), True, white), (20, 295))

    # logic gate instance
    for i, x in enumerate(inst_logic_gate):
        if x:
            for z, y in enumerate(x):
                y.draw(win)

    # lines
    for i, x in enumerate(lines):
        if x:
            x.draw(win)

    # drawing screen output
    scaled_win = pygame.transform.smoothscale(win, screen.get_size())
    screen.blit(scaled_win, (0, 0))
    pygame.display.flip()


# init window
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
win = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# image loading
img_bit_dflt = pygame.image.load('bit default.png').convert_alpha()
img_bit_hover = pygame.image.load('bit hover.png').convert_alpha()
img_bit_clicked = pygame.image.load('bit clicked.png').convert_alpha()
img_create_btn = pygame.image.load('bottombuttons.png').convert_alpha()
img_logic_btn = pygame.image.load('bottombuttons.png').convert_alpha()
img_menu_btn = pygame.image.load('bottombuttons.png').convert_alpha()
img_conn = pygame.image.load('connector.png').convert_alpha()
img_blank = pygame.image.load('blank image.png').convert_alpha()

# text init
white = (255, 255, 255)
big_font = pygame.font.SysFont('Cascadia Mono SemiLight', 35)
small_font = pygame.font.SysFont('Cascadia Mono SemiLight', 16)
# variable init
nb_bit = 4
grp_in_bit = 3
grp_out_bit = 2
coord_in_bit = [[50, 50], [50, 237.5]]
coord_out_bit = [[885, 112.5], [885, 300]]
coord_create_btn = [62.5, 495]
coord_menu_btn = [900, 495]
inbit = [[], [], []]
out_bit = [[], []]
in_conn = [[], [], []]
out_conn = [[], []]
logic_btn = []
logic_btn_txt = ["AND", "NOT", "NAND", "OR", "XOR"]
inst_logic_gate = [[], [], [], [], []]
lines = []
lastline = False
state = True
instructions = "Instructions:"
instrtxt = ["Right click :", "         On a logic gate button to create an instance of this gate",
            "         On a connector (dot) to start a line", "         On one of the left/input bit to flip its value",
            "         On menu button to switch between instruction and the running simulation",
            "Left click functions :",
            "         To set position of the gate instance", "         To finish line", "Middle mouse button click :",
            "         To remove a logic gate or a line"]

# input bit object and input connector object init
for i in range(nb_bit):
    inbit[0].append(el.in_bit(coord_in_bit[0][0], coord_in_bit[0][1] + 37.5 * i, img_bit_dflt))
    inbit[1].append(el.in_bit(coord_in_bit[1][0], coord_in_bit[1][1] + 37.5 * i, img_bit_dflt))
    in_conn[0].append(el.conn(coord_in_bit[0][0] + 37.5, coord_in_bit[0][1] + 37.5 * i + 10, img_conn))
    in_conn[1].append(el.conn(coord_in_bit[1][0] + 37.5, coord_in_bit[1][1] + 37.5 * i + 10, img_conn))
inbit[2].append(el.in_bit(50, 425, img_bit_dflt))
in_conn[2].append(el.conn(87.5, 435, img_conn))

# linking in bit and in conn
for i in range(nb_bit):
    in_conn[0][i].makelink(inbit[0][i])
    in_conn[1][i].makelink(inbit[1][i])
in_conn[2][0].makelink(inbit[2][0])

# output bit object and output connector object init
for i in range(nb_bit):
    out_conn[0].append(el.conn(coord_out_bit[0][0] - 27.5, coord_out_bit[0][1] + 37.5 * i + 10, img_conn))
    out_bit[0].append(el.out_bit(coord_out_bit[0][0], coord_out_bit[0][1] + 37.5 * i, out_conn[0][i], img_bit_dflt))
for i in range(3):
    out_conn[1].append(el.conn(coord_out_bit[1][0] - 27.5, coord_out_bit[1][1] + 37.5 * i + 10, img_conn))
    out_bit[1].append(el.out_bit(coord_out_bit[1][0], coord_out_bit[1][1] + 37.5 * i, out_conn[1][i], img_bit_dflt))

# create button init
create_btn = el.create(coord_create_btn[0], coord_create_btn[1], img_create_btn)

# logic buttons init
for i in range(5):
    x, y = 2, 1
    if logic_btn_txt[i] == "NOT":
        x = 1
    logic_btn.append(el.logic_btn(122.5 + 60 * i, 495, img_logic_btn, logic_btn_txt[i], x, y))

# menu button init
menu_btn = el.menu(coord_menu_btn[0], coord_menu_btn[1], img_menu_btn)
menu_btn1 = el.menu(coord_menu_btn[0] - 75, coord_menu_btn[1], img_menu_btn)

# playground object init
playground = pygame.Rect((62.5, 25, 835, 450))

# game loop
run = True
while run:
    # getting mouse position at beginning because it is used every where
    pos = pygame.mouse.get_pos()

    # event handler
    for event in pygame.event.get():
        # quit event handler
        if event.type == QUIT:
            run = False
        # screen resize handler
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
            win = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # middle mouse click to be sure it isn't accidental, call the remove line on top
    if pygame.mouse.get_pressed()[1]:
        # Remove lines if the mouse is over them
        remove_inst(pos)
        remove_line(pos)

    if pygame.mouse.get_pressed()[0] and menu_btn.rect.collidepoint(pos) and menu_btn.changestate():
        state = False
    if pygame.mouse.get_pressed()[0] and menu_btn1.rect.collidepoint(pos) and menu_btn1.changestate():
        state = True

    # determining input bits value
    sumx = [0, 0]
    for x in range(2):
        for i in range(nb_bit):
            if inbit[x][i].onvalue_inbit():
                if i == 0:
                    sumx[x] -= 2 ** (nb_bit - 1 - i)
                else:
                    sumx[x] += 2 ** (nb_bit - 1 - i)
    inbit[2][0].onvalue_inbit()

    # makes instances of the correct logic type when condition for it are met, see el:x.makeinstance
    for i, x in enumerate(logic_btn):
        if x.makeinstance():
            inst_logic_gate[i].append(
                el.logic_btn_inst(0, 0, img_logic_btn, img_conn, (x.type1, x.nb_in_conn, x.nb_out_conn)))

    # make lines from in conn and if so save that last line was made in this file
    for z in in_conn:
        for x in z:
            if x.makeline():
                lines.append(el.line(x.rect.x, x.rect.y, x, img_blank))
                lastline = True

    # goes over all out conn and logic gate instances in conn, checks if any is colliding with mouse and being pressed
    # if so verify if lastline was made here or from a logic gate instance
    # finally if all conditions are met it finishes the line make necassary link and reset last line
    for z in out_conn:
        for x in z:
            if x.rect.collidepoint(pos) and pygame.mouse.get_pressed()[2]:
                if lastline:
                    lines[-1].finish(True)
                    x.makelink(lines[-1])
                    lastline = False
                else:
                    for t in inst_logic_gate:
                        for r in t:
                            if r.lastline:
                                r.lines[-1].finish(True)
                                x.makelink(r.lines[-1])
                                r.lastline = False
    for z in inst_logic_gate:
        for y in z:
            for x in y.in_conn:
                if x.rect.collidepoint(pos) and pygame.mouse.get_pressed()[2]:
                    if lastline:
                        lines[-1].finish(True)
                        x.makelink(lines[-1])
                        lastline = False
                    else:
                        for t in inst_logic_gate:
                            for r in t:
                                if r.lastline:
                                    r.lines[-1].finish(True)
                                    x.makelink(r.lines[-1])
                                    r.lastline = False

    # Draw the rectangles based on the menu_state
    if state:
        # draws game as explained on top
        draw_game()
    else:
        # screen filler to erase everything on screen to draw next frame
        win.fill((0, 0, 0))

        # drawing menu buttons
        menu_btn1.draw(win)

        # drawing input bit counter
        win.blit(big_font.render(instructions, True, white), (380, 40))
        # drawing input bit counter
        for d, i in enumerate(instrtxt):
            win.blit(small_font.render(i, True, white), (20, 110 + 35 * d))

        # drawing screen output
        scaled_win = pygame.transform.smoothscale(win, screen.get_size())
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()

# close pygame window
pygame.quit()
