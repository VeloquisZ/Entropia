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

class Atomo():#classe atomo que vai gerencia a localização deles no eixo x e y
    def __init__(self,x,y):
        self.x = x
        self.y = y


def draw_atomo():
    pass
