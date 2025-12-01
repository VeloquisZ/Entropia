"""
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

# make the data
np.random.seed(3)
x = 4 + np.random.normal(0, 2, 24)
y = 4 + np.random.normal(0, 2, len(x))
# size and color:
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))

# plot
fig, ax = plt.subplots()

ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()
"""


import turtle

config_tank = {1 : -200, 2 : 100}

# Screen setup
screen = turtle.Screen()
screen.setup(width=500, height=500)

def grids(x,y,linhas,colunas,size):
       pen = turtle.Turtle()
       pen.speed(0)
       pen.penup()
       #comeco da grade
       pen.goto(x,y)
       
       #loop com linhas
       for i in range(linhas):
              #loop com colunas
              for j in range(colunas):
                     #desenhando quadrdos
                     for _ in range(4):
                            pen.pendown()
                            pen.forward(size)
                            pen.right(90)
                            pen.penup()
                     #apos fazer um quadrado vai para a proxima posição
                     pen.forward(size)
              #mexe o pincel para a comeca a proxima linha
              pen.goto(x,y - (i  + 1) * size)
              
              
grids(-200,100,3,3,50)
grids(100,200, 5 , 5 , 50)
turtle.done()