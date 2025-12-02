import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from itertools import product

# --- CONFIGURAÇÕES GLOBAIS ---
SIZE_TANQUE = 3     # Matriz da Direita (Tanque)
SIZE_AMBIENTE = 5   # Matriz da Esquerda (Ambiente)
NUM_ATOMS = 9       # Número total de átomos
N_MOVIMENTOS = 1000 # Número de passos na simulação (Loop da animação)
INTERVAL = 50       # Intervalo de atualização da animação em ms

# --- CÁLCULO DAS POSSIBILIDADES (PRÉ-CÁLCULO DA ENTROPIA) ---
T_CELLS = SIZE_TANQUE * SIZE_TANQUE    # 9
M_CELLS = SIZE_AMBIENTE * SIZE_AMBIENTE # 25

# Pré-calcula S = ln(Omega) para todos os estados possíveis.
# A chave do dicionário é o número de átomos FORA do Tanque (NA).
ln_omega_values = {}
for nt in range(NUM_ATOMS + 1):
    na = NUM_ATOMS - nt # Número de átomos Fora do Tanque (Eixo X)
    
    # Se o número de átomos exceder o número de células em qualquer matriz, Omega = 0
    if nt > T_CELLS or na > M_CELLS:
        ln_omega_values[na] = -np.inf 
        continue
    
    # Cálculo das Permutações P(n, k) = n! / (n-k)! usando lgamma (ln de fatorial)
    # Permutações no Tanque (PT)
    log_p_t = math.lgamma(T_CELLS + 1) - math.lgamma(T_CELLS - nt + 1)
    
    # Permutações no Ambiente (PM)
    log_p_m = math.lgamma(M_CELLS + 1) - math.lgamma(M_CELLS - na + 1)
    
    # Entropia S = ln(Omega) = ln(PT * PM) = log_p_t + log_p_m
    ln_omega_values[na] = log_p_t + log_p_m

class DualGridSimulator:
    """Gerencia a lógica de movimento e estado, usando NumPy."""
    
    def __init__(self):
        self.sizes = {0: SIZE_AMBIENTE, 1: SIZE_TANQUE} # 0: Ambiente, 1: Tanque
        self.occupied_positions = set()
        
        # Posições dos átomos: Array NumPy [N, 3] onde [mid, r, c]
        initial_tanque_positions = list(product(range(1, 2), range(SIZE_TANQUE), range(SIZE_TANQUE)))
        self.atoms_list = np.array(initial_tanque_positions, dtype=int) 

        for mid, r, c in self.atoms_list:
            self.occupied_positions.add((mid, r, c))
            
        # Rastreia o estado macro pelo número de átomos no Tanque
        self.current_nt = NUM_ATOMS 
        self.current_na = 0 # Inicialmente, 0 átomos fora do tanque
        self.current_entropy = ln_omega_values[0] # Entropia em NA=0 (NT=9)

    def move_random_atom(self):
        
        idx = random.randrange(len(self.atoms_list))
        current_mid, current_r, current_c = self.atoms_list[idx]
        current_pos = (current_mid, current_r, current_c)
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] 
        dr, dc = random.choice(directions)
        
        target_mid = current_mid
        target_r = current_r + dr
        target_c = current_c + dc
        
        # --- LIGAÇÃO ESPECIAL (MOTOR: Tanque(1) (0, 0) -> Ambiente(0) (0, 4) se movimento Esquerda)
        if current_mid == 1 and current_r == 0 and current_c == 0 and dc == -1:
            target_mid = 0
            target_r = 0
            target_c = SIZE_AMBIENTE - 1
            moved_across_link = True # Movimento 1 -> 0 (Tanque -> Ambiente)

        # --- MOVIMENTO NORMAL/FRONTEIRA ---
        else:
            size = self.sizes[current_mid]
            is_in_bounds = (0 <= target_r < size and 0 <= target_c < size)
            
            if not is_in_bounds:
                return 
        
        target_pos = (target_mid, target_r, target_c)
        
        # Checagem de Colisão (Exclusão de Volume)
        if target_pos in self.occupied_positions:
            return 

        # --- MOVIMENTO BEM-SUCEDIDO ---
        
        self.occupied_positions.remove(current_pos)
        self.occupied_positions.add(target_pos)
        self.atoms_list[idx] = [target_mid, target_r, target_c]
        
        # 2. Atualiza a Entropia
        if current_mid != target_mid:
            # Se saiu do tanque (1 -> 0): Nt diminui em 1 (NA aumenta em 1)
            if current_mid == 1:
                self.current_nt -= 1
            # Se entrou no tanque (0 -> 1): Nt aumenta em 1 (NA diminui em 1)
            else: 
                self.current_nt += 1
                
            self.current_na = NUM_ATOMS - self.current_nt
            self.current_entropy = ln_omega_values[self.current_na]

# ----------------------------------------------------------------------
## FUNÇÕES DE VISUALIZAÇÃO E ANIMAÇÃO (Matplotlib)

def draw_grid_lines(ax, start_x, start_y, size, color, label):
    """Desenha as linhas da matriz e rótulo."""
    
    # Desenha linhas verticais e horizontais
    for i in range(size + 1):
        ax.plot([start_x + i, start_x + i], [start_y, start_y + size], color=color, linewidth=1)
        ax.plot([start_x, start_x + size], [start_y + i, start_y + i], color=color, linewidth=1)

    # Rótulo da matriz
    ax.text(start_x + size / 2, start_y + size + 0.5, label, 
            ha='center', va='center', color=color, fontsize=10, fontweight='bold')

def setup_plot():
    """Configura o layout de subplots para matrizes e gráfico de Entropia."""
    
    fig = plt.figure(figsize=(12, 6))
    
    # Subplot 1: Visualização das Matrizes (Ocupa 2/3 da largura)
    gs = fig.add_gridspec(1, 3, wspace=0.3)
    ax_sim = fig.add_subplot(gs[0, :2])
    
    # Subplot 2: Gráfico de Entropia (Ocupa 1/3 da largura)
    ax_hist = fig.add_subplot(gs[0, 2])
    
    # --- Configurações da Simulação (Matrizes) ---
    
    # Mapa de coordenadas: (mid, r, c) -> (x_plot, y_plot)
    ax_start_x_tanque = SIZE_AMBIENTE + 1 
    ax_sim.set_xlim(-0.5, ax_start_x_tanque + SIZE_TANQUE + 0.5)
    ax_sim.set_ylim(-0.5, SIZE_AMBIENTE + 0.5)
    ax_sim.set_aspect('equal', adjustable='box')
    ax_sim.axis('off') 
    
    draw_grid_lines(ax_sim, 0, 0, SIZE_AMBIENTE, 'blue', 'AMBIENTE (5x5) - Esquerda')
    draw_grid_lines(ax_sim, ax_start_x_tanque, 0, SIZE_TANQUE, 'red', 'TANQUE (3x3) - Direita')
    
    # Linha da Ligação (Motor: Ambiente(0,4) e Tanque(0,0))
    ax_sim.plot([SIZE_AMBIENTE - 1 + 0.5, ax_start_x_tanque + 0.5], [0.5, 0.5], 'g--', linewidth=2, alpha=0.7)
    
    # Scatter plot para os átomos
    scatter = ax_sim.scatter([], [], color='orange', s=200, edgecolors='black', zorder=5)
    
    # Texto de status
    text = ax_sim.text(0.5, -0.1, '', transform=ax_sim.transAxes, ha='center', fontsize=10, fontweight='bold')
    
    # --- Configurações do Gráfico de Entropia ---
    
    ax_hist.bar(ln_omega_values.keys(), ln_omega_values.values(), color='lightgray', edgecolor='black')
    ax_hist.set_title('Entropia $S = \ln \Omega$')
    ax_hist.set_xlabel('Átomos Fora do Tanque ($N_A$)')
    ax_hist.set_ylabel('Logaritmo do Número de Possibilidades ($\ln \Omega$)')
    ax_hist.set_xticks(range(NUM_ATOMS + 1))
    ax_hist.grid(True, axis='y', alpha=0.5)
    
    # Linha vertical para indicar o estado atual
    line, = ax_hist.plot([], [], 'r-', linewidth=3, label='Estado Atual')
    
    return fig, ax_sim, ax_hist, scatter, line, text

def update_plot(frame, sim, scatter, line, text, ax_hist):
    """Função de atualização chamada pela animação."""
    
    # Realiza um passo da simulação
    sim.move_random_atom()
    
    # --- Atualiza Visualização da Simulação (Scatter Plot) ---
    
    positions = []
    ax_start_x_tanque = SIZE_AMBIENTE + 1 
    
    # Mapeia as coordenadas (mid, r, c) para (x_sim, y_sim) para Matplotlib
    for mid, r, c in sim.atoms_list:
        # Note que a ordem é (coluna + offset, linha)
        if mid == 0: # Ambiente (Esquerda)
            x_plot = c + 0.5
        else: # Tanque (Direita)
            x_plot = c + 0.5 + ax_start_x_tanque
        
        y_plot = r + 0.5
        positions.append([x_plot, y_plot])
    
    if positions:
        positions_np = np.array(positions)
        scatter.set_offsets(positions_np)
    
    # --- Atualiza Gráfico de Entropia (Bar Plot) ---
    
    current_na = sim.current_na
    current_entropy = sim.current_entropy
    
    # Mapeia a linha vertical para a Entropia atual usando N_A
    line.set_data([current_na, current_na], [ax_hist.get_ylim()[0], current_entropy])
    
    # Atualiza o texto de status
    text.set_text(f'Passo: {frame+1}/{N_MOVIMENTOS} | $N_A$ (Fora do Tanque): {current_na} | $\ln(\\Omega)$: {current_entropy:.2f}')
    
    return scatter, line, text

def run_simulation_with_plot():
    """Configura e executa a simulação e o gráfico integrados."""
    
    sim = DualGridSimulator()
    fig, ax_sim, ax_hist, scatter, line, text = setup_plot()

    # Define a posição inicial no gráfico de Entropia (N_A=0)
    line.set_data([sim.current_na, sim.current_na], [ax_hist.get_ylim()[0], sim.current_entropy])
    
    # O loop da animação é gerenciado pelo FuncAnimation
    anim = animation.FuncAnimation(
        fig, 
        update_plot, 
        frames=N_MOVIMENTOS, 
        fargs=(sim, scatter, line, text, ax_hist),
        interval=INTERVAL, 
        blit=True, 
        repeat=False
    )
    
    # Abre a janela do Matplotlib e executa a simulação
    plt.show()

if __name__ == "__main__":
    run_simulation_with_plot()