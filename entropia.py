import random
import time
import turtle
import matplotlib.pyplot as plt
import numpy as np


size_tank = 3     #tamanho do tank
size_ambiente = 5   #tamanho do ambiente
n_movimentos = 500  #numero de passos de movimento na simulação
delay = 0.50        #atraso em segundos entre cada movimento

#configurações da tela
tamanho_grad = 60
espaco_entre_grads = 50 
tela_largura = (size_ambiente + size_tank) * tamanho_grad + espaco_entre_grads + 100
tela_altura = size_ambiente * tamanho_grad + 100


#largura dos componentes individuais
largura_ambiente = size_ambiente * tamanho_grad
largura_tank = size_tank * tamanho_grad

#soma tudo o que será desenhado horizontalmente
largura_total = largura_ambiente + espaco_entre_grads + largura_tank

#define onde começa o desenho do ambiente
inicio_x_ambiente = -largura_total / 2

#define onde começa o desenho do tank
inicio_x_tank = inicio_x_ambiente + largura_ambiente + espaco_entre_grads

#centralização vertical
inicio_y = -largura_ambiente / 2

def coordenadas_grads(matrix_id, linha, coluna):
    #mapeia coordenadas (id da matriz, linha, coluna) para coordenadas (x, y) da tela
    if matrix_id == 0:  # ambiente
        start_x = inicio_x_ambiente
    else:  #tank
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
                
        self.lista_atomos = np.array(posicao_inicial_tank, dtype=int) 

        #preenche o set de ocupação inicial
        for posicao in posicao_inicial_tank:
            self.posicoes_ocupadas.add(posicao)
    
    
    def movento_aleatorio_atomo(self):
    #    Escolhe um atomo aleatorio e tenta move ele,checando limites de linhas, colisao e a passagem.
        if self.lista_atomos.size == 0:
            return False

        #escolhe um átomo aleatório
        index = random.randrange(len(self.lista_atomos))
        
        # obtem a posição atual do array 
        id_matriz, indix_linha, index_coluna = self.lista_atomos[index]
        posicao_atual = (id_matriz, indix_linha, index_coluna)
        
        #escolhe uma direção aleatória: Cima, Baixo, Direita, Esquerda
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        direcao_linha, direcao_coluna = random.choice(directions)
        
        id_matriz_temporario = id_matriz
        nova_linha = indix_linha + direcao_linha
        nova_coluna = index_coluna + direcao_coluna
        
        #passagem entre grids
        #tank para ambiente quando vai para esquerda
        if id_matriz == 1 and indix_linha == 0 and index_coluna == 0 and direcao_coluna == -1:
            id_matriz_temporario = 0
            nova_linha = 0
            nova_coluna = size_ambiente - 1
            
        # retorno do ambiente para o tanque
        elif id_matriz == 0 and indix_linha == 0 and index_coluna == size_ambiente - 1 and direcao_coluna == 1:
            id_matriz_temporario = 1
            nova_linha = 0
            nova_coluna = 0
            
        #logica de movimento normal/limite
        else:
            #checagem de limite (fronteira)
            size = self.sizes[id_matriz]
            is_in_bounds = (0 <= nova_linha < size and 0 <= nova_coluna < size)
            
            if not is_in_bounds:
                return False
        
        #posição de destino final (pode ser na mesma matriz ou na outra)
        posicao_final = (id_matriz_temporario, nova_linha, nova_coluna)
        
        #checagem de Colisão (Se o bloco de destino está ocupado)
        checar_colicao = posicao_final in self.posicoes_ocupadas
        
        if checar_colicao:
            return False

        #movimento bem-sucedido
        self.posicoes_ocupadas.remove(posicao_atual)
        self.posicoes_ocupadas.add(posicao_final)
        
        #atualiza a posição no array NumPy
        self.lista_atomos[index] = [id_matriz_temporario, nova_linha, nova_coluna]
            
        return True

#criar um turtle separado para desenhar as grades
grade_turtle = turtle.Turtle()
grade_turtle.hideturtle()

def draw_atomos(num_atoms):
    #cria um objeto Turtle separado para cada atomo
    atomos = []
    for _ in range(num_atoms):
        a = turtle.Turtle()  #cria novo objeto para cada átomo
        a.shape("circle")
        a.turtlesize(tamanho_grad / 30) 
        a.penup()
        a.color("blue")
        a.hideturtle()  #esconde até ser posicionado
        atomos.append(a)
    return atomos

def draw_grid(turtle_obj, inicio_x, inicio_y, size, color):
    #desenha as linhas de uma matriz
    turtle_obj.speed(0)
    turtle_obj.penup()
    turtle_obj.pensize(2)
    turtle_obj.color(color)
    
    end_coord_x = inicio_x + size * tamanho_grad
    end_coord_y = inicio_y + size * tamanho_grad
    
    for i in range(size + 1):
        #linhas Verticais
        x = inicio_x + i * tamanho_grad
        turtle_obj.goto(x, inicio_y)
        turtle_obj.pendown()
        turtle_obj.goto(x, end_coord_y)
        turtle_obj.penup()
        
        #linhas Horizontais
        y = inicio_y + i * tamanho_grad
        turtle_obj.goto(inicio_x, y)
        turtle_obj.pendown()
        turtle_obj.goto(end_coord_x, y)
        turtle_obj.penup()

def att_atomo_tela(screen, atomos_turtles, atoms_array):
    #atualiza a posição dos atomos na tela e o status
    
    #mostra todos os átomos
    for turtle_obj in atomos_turtles:
        turtle_obj.showturtle()
    
    #atualiza a posição de cada Turtle usando o array NumPy
    for i in range(len(atoms_array)):
        id_mat, linha, coluna = atoms_array[i]
        x, y = coordenadas_grads(id_mat, linha, coluna)
        atomos_turtles[i].goto(x, y)
    
    screen.update()

#configurações da tela
def config_tela():
    #configura a tela do Turtle e desenha as duas matrizes
    screen = turtle.Screen()
    screen.setup(width=tela_largura, height=tela_altura)
    screen.title("Entropia")
    screen.tracer(0) 

    #desenha matriz ambiente
    draw_grid(grade_turtle, inicio_x_ambiente, inicio_y, size_ambiente, "black")
    
    #desenha matriz tank
    draw_grid(grade_turtle, inicio_x_tank, inicio_y, size_tank, "black")

    #indica a passagem tank para o ambiente
    grade_turtle.penup()
    grade_turtle.color("gray")
    grade_turtle.pensize(3)
    
    #posição de saida
    x1, y1 = coordenadas_grads(1, 0, 0)
    #posição de entrada
    x2, y2 = coordenadas_grads(0, 0, size_ambiente - 1)
    
    #desenha um marcador de ligação 
    grade_turtle.goto(x1, y1)
    grade_turtle.dot(10, "gray")
    grade_turtle.goto(x2, y2)
    grade_turtle.dot(10, "gray")
    return screen

def roda_entropia():
    #executa a simulação principal e a animação
    
    screen = config_tela()
    
    entro = Entropia()
    atomos_turtles = draw_atomos(len(entro.lista_atomos))
    for _ in range(n_movimentos):
        
        #logica de movimento
        entro.movento_aleatorio_atomo()
        
        #atualização gráfica
        att_atomo_tela(screen, atomos_turtles, entro.lista_atomos)
        
        time.sleep(delay)
        
        
    turtle.done()

if __name__ == "__main__":
    roda_entropia()