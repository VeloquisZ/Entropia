import turtle
import random
import time
import numpy as np

# --- CONFIGURAÇÕES GLOBAIS ---
SIZE_TANQUE = 5     # Matriz da Direita (Tanque)
SIZE_AMBIENTE = 7   # Matriz da Esquerda (Ambiente)
NUM_ATOMS = 9       # Número total de átomos
N_MOVIMENTOS = 500  # Número de passos de movimento na simulação
DELAY = 0.05        # Atraso em segundos entre cada movimento

# --- CONFIGURAÇÕES GRÁFICAS DO TURTLE ---
CELL_SIZE = 60
GAP = 50 
SCREEN_WIDTH = (SIZE_AMBIENTE + SIZE_TANQUE) * CELL_SIZE + GAP + 100
SCREEN_HEIGHT = SIZE_AMBIENTE * CELL_SIZE + 100

# Centraliza o grid
TOTAL_WIDTH = (SIZE_AMBIENTE * CELL_SIZE) + GAP + (SIZE_TANQUE * CELL_SIZE)
START_X_AMBIENTE = - TOTAL_WIDTH / 2
START_X_TANQUE = START_X_AMBIENTE + (SIZE_AMBIENTE * CELL_SIZE) + GAP
START_Y = - (SIZE_AMBIENTE / 2) * CELL_SIZE # Linha de base Y

def map_coords_to_screen(matrix_id, row, col):
    """Mapeia coordenadas (id da matriz, linha, coluna) para coordenadas (x, y) da tela."""
    if matrix_id == 0:  # Ambiente (5x5)
        start_x = START_X_AMBIENTE
    else:  # Tanque (3x3)
        start_x = START_X_TANQUE

    x = start_x + col * CELL_SIZE + CELL_SIZE / 2
    y = START_Y + row * CELL_SIZE + CELL_SIZE / 2
    return x, y

class DualGridSimulator:
    """Gerencia o estado e a lógica de movimento dos átomos nas duas matrizes, usando NumPy."""
    
    def __init__(self):
        self.sizes = {0: SIZE_AMBIENTE, 1: SIZE_TANQUE} # 0: Ambiente (5x5), 1: Tanque (3x3)
        
        # Estruturas de dados
        # Ocupação: set{(matrix_id, row, col), ...} para checagem rápida de colisão
        self.occupied_positions = set()
        
        # Posições dos átomos: Array NumPy [N, 3] onde [mid, r, c]
        initial_tanque_positions = []
        for r in range(SIZE_TANQUE):
            for c in range(SIZE_TANQUE):
                initial_tanque_positions.append((1, r, c))
        # O array atoms_list armazena as coordenadas de todos os 9 átomos
        self.atoms_list = np.array(initial_tanque_positions, dtype=int) 

        # Preenche o set de ocupação inicial
        for pos in initial_tanque_positions:
            self.occupied_positions.add(pos)

    def move_random_atom(self):
        """
        Escolhe um átomo aleatório e tenta movê-lo,
        checando fronteira, colisão e a ligação especial.
        """
        if self.atoms_list.size == 0:
            return False

        # 1. Escolhe um átomo aleatório (índice na matriz NumPy)
        idx = random.randrange(len(self.atoms_list))
        
        # Obtém a posição atual do array NumPy
        current_mid, current_r, current_c = self.atoms_list[idx]
        current_pos = (current_mid, current_r, current_c)
        
        # 2. Escolhe uma direção aleatória (dr, dc): Cima, Baixo, Direita, Esquerda
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        dr, dc = random.choice(directions)
        
        target_mid = current_mid
        target_r = current_r + dr
        target_c = current_c + dc
        
        # --- LÓGICA DA LIGAÇÃO ESPECIAL (MOTOR) ---
        # Regra: Tanque(1) (0, 0) -> Ambiente(0) (0, 4) se o movimento for para a esquerda (dc == -1)
        if current_mid == 1 and current_r == 0 and current_c == 0 and dc == -1:
            target_mid = 0
            target_r = 0
            target_c = SIZE_AMBIENTE - 1 # Posição (0, 4) na matriz 5x5 (0)

        # --- LÓGICA DE MOVIMENTO NORMAL/FRONTEIRA ---
        else:
            # 3. Checagem de Limite (Fronteira)
            size = self.sizes[current_mid]
            is_in_bounds = (0 <= target_r < size and 0 <= target_c < size)
            
            if not is_in_bounds:
                return False # Movimento negado por limite de fronteira
        
        # Posição de destino final (pode ser na mesma matriz ou na outra)
        target_pos = (target_mid, target_r, target_c)
        
        # 4. Checagem de Colisão (Se o bloco de destino está ocupado)
        is_colliding = target_pos in self.occupied_positions
        
        if is_colliding:
            return False # Movimento negado por colisão

        # --- MOVIMENTO BEM-SUCEDIDO ---
        
        # 1. Atualiza as estruturas de dados de ocupação
        self.occupied_positions.remove(current_pos)
        self.occupied_positions.add(target_pos)
        
        # 2. Atualiza a posição no array NumPy
        self.atoms_list[idx] = [target_mid, target_r, target_c]
            
        return True

# ----------------------------------------------------------------------
## FUNÇÕES GRÁFICAS (Turtle)

def draw_grid(t, start_x, start_y, size, color):
    """Desenha as linhas de uma matriz."""
    t.speed(0)
    t.penup()
    t.pensize(2)
    t.color(color)
    
    end_coord_x = start_x + size * CELL_SIZE
    end_coord_y = start_y + size * CELL_SIZE
    
    for i in range(size + 1):
        # Linhas Verticais
        x = start_x + i * CELL_SIZE
        t.goto(x, start_y)
        t.pendown()
        t.goto(x, end_coord_y)
        t.penup()
        
        # Linhas Horizontais
        y = start_y + i * CELL_SIZE
        t.goto(start_x, y)
        t.pendown()
        t.goto(end_coord_x, y)
        t.penup()

def setup_screen():
    """Configura a tela do Turtle e desenha as duas matrizes."""
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Simulação Dual-Matriz de Entropia (NumPy)")
    screen.bgcolor("lightyellow")
    screen.tracer(0) 
    
    desenhista = turtle.Turtle()
    desenhista.hideturtle()

    # Desenha Matriz Ambiente (Esquerda, 5x5)
    draw_grid(desenhista, START_X_AMBIENTE, START_Y, SIZE_AMBIENTE, "blue")
    
    # Desenha Matriz Tanque (Direita, 3x3)
    draw_grid(desenhista, START_X_TANQUE, START_Y, SIZE_TANQUE, "red")

    # Indica a Ligação Especial (Motor: Tanque(0,0) -> Ambiente(0,4))
    desenhista.penup()
    desenhista.color("green")
    desenhista.pensize(3)
    
    # Posição de Saída (Tanque 3x3, 0, 0)
    x1, y1 = map_coords_to_screen(1, 0, 0)
    # Posição de Entrada (Ambiente 5x5, 0, 4)
    x2, y2 = map_coords_to_screen(0, 0, SIZE_AMBIENTE - 1)
    
    # Desenha um marcador de ligação 
    desenhista.goto(x1, y1)
    desenhista.dot(10, "green")
    desenhista.goto(x2, y2)
    desenhista.dot(10, "green")
    
    return screen, desenhista

def create_atom_turtles(num_atoms):
    """Cria os objetos Turtle para representar os átomos."""
    atomos = []
    for _ in range(num_atoms):
        a = turtle.Turtle()
        a.shape("circle")
        a.color("orange")
        a.turtlesize(CELL_SIZE / 30) 
        a.penup()
        atomos.append(a)
    return atomos

def update_atoms_and_display(screen, atomos_turtles, atoms_array, passo):
    """Atualiza a posição dos átomos na tela e o status."""
    
    # Atualiza a posição de cada Turtle usando o array NumPy
    for i in range(len(atoms_array)):
        mid, r, c = atoms_array[i]
        x, y = map_coords_to_screen(mid, r, c)
        atomos_turtles[i].goto(x, y)
    
    # Atualiza o texto de status
    status_turtle.clear()
    
    # Conta os átomos no Tanque (mid == 1) usando NumPy
    atomos_no_tanque = np.sum(atoms_array[:, 0] == 1)
    
    status_turtle.write(
        f"Passo: {passo}/{N_MOVIMENTOS} | Átomos no Tanque (3x3): {atomos_no_tanque}", 
        align="center", font=("Arial", 14, "bold")
    )
    
    screen.update()

# Objeto Turtle para o texto de status
status_turtle = turtle.Turtle()
status_turtle.penup()
status_turtle.hideturtle()
status_turtle.goto(0, START_Y + SIZE_AMBIENTE * CELL_SIZE / 2 + 50)


# ----------------------------------------------------------------------
## FUNÇÃO PRINCIPAL DA ANIMAÇÃO

def run_dual_grid_simulation_numpy():
    """Executa a simulação principal e a animação."""
    
    screen, _ = setup_screen()
    
    sim = DualGridSimulator()
    atomos_turtles = create_atom_turtles(len(sim.atoms_list))
    
    print(f"Iniciando simulação dual-matriz com NumPy: Tanque ({SIZE_TANQUE}x{SIZE_TANQUE}) e Ambiente ({SIZE_AMBIENTE}x{SIZE_AMBIENTE}).")
    
    for passo in range(N_MOVIMENTOS):
        
        # Lógica de movimento
        sim.move_random_atom()
        
        # Atualização gráfica
        update_atoms_and_display(screen, atomos_turtles, sim.atoms_list, passo + 1)
        
        time.sleep(DELAY)
        
        # Condição de parada: Se o tanque (Matriz 3x3) esvaziar
        if np.sum(sim.atoms_list[:, 0] == 1) == 0:
             break

    # Mensagem final
    status_turtle.goto(0, 0)
    status_turtle.color("darkgreen")
    status_turtle.write(
        f"SIMULAÇÃO CONCLUÍDA após {passo + 1} passos.", 
        align="center", font=("Arial", 16, "bold")
    )
    screen.update()
    
    screen.mainloop()

if __name__ == "__main__":
    # ATENÇÃO: Descomente a linha abaixo para executar a animação em uma nova janela.
    run_dual_grid_simulation_numpy()