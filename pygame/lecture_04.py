import time
import turtle
from turtle import Turtle
from random import randint

# set window
window = turtle.Screen()
window.title("Turtle race")
turtle.bgcolor("forestgreen")
turtle.color("white")
turtle.speed(0)
turtle.penup()
turtle.setpos(-140, 200)
turtle.write("TURTLE RACE", font=("Arial", 30, "bold"))
turtle.penup()

# dirt
turtle.setpos(-400, -180)
turtle.color("chocolate")
turtle.begin_fill()
turtle.pendown()
turtle.forward(800)
turtle.right(90)
turtle.forward(300)
turtle.right(90)
turtle.forward(800)
turtle.right(90)
turtle.forward(300)
turtle.end_fill()

# finish line
stamp_size = 20
square_size = 15
finish_line = 200

turtle.color("black")
turtle.shape("square")
turtle.shapesize(square_size / stamp_size)
turtle.penup()

for i in range(10):
    turtle.setpos(finish_line, (150 - (i * square_size * 2)))
    turtle.stamp()

for j in range(10):
    turtle.setpos(finish_line + square_size, ((150 - square_size) - (j * square_size * 2)))
    turtle.stamp()

turtle.hideturtle()

class turtles:
    def __init__(self, col, pos_y):
        self.col = col
        self.pos_y = pos_y

    def create(self):
        created = Turtle()
        created.speed(0)
        created.color(self.col)
        created.shape("turtle")
        created.penup()
        created.goto(-250, self.pos_y)
        created.pendown()
        

# create turtle racer
t1 = turtles("black", 100)    
t1.create()    
t1.move_turtle()
t2 = turtles("cyan", 50)    
t2.create()   
t3 = turtles("magenta", 0)    
t3.create()   
t4 = turtles("yellow", -50)    
t4.create()

time.sleep(1)
"""
# move
for i in range(145):
    t1.forward(randint(1, 5))
    t2.forward(randint(1, 5))
    t3.forward(randint(1, 5))
    t4.forward(randint(1, 5))
"""
turtle.exitonclick()
