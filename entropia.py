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


size_tank = 5     # tamanho do tank
size_ambiente = 7   # tamanho do ambiente
num_atom = 9       # Número total de átomos
n_movimentos = 500  # Número de passos de movimento na simulação
delay = 0.05        # Atraso em segundos entre cada movimento

#configurações da tela
tamanho_grad = 60
espaco_entre_grads = 50 
tela_largura = (size_ambiente + size_tank) * tamanho_grad + espaco_entre_grads + 100
tela_altura = size_ambiente * tamanho_grad + 100


# Largura dos componentes individuais
largura_ambiente = size_ambiente * tamanho_grad
largura_tank = size_tank * tamanho_grad

# Soma tudo o que será desenhado horizontalmente
largura_total = largura_ambiente + espaco_entre_grads + largura_tank

# Define onde começa o desenho do ambiente
inicio_x_ambiente = -largura_total / 2

# Define onde começa o desenho do tank
inicio_x_tank = inicio_x_ambiente + largura_ambiente + espaco_entre_grads

# Centralização vertical
inicio_y = -largura_ambiente / 2

def coordenadas_grads(matrix_id, linha, coluna):
    """Mapeia coordenadas (id da matriz, linha, coluna) para coordenadas (x, y) da tela."""
    if matrix_id == 0:  # Ambiente (5x5)
        start_x = inicio_x_ambiente
    else:  # Tanque (3x3)
        start_x = inicio_x_tank

    x = start_x + coluna * tamanho_grad + tamanho_grad / 2
    y = inicio_y + linha * tamanho_grad + tamanho_grad / 2
    return x, y

#classe que vai gerencia a logica
class Entropia():   
    
    def __init__(self):
        
        #id: 0 ambiente , 1 tank
        self.sizes = {0 : size_ambiente ,1 : size_tank}
        
        #espacos ocupados
        self.posicoes_ocupadas = set()
        
        posicao_inicial_tank = []
        
        for linha in range(size_tank):
            
            for coluna in range(size_tank):
                
                posicao_inicial_tank.append((1, linha, coluna))
                
                self.atoms_list = np.array(posicao_inicial_tank, dtype=int) 

        # Preenche o set de ocupação inicial
        for posicao in posicao_inicial_tank:
            self.posicoes_ocupadas.add(posicao)


pen = turtle.Turtle()
pen.hideturtle()

def draw_atomo():
    pass

def draw_grid(inicio_x, inicio_y, size):
    """Desenha as linhas de uma matriz."""
    pen.speed(0)
    pen.penup()
    pen.pensize(2)
    
    end_coord_x = inicio_x + size * tamanho_grad
    end_coord_y = inicio_y + size * tamanho_grad
    
    for i in range(size + 1):
        # Linhas Verticais
        x = inicio_x + i * tamanho_grad
        pen.goto(x, inicio_y)
        pen.pendown()
        pen.goto(x, end_coord_y)
        pen.penup()
        
        # Linhas Horizontais
        y = inicio_y + i * tamanho_grad
        pen.goto(inicio_x, y)
        pen.pendown()
        pen.goto(end_coord_x, y)
        pen.penup()

#configurações da tela
def config_tela():
    """Configura a tela do Turtle e desenha as duas matrizes."""
    screen = turtle.Screen()
    screen.setup(width=tela_largura, height=tela_altura)
    screen.title("Entropia")
    screen.tracer(0) 

    # Desenha Matriz Ambiente (Esquerda, 5x5)
    draw_grid(inicio_x_ambiente, inicio_y, size_ambiente)
    
    # Desenha Matriz Tanque (Direita, 3x3)
    draw_grid(inicio_x_tank, inicio_y, size_tank)

    # Indica a Ligação Especial (Motor: Tanque(0,0) -> Ambiente(0,4))
    pen.penup()
    pen.color("gray")
    pen.pensize(3)
    
    # Posição de Saída (Tanque 3x3, 0, 0)
    x1, y1 = coordenadas_grads(1, 0, 0)
    # Posição de Entrada (Ambiente 5x5, 0, 4)
    x2, y2 = coordenadas_grads(0, 0, size_ambiente - 1)
    
    # Desenha um marcador de ligação 
    pen.goto(x1, y1)
    pen.dot(10, "gray")
    pen.goto(x2, y2)
    pen.dot(10, "gray")
    
    return screen, pen


turtle.done()