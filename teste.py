import random
import time
import turtle
import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# 1. CONFIGURAÇÕES GERAIS (CONSTANTES)
# ==============================================================================
class Config:
    # Parâmetros da Simulação
    SIZE_TANK = 3       # 3x3
    SIZE_AMBIENTE = 5   # 5x5
    N_MOVIMENTOS = 900  # Passos por simulação
    DELAY_ANIMACAO = 0.02
    
    # Parâmetros Gráficos (Turtle)
    TAMANHO_GRAD = 50
    ESPACO_ENTRE_GRADS = 50
    
    # Cores
    COR_AMBIENTE = "#E0E0E0"  # Cinza claro
    COR_TANK = "#ADD8E6"      # Azul claro
    COR_ATOMO = "blue"
    
    @classmethod
    def get_dimensoes_tela(cls):
        largura_ambiente = cls.SIZE_AMBIENTE * cls.TAMANHO_GRAD
        largura_tank = cls.SIZE_TANK * cls.TAMANHO_GRAD
        largura_total = largura_ambiente + cls.ESPACO_ENTRE_GRADS + largura_tank
        
        tela_largura = largura_total + 100
        tela_altura = max(cls.SIZE_AMBIENTE, cls.SIZE_TANK) * cls.TAMANHO_GRAD + 100
        
        # Ponto zero (centro da tela) para alinhar os desenhos
        inicio_x_amb = -largura_total / 2
        inicio_x_tnk = inicio_x_amb + largura_ambiente + cls.ESPACO_ENTRE_GRADS
        inicio_y = -cls.SIZE_AMBIENTE * cls.TAMANHO_GRAD / 2
        
        return {
            'width': tela_largura,
            'height': tela_altura,
            'inicio_x_amb': inicio_x_amb,
            'inicio_x_tnk': inicio_x_tnk,
            'inicio_y': inicio_y
        }

# ==============================================================================
# 2. LÓGICA DA SIMULAÇÃO (MOTOR FÍSICO)
# ==============================================================================
class SimulacaoEntropia:   
    
    def __init__(self):
        self.sizes = {0: Config.SIZE_AMBIENTE, 1: Config.SIZE_TANK}
        self.posicoes_ocupadas = set()
        
        # Inicializa átomos (todos no tanque - ID 1)
        posicao_inicial_tank = []
        for linha in range(Config.SIZE_TANK):
            for coluna in range(Config.SIZE_TANK):
                posicao_inicial_tank.append((1, linha, coluna))
                
        self.lista_atomos = np.array(posicao_inicial_tank, dtype=int) 
        
        # Preenche conjunto de colisão
        for posicao in posicao_inicial_tank:
            self.posicoes_ocupadas.add(posicao)
            
        # Direções possíveis (pré-definidas para performance)
        self.direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def movimento_aleatorio(self):
        """Tenta mover um átomo aleatório. Retorna True se moveu, False se bloqueado."""
        if self.lista_atomos.size == 0:
            return False

        # Escolhe átomo e direção
        index = random.randrange(len(self.lista_atomos))
        id_matriz, idx_linha, idx_coluna = self.lista_atomos[index]
        posicao_atual = (id_matriz, idx_linha, idx_coluna)
        
        d_linha, d_coluna = random.choice(self.direcoes)
        
        # Variáveis temporárias para o destino
        novo_id = id_matriz
        nova_linha = idx_linha + d_linha
        nova_coluna = idx_coluna + d_coluna
        
        # --- Lógica de Portal (Gargalo) ---
        # 1. Do Tank (1) para Ambiente (0): Saída em (0,0) indo para Esquerda
        if id_matriz == 1 and idx_linha == 0 and idx_coluna == 0 and d_coluna == -1:
            novo_id = 0
            nova_linha = 0
            nova_coluna = Config.SIZE_AMBIENTE - 1
            
        # 2. Do Ambiente (0) para Tank (1): Entrada em (0, max) indo para Direita
        elif id_matriz == 0 and idx_linha == 0 and idx_coluna == Config.SIZE_AMBIENTE - 1 and d_coluna == 1:
            novo_id = 1
            nova_linha = 0
            nova_coluna = 0
            
        # --- Lógica de Fronteira (Paredes) ---
        else:
            tamanho_atual = self.sizes[id_matriz]
            dentro_limites = (0 <= nova_linha < tamanho_atual and 0 <= nova_coluna < tamanho_atual)
            if not dentro_limites:
                return False
        
        posicao_final = (novo_id, nova_linha, nova_coluna)
        
        # --- Lógica de Exclusão (Colisão) ---
        if posicao_final in self.posicoes_ocupadas:
            return False

        # --- Executa o Movimento ---
        self.posicoes_ocupadas.remove(posicao_atual)
        self.posicoes_ocupadas.add(posicao_final)
        self.lista_atomos[index] = [novo_id, nova_linha, nova_coluna]
            
        return True

    def rodar_lote_rapido(self, n_passos):
        """Roda N passos sem animação para fins estatísticos"""
        for _ in range(n_passos):
            self.movimento_aleatorio()
        return self.coletar_dados()

    def coletar_dados(self):
        """Retorna dicionário com estado atual"""
        atomos_amb = np.sum(self.lista_atomos[:, 0] == 0)
        atomos_tank = np.sum(self.lista_atomos[:, 0] == 1)
        return {
            'ambiente': atomos_amb,
            'tank': atomos_tank,
            'total': len(self.lista_atomos)
        }

# ==============================================================================
# 3. VISUALIZAÇÃO (TURTLE)
# ==============================================================================
class VisualizadorTurtle:
    def __init__(self):
        self.dims = Config.get_dimensoes_tela()
        self.screen = None
        self.turtle_grade = None
        self.turtles_atomos = []

    def converter_coord(self, matrix_id, linha, coluna):
        """Converte grade (matriz) para pixels (x,y)"""
        start_x = self.dims['inicio_x_amb'] if matrix_id == 0 else self.dims['inicio_x_tnk']
        
        x = start_x + coluna * Config.TAMANHO_GRAD + Config.TAMANHO_GRAD / 2
        y = self.dims['inicio_y'] + linha * Config.TAMANHO_GRAD + Config.TAMANHO_GRAD / 2
        return x, y

    def desenhar_grade(self, t, inicio_x, inicio_y, size, cor_bg):
        """Desenha o grid quadrado"""
        t.speed(0); t.penup(); t.pensize(2); t.color("black")
        
        # Fundo colorido (opcional)
        # t.goto(inicio_x, inicio_y); t.begin_fill(); t.fillcolor(cor_bg)
        # ... lógica de fill ... t.end_fill()
        
        end_x = inicio_x + size * Config.TAMANHO_GRAD
        end_y = inicio_y + size * Config.TAMANHO_GRAD
        
        for i in range(size + 1):
            offset = i * Config.TAMANHO_GRAD
            # Verticais
            t.goto(inicio_x + offset, inicio_y); t.pendown(); t.goto(inicio_x + offset, end_y); t.penup()
            # Horizontais
            t.goto(inicio_x, inicio_y + offset); t.pendown(); t.goto(end_x, inicio_y + offset); t.penup()

    def setup_tela(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=self.dims['width'], height=self.dims['height'])
        self.screen.title("Simulação de Entropia e Difusão")
        self.screen.tracer(0)
        
        self.turtle_grade = turtle.Turtle()
        self.turtle_grade.hideturtle()
        
        # Desenha Ambiente
        self.desenhar_grade(self.turtle_grade, self.dims['inicio_x_amb'], self.dims['inicio_y'], Config.SIZE_AMBIENTE, Config.COR_AMBIENTE)
        # Desenha Tank
        self.desenhar_grade(self.turtle_grade, self.dims['inicio_x_tnk'], self.dims['inicio_y'], Config.SIZE_TANK, Config.COR_TANK)
        
        # Desenha conexão (Gargalo)
        self.turtle_grade.pensize(4); self.turtle_grade.color("gray")
        x1, y1 = self.converter_coord(1, 0, 0)
        x2, y2 = self.converter_coord(0, 0, Config.SIZE_AMBIENTE - 1)
        self.turtle_grade.goto(x1, y1); self.turtle_grade.dot(10)
        self.turtle_grade.goto(x2, y2); self.turtle_grade.dot(10)

    def preparar_atomos(self, n_atomos):
        self.turtles_atomos = []
        for _ in range(n_atomos):
            t = turtle.Turtle()
            t.shape("circle")
            t.turtlesize(Config.TAMANHO_GRAD / 35)
            t.color(Config.COR_ATOMO)
            t.penup()
            t.hideturtle()
            self.turtles_atomos.append(t)

    def atualizar_tela(self, lista_atomos):
        for i, (mat_id, lin, col) in enumerate(lista_atomos):
            x, y = self.converter_coord(mat_id, lin, col)
            self.turtles_atomos[i].goto(x, y)
            self.turtles_atomos[i].showturtle()
        self.screen.update()

# ==============================================================================
# 4. ANÁLISE E GRÁFICOS (MATPLOTLIB)
# ==============================================================================
def plotar_histograma(resultados):
    """Gera gráfico de distribuição de frequência"""
    atomos_ambiente = [r['ambiente'] for r in resultados]
    total_atomos = resultados[0]['total']
    
    plt.figure(figsize=(10, 6))
    
    # Histograma
    valores_unicos = sorted(list(set(atomos_ambiente)))
    frequencias = [atomos_ambiente.count(v) for v in valores_unicos]
    
    barras = plt.bar(valores_unicos, frequencias, color='#4a90e2', edgecolor='black', alpha=0.8, zorder=3)
    
    # Linhas de Referência
    media = np.mean(atomos_ambiente)
    plt.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Média ({media:.1f})')
    plt.axvline(total_atomos, color='green', linestyle=':', label='Total Possível')
    
    # Estilização
    plt.title(f'Distribuição de Partículas no Ambiente após {Config.N_MOVIMENTOS} passos', fontsize=14)
    plt.xlabel('Número de Partículas no Ambiente', fontsize=12)
    plt.ylabel('Frequência (Simulações)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    plt.legend()
    
    # Anotação nas barras
    for barra in barras:
        height = barra.get_height()
        if height > 0:
            plt.text(barra.get_x() + barra.get_width()/2., height,
                     f'{int(height)}', ha='center', va='bottom', fontsize=8)

    txt_stats = (f"Simulações: {len(resultados)}\n"
                 f"Desvio Padrão: {np.std(atomos_ambiente):.2f}\n"
                 f"Moda: {max(set(atomos_ambiente), key=atomos_ambiente.count)}")
    
    plt.gcf().text(0.02, 0.95, txt_stats, fontsize=9, 
                   bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    plt.show()

# ==============================================================================
# 5. EXECUÇÃO PRINCIPAL
# ==============================================================================
def main():
    while True:
        print("\n--- SIMULADOR DE ENTROPIA ---")
        print("1. Ver animação visual (Turtle)")
        print(f"2. Rodar estatística (Matplotlib) - Default: 1000 simulações")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            # Modo Visual
            vis = VisualizadorTurtle()
            sim = SimulacaoEntropia()
            vis.setup_tela()
            vis.preparar_atomos(len(sim.lista_atomos))
            
            print("Iniciando animação... (Feche a janela do Turtle para voltar)")
            try:
                for _ in range(Config.N_MOVIMENTOS):
                    sim.movimento_aleatorio()
                    vis.atualizar_tela(sim.lista_atomos)
                    time.sleep(Config.DELAY_ANIMACAO)
                print("Animação finalizada.")
                turtle.done()
            except turtle.Terminator:
                print("Janela fechada pelo usuário.")
            
            # Necessário reiniciar o turtle se quiser rodar de novo na mesma execução
            turtle.Screen().reset() 
            
        elif escolha == '2':
            # Modo Estatístico
            try:
                qtd = int(input("Quantas simulações deseja rodar? (Recomendado: 1000): ") or 1000)
            except ValueError:
                qtd = 1000
                
            resultados = []
            print(f"Processando {qtd} simulações...")
            start = time.time()
            
            for i in range(qtd):
                sim = SimulacaoEntropia()
                dados = sim.rodar_lote_rapido(Config.N_MOVIMENTOS)
                resultados.append(dados)
                
                if (i+1) % (qtd//10 if qtd >= 10 else 1) == 0:
                    print(f"Progresso: {i+1}/{qtd}")
                    
            print(f"Concluído em {time.time() - start:.2f} segundos.")
            plotar_histograma(resultados)
            
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()