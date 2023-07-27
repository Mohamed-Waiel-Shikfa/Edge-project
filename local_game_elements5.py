import pygame


class Basic:
    # x coord, y coord, image itself
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image,
                                            (int(image.get_width()), int(image.get_height())))  # create the image
        self.rect = self.image.get_rect()  # creates rectangle
        self.rect.topleft = (x, y)  # coordinates
        self.white = (255, 255, 255)
        self.sfont = pygame.font.SysFont('Cascadia Mono SemiLight', 16)
        self.big_font = pygame.font.SysFont('Cascadia Mono SemiLight', 35)


class in_bit(Basic):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.state = [True, False, False]
        self.clicked = False
        self.onvaluevar = False

    def onvalue_inbit(self):
        # checks pos of mouse and if hovering over button. and checks if it got clicked.
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.state[0]:
                    self.state[0] = False
                    self.state[2] = True
                    self.onvaluevar = True
                else:
                    self.state[0] = True
                    self.state[2] = False
                    self.onvaluevar = False
            else:
                self.state[1] = True
        else:
            self.state[1] = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return self.onvaluevar

    def draw(self, win, imagedefault, imagehover, imageclicked):
        if self.state[1] and not self.state[2]:
            self.image = pygame.transform.scale(imagehover, (int(imagehover.get_width()), int(imagehover.get_height())))
        elif self.state[0]:
            self.image = pygame.transform.scale(imagedefault,
                                                (int(imagedefault.get_width()), int(imagedefault.get_height())))
        else:
            self.image = pygame.transform.scale(imageclicked,
                                                (int(imageclicked.get_width()), int(imageclicked.get_height())))
        # draws bits on screen
        win.blit(self.image, (self.rect.x, self.rect.y))


class out_bit(Basic):
    def __init__(self, x, y, z, image):
        super().__init__(x, y, image)
        self.link_to = z
        self.onvaluevar = False

    def draw(self, win, imagedefault, imageclicked):
        self.onvalue_outbit()
        if self.onvaluevar:
            self.image = pygame.transform.scale(imageclicked,
                                                (int(imageclicked.get_width()), int(imageclicked.get_height())))
        else:
            self.image = pygame.transform.scale(imagedefault,
                                                (int(imagedefault.get_width()), int(imagedefault.get_height())))
        # draws bits on screen
        win.blit(self.image, (self.rect.x, self.rect.y))

    def onvalue_outbit(self):
        if self.link_to is not None:
            self.onvaluevar = self.link_to.onvaluevar
        return self.onvaluevar


class logic_btn(Basic):
    def __init__(self, x, y, image, type1, nb_in_conn, nb_out_conn):
        super().__init__(x, y, image)
        self.clicked = False
        self.type1 = type1
        self.nb_in_conn = nb_in_conn
        self.nb_out_conn = nb_out_conn

    def makeinstance(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
            0] == 1 and self.clicked == False:
            self.clicked = True
            return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(self.sfont.render(self.type1, True, self.white), (self.rect.x + 5.5, self.rect.y + 8.5))


class logic_btn_inst(Basic):
    def __init__(self, x, y, image, img_conn, conn_info):
        super().__init__(x, y, image)
        self.endpos = None
        self.type1 = conn_info[0]
        self.nb_in_conn = conn_info[1]
        self.nb_out_conn = conn_info[2]
        self.in_conn = []
        self.out_conn = []
        for _ in range(self.nb_in_conn):
            self.in_conn.append(conn(0, 0, img_conn))
        for _ in range(self.nb_out_conn):
            self.out_conn.append(conn(0, 0, img_conn))
        self.img_blank = pygame.image.load('blank image.png').convert_alpha()
        self.lines = []
        self.onvaluevar = False
        self.lastline = False

    def remove_line(self, tolerance=3):
        pos = pygame.mouse.get_pos()
        lines_to_remove = []
        if pygame.mouse.get_pressed()[1]:
            for x in self.lines:
                x1, y1 = x.rect.x + 4, x.rect.y + 4
                x2, y2 = x.end_pos
                a = round((y2 - y1) / (x2 - x1), 3)
                b = round(y1 - a * x1, 3)
                if abs(pos[1] - (a * pos[0] + b)) < tolerance and min(x1, x2) <= pos[0] <= max(x1, x2) and min(y1,
                                                                                                               y2) <= \
                        pos[1] <= max(y1, y2):
                    lines_to_remove.append(x)

            for x in lines_to_remove:
                self.lines.remove(x)

    def add_line(self):
        for x in self.out_conn:
            if x.makeline():
                self.lines.append(line(x.rect.x, x.rect.y, x, self.img_blank))
                self.lastline = True

    def draw(self, win):
        self.onvalue_logic()
        for i in self.out_conn:
            i.onvaluevar = self.onvaluevar
        if self.endpos is not None:
            self.add_line()
            self.remove_line()
            win.blit(self.image, self.endpos)
            win.blit(self.sfont.render(self.type1, True, self.white), (self.endpos[0] + 5.5, self.endpos[1] + 8.5))
            for x, i in enumerate(self.in_conn):
                if self.nb_in_conn % 2 == 1:
                    i.draw(win, self.endpos[0] - 12.5, self.endpos[1] + 6.25 + (x - self.nb_in_conn // 2) * 12.5)
                else:
                    i.draw(win, self.endpos[0] - 12.5, self.endpos[1] + 12.5 + (x - self.nb_in_conn // 2) * 12.5)
            for x, i in enumerate(self.out_conn):
                if self.nb_out_conn % 2 == 1:
                    i.draw(win, self.endpos[0] + 56.25, self.endpos[1] + 6.25 + (x - self.nb_out_conn // 2) * 12.5)
                else:
                    i.draw(win, self.endpos[0] + 56.25, self.endpos[1] + 12.5 + (x - self.nb_out_conn // 2) * 12.5)
        elif not pygame.mouse.get_pressed()[2]:
            win.blit(self.image, pygame.mouse.get_pos())
            win.blit(self.sfont.render(self.type1, True, self.white),
                     (pygame.mouse.get_pos()[0] + 5.5, pygame.mouse.get_pos()[1] + 8.5))
            for x, i in enumerate(self.in_conn):
                if self.nb_in_conn % 2 == 1:
                    i.draw(win, pygame.mouse.get_pos()[0] - 12.5,
                           pygame.mouse.get_pos()[1] + 6.25 + (x - self.nb_in_conn // 2) * 12.5)
                else:
                    i.draw(win, pygame.mouse.get_pos()[0] - 12.5,
                           pygame.mouse.get_pos()[1] + 12.5 + (x - self.nb_in_conn // 2) * 12.5)
            for x, i in enumerate(self.out_conn):
                if self.nb_out_conn % 2 == 1:
                    i.draw(win, pygame.mouse.get_pos()[0] + 56.25,
                           pygame.mouse.get_pos()[1] + 6.25 + (x - self.nb_out_conn // 2) * 12.5)
                else:
                    i.draw(win, pygame.mouse.get_pos()[0] + 56.25,
                           pygame.mouse.get_pos()[1] + 12.5 + (x - self.nb_out_conn // 2) * 12.5)
        else:
            self.endpos = pygame.mouse.get_pos()

        for x in self.lines:
            if x:
                x.draw(win)

    def onvalue_logic(self):
        if self.type1 == "AND":
            if self.in_conn[0].onvaluevar and self.in_conn[1].onvaluevar:
                self.onvaluevar = True
            else:
                self.onvaluevar = False
        elif self.type1 == "NOT":
            if self.in_conn[0].onvaluevar:
                self.onvaluevar = False
            else:
                self.onvaluevar = True
        elif self.type1 == "NAND":
            if not (self.in_conn[0].onvaluevar and self.in_conn[1].onvaluevar):
                self.onvaluevar = True
            else:
                self.onvaluevar = False
        elif self.type1 == "OR":
            if self.in_conn[0].onvaluevar or self.in_conn[1].onvaluevar:
                self.onvaluevar = True
            else:
                self.onvaluevar = False
        else:
            if self.in_conn[0].onvaluevar != self.in_conn[1].onvaluevar:
                self.onvaluevar = True
            else:
                self.onvaluevar = False
        return self.onvaluevar


class menu(Basic):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.clicked = True

    def draw(self, win):
        # draws button on screen
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(self.sfont.render("MENU", True, self.white), (self.rect.x + 9, self.rect.y + 8.5))

    def changestate(self):
        if self.clicked:
            return True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


class create(Basic):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def draw(self, win):
        # draws button on screen
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(self.sfont.render("CREATE", True, self.white), (self.rect.x + 2.5, self.rect.y + 8.5))


class conn(Basic):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.clicked = False
        self.link_to = None
        self.onvaluevar = False

    def draw(self, win, x, y):
        self.onvalue_conn()
        self.rect.x = x
        self.rect.y = y
        win.blit(self.image, (self.rect.x, self.rect.y))

    def makeline(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[
            0] == 1 and self.clicked == False:
            self.clicked = True
            return True
        elif pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            return False
        else:
            return False

    def makelink(self, to_link):
        if self.link_to is None:
            self.link_to = to_link
            self.onvaluevar = self.link_to.onvaluevar

    def onvalue_conn(self):
        if self.link_to is not None:
            self.onvaluevar = self.link_to.onvaluevar
        return self.onvaluevar


class line(Basic):
    def __init__(self, x, y, to_link, image):
        super().__init__(x, y, image)
        self.color = [0, 0, 0]
        self.end_pos = None
        self.onvaluevar = False
        self.link_to = to_link
        self.justfortesting = None

    def draw(self, win):
        self.onvalue_line()
        if self.onvaluevar:
            self.color = [255, 0, 0]
        else:
            self.color = [0, 0, 0]
        if self.end_pos is not None:
            pygame.draw.line(win, tuple(self.color), (self.rect.x + 4, self.rect.y + 4), self.end_pos, 2)

        elif not pygame.mouse.get_pressed()[2]:
            pygame.draw.line(win, tuple(self.color), (self.rect.x + 4, self.rect.y + 4), pygame.mouse.get_pos(), 2)

    def finish(self, x):
        if x and self.end_pos is None and pygame.mouse.get_pressed()[2]:
            self.end_pos = pygame.mouse.get_pos()

    def onvalue_line(self):
        if self.link_to is not None:
            self.onvaluevar = self.link_to.onvaluevar
        return self.onvaluevar
