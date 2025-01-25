import tkinter as tk
from PIL import ImageTk, Image
import random
import os
from pygame import mixer
import win32com.client as wincom

# TEXT TO SPEECH
def speak_1(a):
        speak = wincom.Dispatch("SAPI.SpVoice")
        speak.speak(a)

# BACKGROUND MUSIC SETUP
mixer.init()
mixer.music.load("Images/music.mp3")
mixer.music.play()

player_1 = input("Enter the name of Player-1: ")
p1 = player_1
player_2 = input("Enter the name of Player-2: ")
p2 = player_2

def StartGame():
    global img
    global but1, but2
    
    # PLAYER_1
    but1.place(x=1250, y=400)

    # PLAYER_2
    but2.place(x=1250, y=550)

    # DICE
    img = Image.open("Images/d1.WEBP")
    img = img.resize((75,75))
    img = ImageTk.PhotoImage(img)
    dice = tk.Button(root, image=img, height=80, width=80)
    dice.place(x=1325, y=180)

    # EXIT BUTTON
    exitBut = tk.Button(root, text="Click Here To End Term", height=3, width=20, fg="red", bg="yellow", font=("Cursive",14,"bold"), activebackground="red", command=root.destroy)
    exitBut.place(x=1250, y=20)

def reset_coins():
    global player_1, player_2
    global pos1, pos2
    
    player_1.place(x=15, y=720)
    player_2.place(x=65, y=720)

    pos1 = 0
    pos2 = 0

def load_dice_images():
    global dice_img
    names = ["a.PNG","b.PNG","c.PNG","d.PNG","e.PNG","f.PNG"]
    for name in names:
        img = Image.open("Images/"+name)
        img = img.resize((75,75))
        img = ImageTk.PhotoImage(img)
        dice_img.append(img)

def check_ladder(turn):
    global pos1, pos2
    global ladder
    f = 0
    if turn==1: 
        if pos1 in ladder:
            mixer.music.pause()
            speak_1("Ladder at "+str(pos1)+" going up to ")
            pos1 = ladder[pos1]
            speak_1(str(pos1))
            mixer.music.unpause()
            f=1
    else:
        if(pos2 in ladder):
            mixer.music.pause()
            speak_1("ladder at "+str(pos1)+" going up to ")
            pos2 = ladder[pos2]
            speak_1(str(pos1))
            mixer.music.unpause()
            f=1
    return f

def check_snake(turn):
    global pos1, pos2
    
    if turn==1:
        if pos1 in snake:
            mixer.music.pause()
            speak_1("snake at "+str(pos1)+" going down to ")
            pos1 = snake[pos1]
            speak_1(str(pos1))
            mixer.music.unpause()
    else:
        if(pos2 in snake):
            mixer.music.pause()
            speak_1("snake at "+str(pos1)+" going down to ")
            pos2 = snake[pos2]
            speak_1(str(pos2))
            mixer.music.unpause()

def roll_dice():
    global dice_img
    global turn
    global pos1, pos2
    global but1, but2
    
    r = random.choice([1,2,3,4,5,6])
    dice = tk.Button(root, image=dice_img[r-1], height=80, width=80)
    dice.place(x=1325, y=180)

    if(turn==1):
        #speak_1("player_1 chance")
        if(pos1+r)<=100:
            pos1 += r
        check_ladder(turn)
        check_snake(turn)
        move_coin(turn, pos1)
        if r!=1:
            turn = 2
            but1.config(state = "disabled")
            but2.config(state = "normal")
    else:
        #speak_1("player_2 chance")
        if(pos2+r)<=100:
            pos2 += r
        check_ladder(turn) 
        check_snake(turn)
        move_coin(turn, pos2)
        if r!=1:
            turn = 1
            but1.config(state = "normal")
            but2.config(state = "disabled")
    win = is_winner()
    if(win):
        but1.config(state = "disabled")
        but2.config(state = "disabled")

def is_winner():
    global pos1, pos2
    global player_1, player_2
    if pos1==100:
        msg = "Player - 1 is the Winner"
        Lab = tk.Label(root, text=msg, height=2, width=20, bg="red", font=("Cursive",30,"bold"))
        Lab.place(x=300, y=300)
        reset_coins()
        mixer.music.stop()
        speak_1("Congratulation"+p1+"you won the match")
        speak_1("Thanku for visiting this game i hope you injoy it")
        mixer.music.load("Images/m2.mp3")
        mixer.music.play()
        return 1
    elif pos2==100:
        msg = "Player - 2 is the Winner"
        Lab = tk.Label(root, text=msg, height=2, width=20, bg="red", font=("Cursive",30,"bold"))
        Lab.place(x=300, y=300)
        reset_coins()
        speak_1("Congratulation"+p2+"you won the match")
        speak_1("Thanku for visiting this game i hope you injoy it")
        mixer.music.load("Images/m2.mp3")
        mixer.music.play()
        return 1

def move_coin(turn, r):
    global player_1, player_2
    global index

    if(turn==1):
        player_1.place(x=index[r][0], y=index[r][1])
    else:
        player_2.place(x=index[r][0], y=index[r][1])

def get_index():
    global player_1, player_2
    # x->155
    # y->91
    num = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, \
           81, 82, 83, 84, 85, 86, 87, 88, 89, 90, \
           80, 79, 78, 77, 76, 75, 74, 73, 72, 71,\
           61, 62, 63, 64, 65, 66, 67, 68, 69, 70, \
           60, 59, 58, 57, 56, 55, 54, 53, 52, 51, \
           41, 42, 43, 44, 45, 46, 47, 48, 49, 50, \
           40, 39, 38, 37, 36, 35, 34, 33, 32, 31, \
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, \
           20, 19, 18, 17, 16, 15, 14, 13, 12, 11, \
           1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    row = 20
    i=0
    for x in range(1,11):
        col = 50
        for y in range(1,11):
            index[num[i]]=(col,row)
            col += 107
            i += 1
        row += 69
    #print(index)


# STORING X & Y CO-ORDINATES OF THE GIVEN NUM
index = {}

# STORING DICE IMAGES
dice_img = []

# INITIAL POSITION OF PLAYERS
pos1 = None
pos2 = None

# LADDER BOTTOM TO TOP
ladder = {2:23, 8:12, 17:93, 29:54, 32:51, 39:80, 70:89, 75:96}

# SNAKE TOP TO BOTTOM
snake = {31:14, 41:20, 58:37, 67:49, 84:62, 92:76, 99:4}

# SNAKE BOARD DECLARATION
root = tk.Tk()
root.geometry("1200x800")
root.title("Snake And Ladder")
root.config(bg="black")

# ADDING LOGO
icon = ImageTk.PhotoImage(file = "Images/icon_2.png")
root.iconphoto(False, icon)

snake_fr = tk.Frame(root, width=1200, height=800) 
snake_fr.place(x=0, y=0)

#SETTING UP BOARD CONFIGURATION
bod = ImageTk.PhotoImage(Image.open("Images/b1.PNG"))
lbl_bod = tk.Label(snake_fr, image = bod, padx=0, pady=0, borderwidth=0, highlightthickness=0)
lbl_bod.place(x = 0, y = 0)


# BUTTON SETTING UP
but1 = tk.Button(root,
                 text=player_1,
                 cursor="hand1",
                 height=3,
                 width=20,
                 fg="white",
                 bg="blue",
                 highlightbackground="white",
                 highlightcolor="yellow", 
                 highlightthickness=5,
                 font=("Cursive",14,"bold"),
                 activebackground="cyan",
                 command = roll_dice)

but2 = tk.Button(root,
                 text=player_2,
                 cursor="hand1",
                 height=3,
                 width=20,
                 fg="white",
                 bg="red",
                 highlightbackground="white",
                 highlightcolor="green", 
                 highlightthickness=5,
                 font=("Cursive",14,"bold"),
                 activebackground="yellow",
                 command = roll_dice)

# PLAYER_1 TOKENS
player_1 = tk.Canvas(root, width=40, height=40)
player_1.create_oval(10,10,40,40,fill="blue")

# PLAYER_2 TOKENS
player_2 = tk.Canvas(root, width=40, height=40)
player_2.create_oval(10,10,40,40,fill="red")

reset_coins()
get_index()
turn = 1
load_dice_images()
StartGame()

root.mainloop()
