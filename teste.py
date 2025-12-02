import random
import time
import turtle
import matplotlib.pyplot as plt
import numpy as np

# --- Configurações ---
size_tank = 3       # tamanho do tank
size_ambiente = 5   # tamanho do ambiente
n_movimentos = 900  # numero de passos de movimento na simulação
delay = 0.05        # atraso em segundos entre cada movimento

# Configurações da tela (Turtle)
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
    # Mapeia coordenadas (id da matriz, linha, coluna) para coordenadas (x, y) da tela
    if matrix_id == 0:  # ambiente
        start_x = inicio_x_ambiente
    else:  # tank
        start_x = inicio_x_tank

    x = start_x + coluna * tamanho_grad + tamanho_grad / 2
    y = inicio_y + linha * tamanho_grad + tamanho_grad / 2
    return x, y

# --- Classe Lógica ---
class Entropia():   
    
    def __init__(self):
        # id: 0 ambiente , 1 tank
        self.sizes = {0 : size_ambiente ,1 : size_tank}
        
        # espacos ocupados
        self.posicoes_ocupadas = set()
        
        posicao_inicial_tank = []
        
        for linha in range(size_tank):
            for coluna in range(size_tank):
                posicao_inicial_tank.append((1, linha, coluna))
                
        self.lista_atomos = np.array(posicao_inicial_tank, dtype=int) 

        # preenche o set de ocupação inicial
        for posicao in posicao_inicial_tank:
            self.posicoes_ocupadas.add(posicao)
    
    
    def movimento_aleatorio_atomo(self):
        # Escolhe um atomo aleatorio e tenta mover ele, checando limites, colisao e a passagem.
        if self.lista_atomos.size == 0:
            return False

        # escolhe um átomo aleatório
        index = random.randrange(len(self.lista_atomos))
        
        # obtem a posição atual do array 
        id_matriz, indix_linha, index_coluna = self.lista_atomos[index]
        posicao_atual = (id_matriz, indix_linha, index_coluna)
        
        # escolhe uma direção aleatória: Cima, Baixo, Direita, Esquerda
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        direcao_linha, direcao_coluna = random.choice(directions)
        
        id_matriz_temporario = id_matriz
        nova_linha = indix_linha + direcao_linha
        nova_coluna = index_coluna + direcao_coluna
        
        # Passagem entre grids
        # Tank para ambiente (quando vai para esquerda na porta)
        if id_matriz == 1 and indix_linha == 0 and index_coluna == 0 and direcao_coluna == -1:
            id_matriz_temporario = 0
            nova_linha = 0
            nova_coluna = size_ambiente - 1
            
        # Retorno do ambiente para o tanque (quando vai para direita na porta)
        elif id_matriz == 0 and indix_linha == 0 and index_coluna == size_ambiente - 1 and direcao_coluna == 1:
            id_matriz_temporario = 1
            nova_linha = 0
            nova_coluna = 0
            
        # Logica de movimento normal/limite
        else:
            # checagem de limite (fronteira)
            size = self.sizes[id_matriz]
            is_in_bounds = (0 <= nova_linha < size and 0 <= nova_coluna < size)
            
            if not is_in_bounds:
                return False
        
        # posição de destino final (pode ser na mesma matriz ou na outra)
        posicao_final = (id_matriz_temporario, nova_linha, nova_coluna)
        
        # Checagem de Colisão (Se o bloco de destino está ocupado)
        checar_colisao = posicao_final in self.posicoes_ocupadas
        
        if checar_colisao:
            return False

        # movimento bem-sucedido
        self.posicoes_ocupadas.remove(posicao_atual)
        self.posicoes_ocupadas.add(posicao_final)
        
        # atualiza a posição no array NumPy
        self.lista_atomos[index] = [id_matriz_temporario, nova_linha, nova_coluna]
            
        return True

    def simular_sem_animacao(self, n_movimentos):
        """Executa a simulação sem animação gráfica"""
        for _ in range(n_movimentos):
            self.movimento_aleatorio_atomo()
        return self.get_estatisticas()

    def get_estatisticas(self):
        """Retorna estatísticas sobre a distribuição dos átomos"""
        atomos_no_ambiente = 0
        atomos_no_tank = 0
        
        for atomo in self.lista_atomos:
            if atomo[0] == 0:  # ambiente
                atomos_no_ambiente += 1
            else:  # tank
                atomos_no_tank += 1
        
        total_atomos = len(self.lista_atomos)
        percentual_ambiente = (atomos_no_ambiente / total_atomos) * 100 if total_atomos > 0 else 0
        percentual_tank = (atomos_no_tank / total_atomos) * 100 if total_atomos > 0 else 0
        
        return {
            'atomos_no_ambiente': atomos_no_ambiente,
            'atomos_no_tank': atomos_no_tank,
            'total_atomos': total_atomos,
            'percentual_ambiente': percentual_ambiente,
            'percentual_tank': percentual_tank,
            'distribuicao': [atomos_no_ambiente, atomos_no_tank]
        }

# --- Funções Gráficas (Turtle) ---
grade_turtle = turtle.Turtle()
grade_turtle.hideturtle()

def draw_atomos(num_atoms):
    atomos = []
    for _ in range(num_atoms):
        a = turtle.Turtle()
        a.shape("circle")
        a.turtlesize(tamanho_grad / 30) 
        a.penup()
        a.color("blue")
        a.hideturtle()
        atomos.append(a)
    return atomos

def draw_grid(turtle_obj, inicio_x, inicio_y, size, color):
    turtle_obj.speed(0)
    turtle_obj.penup()
    turtle_obj.pensize(2)
    turtle_obj.color(color)
    
    end_coord_x = inicio_x + size * tamanho_grad
    end_coord_y = inicio_y + size * tamanho_grad
    
    for i in range(size + 1):
        # Linhas Verticais
        x = inicio_x + i * tamanho_grad
        turtle_obj.goto(x, inicio_y)
        turtle_obj.pendown()
        turtle_obj.goto(x, end_coord_y)
        turtle_obj.penup()
        
        # Linhas Horizontais
        y = inicio_y + i * tamanho_grad
        turtle_obj.goto(inicio_x, y)
        turtle_obj.pendown()
        turtle_obj.goto(end_coord_x, y)
        turtle_obj.penup()

def att_atomo_tela(screen, atomos_turtles, atoms_array):
    for turtle_obj in atomos_turtles:
        turtle_obj.showturtle()
    
    for i in range(len(atoms_array)):
        id_mat, linha, coluna = atoms_array[i]
        x, y = coordenadas_grads(id_mat, linha, coluna)
        atomos_turtles[i].goto(x, y)
    
    screen.update()

def config_tela():
    screen = turtle.Screen()
    screen.setup(width=tela_largura, height=tela_altura)
    screen.title("Entropia")
    screen.tracer(0) 

    draw_grid(grade_turtle, inicio_x_ambiente, inicio_y, size_ambiente, "black")
    draw_grid(grade_turtle, inicio_x_tank, inicio_y, size_tank, "black")

    # Indica a passagem tank para o ambiente
    grade_turtle.penup()
    grade_turtle.color("gray")
    grade_turtle.pensize(3)
    
    x1, y1 = coordenadas_grads(1, 0, 0)
    x2, y2 = coordenadas_grads(0, 0, size_ambiente - 1)
    
    grade_turtle.goto(x1, y1)
    grade_turtle.dot(10, "gray")
    grade_turtle.goto(x2, y2)
    grade_turtle.dot(10, "gray")
    return screen

def roda_entropia():
    # Executa a simulação principal e a animação
    screen = config_tela()
    
    entro = Entropia()
    atomos_turtles = draw_atomos(len(entro.lista_atomos))
    for _ in range(n_movimentos):
        entro.movimento_aleatorio_atomo()
        att_atomo_tela(screen, atomos_turtles, entro.lista_atomos)
        time.sleep(delay)
    
    turtle.done()

# --- Funções de Análise e Plotagem ---

def roda_multiplas_simulacoes(n_simulacoes=1000):
    """Roda múltiplas simulações e coleta dados estatísticos"""
    resultados = []
    
    print(f"Rodando {n_simulacoes} simulações...")
    
    for i in range(n_simulacoes):
        entro = Entropia()
        # Roda simulação sem animação
        estatisticas = entro.simular_sem_animacao(n_movimentos)
        resultados.append(estatisticas)
        
        if (i + 1) % 100 == 0:
            print(f"  Concluído: {i + 1}/{n_simulacoes}")
    
    print("Simulações concluídas!")
    return resultados

def plotar_resultados(resultados):
    """Cria gráfico de distribuição para o ambiente"""
    
    # Extrai dados do ambiente
    atomos_ambiente = [r['atomos_no_ambiente'] for r in resultados]
    
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Conta frequências para cada valor
    valores_unicos = sorted(set(atomos_ambiente))
    frequencias = [atomos_ambiente.count(valor) for valor in valores_unicos]
    
    # Cores
    cores = plt.cm.Blues(np.linspace(0.5, 0.9, len(valores_unicos)))
    
    # Barras
    barras = ax.bar(valores_unicos, frequencias, color=cores, edgecolor='black', alpha=0.8)
    
    ax.set_xlabel('Número de Átomos no Ambiente')
    ax.set_ylabel('Frequência')
    ax.set_title(f'Distribuição de Átomos no Ambiente\n({len(resultados)} simulações)', fontweight='bold')
    
    # Estatísticas
    media = np.mean(atomos_ambiente)
    ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')
    
    ax.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # --- MODO DE EXECUÇÃO ---
    # Se quiser ver a animação visual, descomente a linha abaixo:
    # roda_entropia()
    
    # Se quiser ver o gráfico estatístico (padrão):
    n_simulacoes = 1000  
    resultados = roda_multiplas_simulacoes(n_simulacoes)
    plotar_resultados(resultados)