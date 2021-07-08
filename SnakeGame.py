"""
Created on Sun Oct  31 15:01:50 2020
@author: Viswanathan A
@Descirpion : Snake Game using Turle Module

Learning Objectives
1. Tutle Module for Playing a Snake Game
2. Set up a Player Class and instantiate it
3. sqlite integration to insert ans retrieve player data

"""

import turtle
import time
import random
from checkDBConn import DatabaseManager
from players import Players

# Functions Defenitions
def playGame(FN,LN):
#Create a New Database connection
    dbmngr.create_connection()

#Check if Table Exists , else Create Player Table
    dbmngr.create_PlayerTable()
#Create an Instance of a New Player to Begin Playing
    p1 = Players(FN,LN)   
#Check if the the Player exists on the Player Table
    if dbmngr.check_PlayerExists(p1):
        return p1
    else:
        dbmngr.insert_PlayerData(p1)        
        return p1

#Function to Check if the Snake encountered a Crash with the wall or self
def CheckCrash(p1):
    # Check if Snake Head hit the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        hideTurtle()
    else:# Check if Snake Head hit its own body
        for segment in segments:
            if segment.distance(head) < 20:
                hideTurtle()
                #ClearPen(0,highScore,resetVal='hit')
                break

#Function to Clear the Pen to Clear the Text Content and Update with New Text Content
def ClearPen(Score=0,HighScore=0,resetVal ='grow'):  
    if resetVal == 'resetGame':
        global score
        global highScore
        score = 0 
    elif resetVal == 'hit': 
        score = 0
    else:
        pass
    pen.clear()
    pen.write("Player Name:" +FN.upper()+" " +"Player Score : " +str(Score) +"     High Score : " +str(HighScore), align = "center", font = ("courier",10,"normal"))

#Function to Hide the Snake Body when a crash was dedected and Start from initial state
def hideTurtle():
    time.sleep(0.5)
    head.goto(0,0)
    head.direction = "stop"
    for segment in segments:
        segment.hideturtle()
    segments.clear()
    #print(score)
    if score > playerHighScore:
        #print(score)
        dbmngr.update_PlayerData(p1,score) 
    ClearPen(0,highScore,resetVal='hit')  
    
#Close the Game Window when the Escape Key is Pressed
def close_game():
    turtle.bye()

#Reset the Game When the 'R' key is Pressed
def reset_game():
    global highScore
    global playerHighScore
    ClearPen(HighScore=highScore,resetVal='resetGame')
    head.goto(0,0)
    head.direction = 'stop'
    for segment in segments:
        segment.hideturtle()
    segments.clear()
    highScore = dbmngr.get_HighScore()
    playerHighScore = dbmngr.get_HighScoreByPlayer(p1)

def go_up():
    if head.direction != "down":
        head.direction = 'up'

def go_down():
    if head.direction != "up":
        head.direction = 'down'

def go_right():
    if head.direction != "left":
        head.direction = 'right'

def go_left():
    if head.direction != "right":
        head.direction = 'left'

def move():
    if head.direction =='up':
        y = head.ycor()
        head.sety(y+20)
        
    if head.direction =='down':
        y = head.ycor()
        head.sety(y-20)
       
    if head.direction =='left':
        x = head.xcor()
        head.setx(x - 20)
        
    if head.direction =='right':
        x = head.xcor()
        head.setx(x + 20)   
        

#Variable Declarion and tutle Screen Set up 
dbname = "SnakeGameDB"
dbPath= 'c:/Users/sachi/Desktop/Python Code/Py_Project/SnakeGame/'+dbname+'.db'
dbmngr = DatabaseManager(dbPath)
stats = False
segments = []
score = 0
delay = 0.1

#Set up Turtle Screen to Play the Game
wn = turtle.Screen()
wn.title("My Snake Game")
wn.bgcolor('light gray')
wn.setup(width=600,height=600)
wn.tracer(0)

#Set up Pen to Display Text
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("red")
pen.penup()
pen.hideturtle()
pen.goto(0,280)

#Continue to get User Name until the User has Entered his First & Last Name Split by a Space
while stats is False:
    try:
         
        FN,LN = turtle.textinput("Enter Full Name separated by Space", "Name").split(' ')
        p1 = playGame(FN,LN)
        stats = True
        pen.clear()
    except:
        pen.write("Please Enter a Valid Player Name in First Name Last Name format" , align = "center", font = ("courier",10,"normal"))

#Get the Player and Score Details from the Player Table
highScore = dbmngr.get_HighScore()
playerHighScore = dbmngr.get_HighScoreByPlayer(p1)


#Define the Snakes's Head and set its Starting Position
head = turtle.Turtle()
head.speed()
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = 'stop'

#Define the Snake's Food and set its Starting Position
food = turtle.Turtle()
food.speed()
food.shapesize(stretch_wid=0.8, stretch_len=0.8)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

#Initiate Pen Value to Display Initial game Score
pen.write("Player Name:" +FN.upper()+" " +"Player Score: " +str(score) +"     High Score: " +str(highScore), align = "center", font = ("courier",10,"normal"))


#Set Keyboard Bindings
wn.listen()
wn.onkeypress(go_up,"Up")
wn.onkeypress(go_right,"Right")
wn.onkeypress(go_down,"Down")
wn.onkeypress(go_left,"Left")
wn.onkeypress(reset_game,"r")
wn.onkeypress(close_game,"Escape")

#Main Game Loop
while True:
    
    wn.update()
    # Check Snake made contact with food, If yes move to a Random spot on the Grid
    if head.distance(food) <20:
        x = random.randrange(-280,280,20)
        y = random.randrange(-280,280,20)
        food.goto(x,y) 
        
        # add a new segment to Snake Body
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        #Increase the Score
        score += 10
        if score > highScore:
            highScore = score
        ClearPen(score,highScore)

    # Grow  Tail
    for index in range(len(segments)-1,0,-1):
        x = segments[index -1].xcor()
        y = segments[index -1].ycor()
        segments[index].goto(x,y)

    if len(segments) >0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    #Keep Making Move
    move()
    #Check if the Snake Crashed to the wall or to itself
    CheckCrash(p1) 
    
    #increase Time Delay
    time.sleep(delay)
  
wn.mainloop()