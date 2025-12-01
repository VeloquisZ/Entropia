#grade de 3x3 para armazenar os atomos 
#atomos se movem para esquerda,direita,cima,baixo se nao houver nada bloqueando o caminho 
#se o caminho estiver bloqueado por outro atomo ou uma parede, nada acontence e a simulação continua para a proxima etapa
#onde outro atomo é selecionado para se mover
#um atomo que se move para a esquerda no campo inferior esquerdo do tanque, ira atravessar o motor e entrar no ambiente 
#impulsionando o carro a frente. Um atomo que se move para a direita no campo inferior direito da grade que representa o seu ambiente
#ira se mover atraves do motor para o tanque e empurrar o carro para tras   
#
#
#
#
import turtle
import matplotlib.pyplot as plt
import numpy as np


# configurações da tela
screen = turtle.Screen()
screen.setup(width=500, height=500)
screen.title("Entropia")

class Atomo():#classe atomo que vai gerencia a localização deles no eixo x e y
    def __init__(self,x,y):
        self.x = x
        self.y = y


def draw_atomo():
    pass




#função que cria grades
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
              
              

#grids(x = -200, y = 100, colunas = 3, linhas = 3, size = 50)
#grids(x = 100, y = 200, colunas = 5, linhas = 5, size = 50)

turtle.done()