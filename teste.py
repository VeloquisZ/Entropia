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

g = [1,2,3,6,5]
g = [-100,-70,-40,-10,20]

def desenho_atomos(corde_x,corde_y):
       
      todos_atomos = []
      for eixo_x in corde_x:  # Iterar diretamente pelos valores da lista
        atomo = turtle.Turtle(shape="circle")
        atomo.penup()
        atomo.goto(x=eixo_x, y=corde_y)  # Usar o valor diretamente, não como índice
        todos_atomos.append(atomo)

       

desenho_atomos(g,100)

turtle.mainloop()
