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
import random
import time
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
                
        self.lista_atomos = np.array(posicao_inicial_tank, dtype=int) 

        # Preenche o set de ocupação inicial
        for posicao in posicao_inicial_tank:
            self.posicoes_ocupadas.add(posicao)
    
    
    def movento_aleatorio_atomo(self):
        """
        Escolhe um atomo aleatorio e tenta move ele,
        checando limites de linhas, colisão e a passagem.
        """
        if self.lista_atomos.size == 0:
            return False

        # 1. Escolhe um átomo aleatório (índice na matriz NumPy)
        index = random.randrange(len(self.lista_atomos))
        
        # Obtém a posição atual do array NumPy
        id_matriz, indix_linha, index_coluna = self.lista_atomos[index]
        posicao_atual = (id_matriz, indix_linha, index_coluna)
        
        # 2. Escolhe uma direção aleatória (dr, dc): Cima, Baixo, Direita, Esquerda
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        direcao_linha, direcao_coluna = random.choice(directions)
        
        id_matriz_temporario = id_matriz
        nova_linha = indix_linha + direcao_linha
        nova_coluna = index_coluna + direcao_coluna
        
        # --- logica de passagem ---
        # Regra: tank(1) (0, 0) -> ambiente(0) (0, 4) se o movimento for para a esquerda (direcao_coluna == -1)
        if id_matriz == 1 and indix_linha == 0 and index_coluna == 0 and direcao_coluna == -1:
            id_matriz_temporario = 0
            nova_linha = 0
            nova_coluna = size_ambiente - 1 # Posição (0, 4) na matriz 5x5 (0)
            
        elif id_matriz == 0 and indix_linha == 0 and index_coluna == size_ambiente - 1 and direcao_coluna == 1:
            id_matriz_temporario = 1
            nova_linha = 0
            nova_coluna = 0
            
        #logica de movimento normal/limite
        else:
            # 3. Checagem de limite (fronteira)
            size = self.sizes[id_matriz]
            #obtem tamanho da matriz atual
            is_in_bounds = (0 <= nova_linha < size and 0 <= nova_coluna < size)
            
            if not is_in_bounds:
                return False # movimento negado por limite de fronteira
        
        # Posição de destino final (pode ser na mesma matriz ou na outra)
        posicao_final = (id_matriz_temporario, nova_linha, nova_coluna)
        
        # 4. Checagem de Colisão (Se o bloco de destino está ocupado)
        checar_colicao = posicao_final in self.posicoes_ocupadas
        
        if checar_colicao:
            return False # movimento negado por colisão

        # movimento bem-sucedido
        
        #atualiza a variavel de ocupação
        self.posicoes_ocupadas.remove(posicao_atual)
        self.posicoes_ocupadas.add(posicao_final)
        
        #atualiza a posição no array NumPy
        self.lista_atomos[index] = [id_matriz_temporario, nova_linha, nova_coluna]
            
        return True


pen = turtle.Turtle()
pen.hideturtle()

def draw_atomos(num_atoms):
    """desenhas os átomos."""
    atomos = []
    for _ in range(num_atoms):
        pen.shape("circle")
        pen.turtlesize(tamanho_grad / 30) 
        pen.penup()
        atomos.append(pen)
    return atomos

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
        
def att_atomo_tela(screen, atomos_turtles, atoms_array, passo):
    """Atualiza a posição dos átomos na tela e o status."""
    
    # Atualiza a posição de cada Turtle usando o array NumPy
    for i in range(len(atoms_array)):
        id, linha, coluna = atoms_array[i]
        x, y = coordenadas_grads(id, linha, coluna)
        atomos_turtles[i].goto(x, y)
        
         
    # Atualiza o texto de status
    pen.clear()
        
   # Conta os átomos no Tanque (mid == 1) usando NumPy
    atomos_no_tanque = np.sum(atoms_array[:, 0] == 1)
    
    pen.write(
        
        f"Passo: {passo}/{n_movimentos} | Átomos no Tanque (3x3): {atomos_no_tanque}", 
        align="center", font=("Arial", 14, "bold")
    )
    
    screen.update()
#configurações da tela
def config_tela():
    """Configura a tela do Turtle e desenha as duas matrizes."""
    screen = turtle.Screen()
    screen.setup(width=tela_largura, height=tela_altura)
    screen.title("Entropia")
    screen.tracer(0) 

    # Desenha Matriz ambiente (Esquerda, 5x5)
    draw_grid(inicio_x_ambiente, inicio_y, size_ambiente)
    
    # Desenha Matriz tank (Direita, 3x3)
    draw_grid(inicio_x_tank, inicio_y, size_tank)

    # Indica a passagem tank(0,0) -> ambiente(0,4))
    pen.penup()
    pen.color("gray")
    pen.pensize(3)
    
    # Posição de Saída (tank 3x3, 0, 0)
    x1, y1 = coordenadas_grads(1, 0, 0)
    # Posição de Entrada (ambiente 5x5, 0, 4)
    x2, y2 = coordenadas_grads(0, 0, size_ambiente - 1)
    
    # Desenha um marcador de ligação 
    pen.goto(x1, y1)
    pen.dot(10, "gray")
    pen.goto(x2, y2)
    pen.dot(10, "gray")
    
    return screen, pen

def run_dual_grid_simulation_numpy():
    """Executa a simulação principal e a animação."""
    
    screen, _ = config_tela()
    
    entro = Entropia()
    atomos_turtles = draw_atomos(len(entro.lista_atomos))
    
    print(f"Iniciando simulação dual-matriz com NumPy: Tanque ({size_tank}x{size_tank}) e Ambiente ({size_ambiente}x{size_ambiente}).")
    
    for passo in range(n_movimentos):
        
        # Lógica de movimento
        entro.move_random_atom()
        
        # Atualização gráfica
        att_atomo_tela(screen, atomos_turtles, entro.lista_atomos, passo + 1)
        
        time.sleep(delay)
        
        # Condição de parada: Se o tanque (Matriz 3x3) esvaziar
        if np.sum(entro.lista_atomos[:, 0] == 1) == 0:
             break

    # Mensagem final
    pen.goto(0, 0)
    pen.color("darkgreen")
    pen.write(
        f"SIMULAÇÃO CONCLUÍDA após {passo + 1} passos.", 
        align="center", font=("Arial", 16, "bold")
    )
    screen.update()
    
    screen.mainloop()

if __name__ == "__main__":
    # ATENÇÃO: Descomente a linha abaixo para executar a animação em uma nova janela.
    run_dual_grid_simulation_numpy()

turtle.done()