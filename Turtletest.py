import turtle
import time

def prank(winner):

    skk = turtle.Turtle()
    
    for i in range(4):
        skk.forward(50)
        skk.right(90)
    
    turtle.write(winner , move=True,align='center',font=('Arial',15,'bold'))
    
    time.sleep(4)

    turtle.bye()
    return winner
