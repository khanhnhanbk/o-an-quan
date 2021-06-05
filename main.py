from os import truncate
from tkinter import *
import tkinter as tk
import time
import threading
from tkinter.constants import NW, S, SE
import random
from playsound import playsound
from PIL import ImageTk, Image
import trace
root = tk.Tk()

global direcMouse
global res

res = 0
direcMouse = 0

dataPoint = (
    (100, 150),
    (175, 140),
    (225, 140),
    (275, 140),
    (325, 140),
    (375, 140),
    (420, 150),
    (375, 150),
    (325, 150),
    (275, 150),
    (225, 150),
    (175, 150),
    (0, 0),
)
dataImg = (
    (0, 0),
    (175, 125),
    (225, 125),
    (275, 125),
    (325, 125),
    (375, 125),
    (0, 0),
    (375, 175),
    (325, 175),
    (275, 175),
    (225, 175),
    (175, 175),
    (0, 0),
)

dataBackground = (
    (0, 0, 0, 0),
    (151, 101, 199, 149),
    (201, 101, 249, 149),
    (251, 101, 299, 149),
    (301, 101, 349, 149),
    (351, 101, 399, 149),
    (0, 0, 0, 0),
    (351, 151, 399, 199),
    (301, 151, 349, 199),
    (251, 151, 299, 199),
    (201, 151, 249, 199),
    (151, 151, 199, 199),
)

imgs = (
    ImageTk.PhotoImage(Image.open("./images/0.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/1.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/2.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/3.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/4.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/5.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/6.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/7.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/8.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/9.png").resize((50, 50), Image.ANTIALIAS)),
    ImageTk.PhotoImage(Image.open("./images/10.png").resize((50, 50), Image.ANTIALIAS)),
)


def myplaySound():
    playsound("rock.mp3")
def myplayMusic():
    playsound("music.mp3")

class Game:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.name = ''
        self.player1 = computerRandom(1, self)
        self.player2 = Player(2, self)
        self.data = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
        self.turn = True
        self.canvas = canvas
        print("ok")
        self.id = []
        self.select = 0
        self.direct = 0
        self.state = False
        for i in range(12):
            x, y = 0, 0
            if i == 0:
                x, y = (125, 150)
            elif i < 6:
                x, y = (125 + 50 * i, 125)
            elif i == 6:
                x, y = (425, 150)
            else:
                x, y = (125 + 50 * (12 - i), 175)
            if i != 0 and i != 6:
                self.id.append(
                    canvas.create_text(
                        x - 17,
                        y - 18,
                        text=0,
                        fill="darkblue",
                        font="Times 7 bold",
                    )
                )
            else:
                self.id.append(canvas.create_text(
                        x,
                        y,
                        text=0,
                        fill="darkblue",
                        font="Times 20 bold",
                    ))
        # self.resetGame()

    def resetGame(self):
        if self.state == False:
            self.state = True
            self.player1.point = 0
            self.player2.point = 0
            self.data = [10, 5, 5, 5, 5, 5, 10, 5, 5, 5, 5, 5]
            self.turn = True
            print("ok")
            for i in range(12):
                self.canvas.itemconfigure(self.id[i], text=self.data[i])
                if i != 0 and i != 6:
                    self.canvas.itemconfigure(imagCell[i], image = imgs[self.data[i] if self.data[i] < 10 else 10] )
            self.loop()

    def loop(self):
        print(self.data)
        while sum(self.data) > 12:
            if self.turn:
                res = all(self.data[i] == 0 for i in range(1, 6))
                if res:
                    for i in range(1, 6):
                        self.data[i] = 1
                    self.player1.point -= 5
            else:
                res = all(self.data[i] == 0 for i in range(7, 12))
                if res:
                    for i in range(7, 12):
                        self.data[i] = 1
                    self.player2.point -= 5
            for i in range(12):
                self.canvas.itemconfigure(self.id[i], text=self.data[i])
                if i != 0 and i != 6:
                    self.canvas.itemconfigure(imagCell[i], image = imgs[self.data[i] if self.data[i] < 10 else 10] )

            if self.turn:
                self.player1.moving()
                self.canvas.itemconfigure(play1Pnt, text=self.player1.point)
            else:
                self.player2.moving()
                self.canvas.itemconfigure(play2Pnt, text=self.player2.point)
            self.select = -1
            self.direct = 0
            self.canvas.coords(currentPoint, 0, 0, 0, 0)
            self.turn = not self.turn
        self.state = False
        print(self.checkWinner(), self.player1.point, self.player2.point)

        self.canvas.itemconfigure(play1Pnt, text=self.player1.point)
        self.canvas.itemconfigure(play2Pnt, text=self.player2.point)
        self.canvas.itemconfigure(playing, text=str(self.checkWinner()) + "WIN")

    def checkWinner(self):
        print("ok")
        self.player1.point += sum(self.data[1:6])
        self.player2.point += sum(self.data[7:])
        if self.player1.point > self.player2.point:
            return 1
        elif self.player2.point > self.player1.point:
            return 2
        else:
            return 0

    def moved(self, index, direc, canvas: tk.Canvas):
        if self.data[index] == 0:
            return 0
        current = index + direc
        current %= 12

        canvas.itemconfigure(self.id[index], text=0)
        if index != 0 and index != 6:
            self.canvas.itemconfigure(imagCell[index], image = imgs[0] )
        canvas.coords(currentPoint, dataPoint[index][0], dataPoint[index][1], dataPoint[index][0] + 10, dataPoint[index][1] + 10)
        time.sleep(.5)
        ## x = i % 6
        # y = i // 6
        while self.data[index]:
            xCur, yCur = dataPoint[current]
            canvas.coords(currentPoint, xCur, yCur, xCur + 10, yCur + 10)

            self.data[index] -= 1
            myplaySound()
            canvas.itemconfigure(holding, text="Holding\n" + str(self.data[index]))
            self.data[current] += 1
            canvas.itemconfigure(self.id[current], text=self.data[current])
            if current != 0 and current != 6:
                self.canvas.itemconfigure(imagCell[current], image = imgs[self.data[current] if self.data[current] < 10 else 10] )

            current += direc
            current %= 12

            print(self.data)
            time.sleep(0.5)

        if self.data[current] == 0:
            res = 0

            while self.data[current] == 0:
                current += direc
                current %= 12
                if self.data[current]:
                    res += self.data[current]
                    self.data[current] = 0
                    canvas.itemconfigure(self.id[current], text=self.data[current])
                    current += direc
                    current %= 12
                else:
                    return res
            return res
        elif current in (0, 6):
            return 0
        else:
            return self.moved(current, direc, canvas)


class Player:
    def __init__(self, team, game: Game) -> None:
        self.game = game
        self.team = team
        self.point = 0
        self.name = "Player"

    def moving(self):
        print("ok")
        self.game.canvas.coords(
            turn, 100, 40 + (self.team - 1) * 200, 120, 60 + (self.team - 1) * 200
        )
        i = -1
        direct = 0
        while not (
            (i in range(1 - 6 + 6 * self.team, 6 - 6 + 6 * self.team))
            and (direct in (-1, 1))
        ):
            i = self.game.select
            direct = self.game.direct * (1.5 - self.team) * 2

        self.point += self.game.moved(int(i), int(direct), self.game.canvas)
        self.game.direct = 0


class computerRandom:
    def __init__(self, team, game: Game) -> None:
        self.game = game
        self.team = team
        self.name = "Computer"
        self.point = 0

    def moving(self):
        self.game.canvas.coords(
            turn, 100, 40 + (self.team - 1) * 200, 120, 60 + (self.team - 1) * 200
        )
        i = random.choice(range(1 - 6 + 6 * self.team, 6 - 6 + 6 * self.team))
        while self.game.data[i] == 0:
            i = random.choice(range(1 - 6 + 6 * self.team, 6 - 6 + 6 * self.team))
        direct = random.choice((-1, 1))
        self.game.direct = direct
        self.game.select = i

        self.point += self.game.moved(int(i), int(direct), self.game.canvas)
        self.game.direct = 0
        self.game.select = 0


def mouseEvent(event, g: Game):
    res = 0
    x, y = event.x, event.y
    if (100 <= x < 450) & (100 <= y < 200):
        if x < 150:
            res = 0
        elif x > 400:
            res = 6
        else:
            x = (x - 100) // 50
            y = (y - 100) // 50
            res = x if y == 0 else 6 - x + y * 6
        g.select = res
        g.direct = 0
        g.canvas.coords(backgroundSelect, dataBackground[res])
    elif (300 < y < 400) & (200 < x < 300):
        g.direct = -1
    elif (300 < y < 400) & (300 < x < 400):
        g.direct = 1


# def motion(event):
#     x, y = event.x, event.y
#     print("{}, {}".format(x, y))


# root.bind("<Motion>", motion)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
coord = 10, 50, 240, 210
canvas = tk.Canvas(root, width=600, height=400, background="#F8C939", cursor="hand2")
# canvas.create_line(10, 5, 200, 50)
canvas.create_arc(
    100,
    100,
    200,
    200,
    fill="yellow",
    outline="black",
    start=90,
    extent=180,
    width=5,
    style="arc",
)
canvas.create_arc(
    350,
    100,
    450,
    200,
    fill="yellow",
    outline="black",
    start=-90,
    extent=180,
    width=5,
    style="arc",
)
canvas.create_line(150, 100, 400, 100, width=5)
canvas.create_line(150, 150, 400, 150, width=3)
canvas.create_line(150, 200, 400, 200, width=5)

canvas.create_line(400, 100, 400, 200, width=3)
canvas.create_line(150, 100, 150, 200, width=3)
canvas.create_line(200, 100, 200, 200, width=3)
canvas.create_line(250, 100, 250, 200, width=3)
canvas.create_line(300, 100, 300, 200, width=3)
canvas.create_line(350, 100, 350, 200, width=3)
backgroundSelect = canvas.create_rectangle(151, 101, 199, 149, fill="#D8A909")
turn = canvas.create_rectangle(100, 40, 120, 60, fill="#0f0")
imagCell = []
for i in range(12):
    if i == 0 | i == 6:
        imagCell.append(None)
    else:
        imagCell.append(canvas.create_image(dataImg[i], image=imgs[5]))

g = Game(canvas)

canvas.bind("<Button>", lambda event, game=g: mouseEvent(event, game))


canvas.create_rectangle(200, 300, 300, 400)
canvas.create_rectangle(300, 300, 400, 400)
canvas.create_text(250, 350, text="LEFT", fill="#f00", font="Times 20 bold")
canvas.create_text(350, 350, text="RIGHT", fill="#f00", font="Times 20 bold")
holding = canvas.create_text(
    540, 150, text="Holding", fill="#f00", font="Times 20 bold"
)


def thread_fuc():
    g.resetGame()

def startGame():
    if g.state == False:
        t1 = threading.Thread(target=thread_fuc)
        t1.start()
play1 = canvas.create_text(200, 50, text=g.player1.name, fill="#f00", font="Times 20 bold")
play2 = canvas.create_text(200, 250, text=g.player2.name, fill="#f00", font="Times 20 bold")
play1Pnt = canvas.create_text(300, 50, text=0, fill="blue", font="Times 20 bold")
play2Pnt = canvas.create_text(300, 250, text=0, fill="blue", font="Times 20 bold")


playing = canvas.create_text(50, 150, text="", fill="#f00", font="Times 20 bold")

currentPoint = canvas.create_oval(100, 100, 110, 110, fill="red")

tk.Button(root, text= "start", command=startGame).pack()


# def startGame():
#     if t1.is_alive():
#         t1.killed = truncate
#     if not g.state:
#         t1.run()
# tk.Button(root, text= "start", command=startGame).pack()
def getName():
    if variable1.get() == "Humpan":
        g.player1 = Player(1,g)
    else:
        g.player1 = computerRandom(1,g)
    print(g.player1)
    print(variable1.get())
    name = E.get()
    g.player1.name = name
    canvas.itemconfigure(play1, text = name)
E = tk.Entry(root)
E.pack(anchor = CENTER)
B = Button(root, text = "OK", command=getName)
B.pack(anchor = S)
variable1 = StringVar(root)
variable1.set("Computer") # default value

w1= OptionMenu(root, variable1, "Human", "Computer")
w1.pack()



def getName2():
    if variable2.get() == "Human":
        g.player2 = Player(2,g)
    else:
        g.player2 = computerRandom(2,g)
    print(g.player2)
    name = E2.get()
    g.player2.name = name
    canvas.itemconfigure(play2, text = name)

E2 = tk.Entry(root)
E2.pack(anchor = CENTER)
B2 = Button(root, text = "OK", command=getName2)
B2.pack(anchor = S)

variable2 = StringVar(root)
variable2.set("Computer") # default value

w = OptionMenu(root, variable2, "Human", "Computer")
w.pack()

def thread_fuc2():
    while root.winfo_exists():
        myplayMusic()

t2 = threading.Thread(target=thread_fuc2)
t2.start()

canvas.pack()
root.mainloop()
