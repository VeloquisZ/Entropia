import random
import time
import turtle
import matplotlib.pyplot as plt
import numpy as np


size_tank = 3     # tamanho do tank - CORRIGIDO: mudado de 5 para 3
size_ambiente = 5   # tamanho do ambiente - CORRIGIDO: mudado de 7 para 5
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
    if matrix_id == 0:  # Ambiente
        start_x = inicio_x_ambiente
    else:  # Tanque
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
        # CORREÇÃO: O comentário diz "campo inferior esquerdo", mas o código original usava superior
        # Mantendo a lógica original: Tanque(0,0) -> Ambiente(0,4) quando vai para esquerda
        if id_matriz == 1 and indix_linha == 0 and index_coluna == 0 and direcao_coluna == -1:
            id_matriz_temporario = 0
            nova_linha = 0
            nova_coluna = size_ambiente - 1
            
        # CORREÇÃO: Retorno do ambiente para o tanque
        elif id_matriz == 0 and indix_linha == 0 and index_coluna == size_ambiente - 1 and direcao_coluna == 1:
            id_matriz_temporario = 1
            nova_linha = 0
            nova_coluna = 0
            
        #logica de movimento normal/limite
        else:
            # 3. Checagem de limite (fronteira)
            size = self.sizes[id_matriz]
            is_in_bounds = (0 <= nova_linha < size and 0 <= nova_coluna < size)
            
            if not is_in_bounds:
                return False
        
        # Posição de destino final (pode ser na mesma matriz ou na outra)
        posicao_final = (id_matriz_temporario, nova_linha, nova_coluna)
        
        # 4. Checagem de Colisão (Se o bloco de destino está ocupado)
        checar_colicao = posicao_final in self.posicoes_ocupadas
        
        if checar_colicao:
            return False

        # movimento bem-sucedido
        self.posicoes_ocupadas.remove(posicao_atual)
        self.posicoes_ocupadas.add(posicao_final)
        
        #atualiza a posição no array NumPy
        self.lista_atomos[index] = [id_matriz_temporario, nova_linha, nova_coluna]
            
        return True

# Criar um turtle separado para desenhar as grades
grade_turtle = turtle.Turtle()
grade_turtle.hideturtle()

def draw_atomos(num_atoms):
    """CORREÇÃO: Cria um objeto Turtle separado para CADA átomo."""
    atomos = []
    for _ in range(num_atoms):
        a = turtle.Turtle()  # CORREÇÃO: Cria NOVO objeto para cada átomo
        a.shape("circle")
        a.color("orange")  # CORREÇÃO: Adiciona cor
        a.turtlesize(tamanho_grad / 30) 
        a.penup()
        a.hideturtle()  # Esconde até ser posicionado
        atomos.append(a)
    return atomos

def draw_grid(turtle_obj, inicio_x, inicio_y, size, color):
    """Desenha as linhas de uma matriz."""
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
    """Atualiza a posição dos átomos na tela e o status."""
    
    # Mostra todos os átomos
    for turtle_obj in atomos_turtles:
        turtle_obj.showturtle()
    
    # Atualiza a posição de cada Turtle usando o array NumPy
    for i in range(len(atoms_array)):
        id_mat, linha, coluna = atoms_array[i]
        x, y = coordenadas_grads(id_mat, linha, coluna)
        atomos_turtles[i].goto(x, y)
    
    screen.update()

#configurações da tela
def config_tela():
    """Configura a tela do Turtle e desenha as duas matrizes."""
    screen = turtle.Screen()
    screen.setup(width=tela_largura, height=tela_altura)
    screen.title("Entropia - Simulação de Átomos")
    screen.tracer(0) 

    # Desenha Matriz ambiente (Esquerda, 5x5) - CORREÇÃO: Adiciona cor
    draw_grid(grade_turtle, inicio_x_ambiente, inicio_y, size_ambiente, "blue")
    
    # Desenha Matriz tank (Direita, 3x3) - CORREÇÃO: Adiciona cor
    draw_grid(grade_turtle, inicio_x_tank, inicio_y, size_tank, "red")

    # Indica a passagem tank(0,0) -> ambiente(0,4))
    grade_turtle.penup()
    grade_turtle.color("gray")
    grade_turtle.pensize(3)
    
    # Posição de Saída (tank 3x3, 0, 0)
    x1, y1 = coordenadas_grads(1, 0, 0)
    # Posição de Entrada (ambiente 5x5, 0, 4)
    x2, y2 = coordenadas_grads(0, 0, size_ambiente - 1)
    
    # Desenha um marcador de ligação 
    grade_turtle.goto(x1, y1)
    grade_turtle.dot(10, "gray")
    grade_turtle.goto(x2, y2)
    grade_turtle.dot(10, "gray")
    return screen

# Funções para gráficos matplotlib
def criar_graficos():
    """Cria figuras para os gráficos matplotlib."""
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    
    # Gráfico 1: Distribuição de átomos ao longo do tempo
    axs[0, 0].set_title('Distribuição de Átomos')
    axs[0, 0].set_xlabel('Passos')
    axs[0, 0].set_ylabel('Número de Átomos')
    axs[0, 0].set_ylim(0, num_atom)
    axs[0, 0].grid(True, alpha=0.3)
    
    # Gráfico 2: Entropia (medida de desordem)
    axs[0, 1].set_title('Entropia do Sistema')
    axs[0, 1].set_xlabel('Passos')
    axs[0, 1].set_ylabel('Entropia')
    axs[0, 1].grid(True, alpha=0.3)
    
    # Gráfico 3: Taxa de Movimentação
    axs[1, 0].set_title('Taxa de Movimentação')
    axs[1, 0].set_xlabel('Passos')
    axs[1, 0].set_ylabel('Movimentos Bem Sucedidos')
    axs[1, 0].grid(True, alpha=0.3)
    
    # Gráfico 4: Histograma de posições finais
    axs[1, 1].set_title('Distribuição Final')
    axs[1, 1].set_xlabel('Região')
    axs[1, 1].set_ylabel('Número de Átomos')
    axs[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig, axs

def atualizar_graficos(axs, passo, atomos_no_tanque, movimentos_bem_sucedidos, 
                       historico_tanque, historico_ambiente, historico_entropia):
    """Atualiza os gráficos com novos dados."""
    
    # Limpa e atualiza cada gráfico
    # Gráfico 1: Distribuição
    axs[0, 0].clear()
    axs[0, 0].set_title('Distribuição de Átomos')
    axs[0, 0].set_xlabel('Passos')
    axs[0, 0].set_ylabel('Número de Átomos')
    axs[0, 0].set_ylim(0, num_atom)
    axs[0, 0].grid(True, alpha=0.3)
    
    if len(historico_tanque) > 0:
        passos = list(range(1, len(historico_tanque) + 1))
        axs[0, 0].plot(passos, historico_tanque, 'b-', label='Tanque', linewidth=2)
        axs[0, 0].plot(passos, historico_ambiente, 'r-', label='Ambiente', linewidth=2)
        axs[0, 0].axhline(y=num_atom/2, color='gray', linestyle='--', alpha=0.5, label='Equilíbrio')
        axs[0, 0].legend()
    
    # Gráfico 2: Entropia
    axs[0, 1].clear()
    axs[0, 1].set_title('Entropia do Sistema')
    axs[0, 1].set_xlabel('Passos')
    axs[0, 1].set_ylabel('Entropia')
    axs[0, 1].grid(True, alpha=0.3)
    
    if len(historico_entropia) > 0:
        passos = list(range(1, len(historico_entropia) + 1))
        axs[0, 1].plot(passos, historico_entropia, 'g-', linewidth=2)
        axs[0, 1].fill_between(passos, 0, historico_entropia, alpha=0.3, color='green')
    
    # Gráfico 3: Taxa de Movimentação
    axs[1, 0].clear()
    axs[1, 0].set_title('Taxa de Movimentação')
    axs[1, 0].set_xlabel('Passos')
    axs[1, 0].set_ylabel('Movimentos Bem Sucedidos')
    axs[1, 0].grid(True, alpha=0.3)
    
    if len(movimentos_bem_sucedidos) > 0:
        # Calcula média móvel
        window_size = min(20, len(movimentos_bem_sucedidos))
        mov_media = np.convolve(movimentos_bem_sucedidos, np.ones(window_size)/window_size, mode='valid')
        passos_mov = list(range(window_size, len(movimentos_bem_sucedidos) + 1))
        
        axs[1, 0].bar(range(1, len(movimentos_bem_sucedidos) + 1), 
                      movimentos_bem_sucedidos, alpha=0.5, color='orange')
        axs[1, 0].plot(passos_mov, mov_media, 'r-', linewidth=2, label='Média Móvel')
        axs[1, 0].legend()
    
    # Gráfico 4: Histograma de posições atuais
    axs[1, 1].clear()
    axs[1, 1].set_title(f'Distribuição Atual (Passo {passo})')
    axs[1, 1].set_xlabel('Região')
    axs[1, 1].set_ylabel('Número de Átomos')
    axs[1, 1].grid(True, alpha=0.3)
    
    # Dados para o histograma
    categorias = ['Tanque', 'Ambiente']
    valores = [atomos_no_tanque, num_atom - atomos_no_tanque]
    cores = ['blue', 'red']
    
    axs[1, 1].bar(categorias, valores, color=cores, alpha=0.7)
    axs[1, 1].axhline(y=num_atom/2, color='gray', linestyle='--', alpha=0.5)
    
    # Adiciona valores nas barras
    for i, v in enumerate(valores):
        axs[1, 1].text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.pause(0.001)  # Pequena pausa para atualizar o gráfico

def calcular_entropia(atomos_no_tanque, atomos_no_ambiente):
    """Calcula a entropia do sistema usando a fórmula de Boltzmann."""
    total = atomos_no_tanque + atomos_no_ambiente
    
    if total == 0:
        return 0
    
    # Calcula as probabilidades
    p_tanque = atomos_no_tanque / total if atomos_no_tanque > 0 else 0
    p_ambiente = atomos_no_ambiente / total if atomos_no_ambiente > 0 else 0
    
    # Calcula entropia (S = -k * Σ p_i * ln(p_i))
    # Ignoramos k (constante de Boltzmann) pois estamos interessados na forma relativa
    entropia = 0
    if p_tanque > 0:
        entropia -= p_tanque * np.log(p_tanque)
    if p_ambiente > 0:
        entropia -= p_ambiente * np.log(p_ambiente)
    
    return entropia

def run_dual_grid_simulation_numpy():
    """Executa a simulação principal e a animação."""
    
    screen = config_tela()
    
    entro = Entropia()
    atomos_turtles = draw_atomos(len(entro.lista_atomos))
    
    # Cria um turtle separado para o texto de status
    status_turtle = turtle.Turtle()
    status_turtle.penup()
    status_turtle.hideturtle()
    status_turtle.goto(0, inicio_y + size_ambiente * tamanho_grad / 2 + 50)
    
    # Configura matplotlib para modo interativo
    plt.ion()
    
    # Cria gráficos
    fig, axs = criar_graficos()
    
    # Listas para armazenar histórico
    historico_tanque = []
    historico_ambiente = []
    historico_entropia = []
    movimentos_bem_sucedidos = []
    
    print(f"Iniciando simulação: Tanque ({size_tank}x{size_tank}) e Ambiente ({size_ambiente}x{size_ambiente}).")
    print(f"Transição especial: Tanque(0,0) <-> Ambiente(0,{size_ambiente-1})")
    
    for passo in range(n_movimentos):
        
        # Lógica de movimento
        movimento_sucesso = entro.movento_aleatorio_atomo()
        movimentos_bem_sucedidos.append(1 if movimento_sucesso else 0)
        
        # Atualização gráfica do turtle
        att_atomo_tela(screen, atomos_turtles, entro.lista_atomos)
        
        # Calcula estatísticas atuais
        atomos_no_tanque = np.sum(entro.lista_atomos[:, 0] == 1)
        atomos_no_ambiente = num_atom - atomos_no_tanque
        
        # Atualiza histórico
        historico_tanque.append(atomos_no_tanque)
        historico_ambiente.append(atomos_no_ambiente)
        
        # Calcula e armazena entropia
        entropia_atual = calcular_entropia(atomos_no_tanque, atomos_no_ambiente)
        historico_entropia.append(entropia_atual)
        
        # Atualiza gráficos matplotlib a cada 10 passos (para performance)
        if passo % 10 == 0 or passo == n_movimentos - 1:
            atualizar_graficos(axs, passo + 1, atomos_no_tanque, 
                              movimentos_bem_sucedidos, historico_tanque, 
                              historico_ambiente, historico_entropia)
        
        # Atualiza texto de status no turtle
        status_turtle.clear()
        status_turtle.write(
            f"Passo: {passo+1}/{n_movimentos} | Tanque: {atomos_no_tanque} | Ambiente: {atomos_no_ambiente} | Entropia: {entropia_atual:.3f}",
            align="center", font=("Arial", 12, "bold")
        )
        
        time.sleep(delay)
        
        # Condição de parada: Se o tanque (Matriz 3x3) esvaziar
        if atomos_no_tanque == 0:
            print(f"Tanque vazio após {passo + 1} passos!")
            break
    
    # Finaliza a simulação
    print(f"\nSimulação concluída!")
    print(f"Distribuição final: Tanque={atomos_no_tanque}, Ambiente={atomos_no_ambiente}")
    print(f"Entropia final: {entropia_atual:.3f}")
    print(f"Taxa média de movimentação: {np.mean(movimentos_bem_sucedidos):.2%}")
    
    # Mantém os gráficos abertos
    plt.ioff()
    
    # Cria gráfico final resumo
    fig_final, axs_final = plt.subplots(1, 3, figsize=(15, 5))
    
    # Gráfico 1: Distribuição completa
    passos = list(range(1, len(historico_tanque) + 1))
    axs_final[0].plot(passos, historico_tanque, 'b-', label='Tanque', linewidth=2)
    axs_final[0].plot(passos, historico_ambiente, 'r-', label='Ambiente', linewidth=2)
    axs_final[0].axhline(y=num_atom/2, color='gray', linestyle='--', alpha=0.5, label='Equilíbrio')
    axs_final[0].set_title('Distribuição de Átomos')
    axs_final[0].set_xlabel('Passos')
    axs_final[0].set_ylabel('Número de Átomos')
    axs_final[0].legend()
    axs_final[0].grid(True, alpha=0.3)
    
    # Gráfico 2: Entropia
    axs_final[1].plot(passos, historico_entropia, 'g-', linewidth=2)
    axs_final[1].fill_between(passos, 0, historico_entropia, alpha=0.3, color='green')
    axs_final[1].set_title('Evolução da Entropia')
    axs_final[1].set_xlabel('Passos')
    axs_final[1].set_ylabel('Entropia')
    axs_final[1].grid(True, alpha=0.3)
    
    # Gráfico 3: Distribuição final
    categorias = ['Tanque', 'Ambiente']
    valores = [atomos_no_tanque, atomos_no_ambiente]
    cores = ['blue', 'red']
    axs_final[2].bar(categorias, valores, color=cores, alpha=0.7)
    axs_final[2].set_title(f'Distribuição Final (Passo {len(passos)})')
    axs_final[2].set_xlabel('Região')
    axs_final[2].set_ylabel('Número de Átomos')
    axs_final[2].grid(True, alpha=0.3)
    
    # Adiciona valores nas barras
    for i, v in enumerate(valores):
        axs_final[2].text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Salva os gráficos
    fig.savefig('simulacao_graficos_detalhados.png', dpi=150, bbox_inches='tight')
    fig_final.savefig('simulacao_resumo_final.png', dpi=150, bbox_inches='tight')
    
    print("\nGráficos salvos como 'simulacao_graficos_detalhados.png' e 'simulacao_resumo_final.png'")
    
    plt.show()
    turtle.done()

if __name__ == "__main__":
    run_dual_grid_simulation_numpy()