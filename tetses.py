import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict
import time

class SimuladorEntropia:
    """
    Simulador do "carro" movido por átomos em movimento browniano
    """
    
    def __init__(self, tamanho_ambiente=100, tamanho_tanque=10, capacidade_tanque=100):
        """
        Inicializa o simulador
        
        Args:
            tamanho_ambiente: Tamanho do ambiente (quadrado)
            tamanho_tanque: Tamanho do tanque (quadrado)
            capacidade_tanque: Número máximo de átomos no tanque
        """
        self.tamanho_ambiente = tamanho_ambiente
        self.tamanho_tanque = tamanho_tanque
        self.capacidade_tanque = capacidade_tanque
        
        # Posição inicial do tanque no centro do ambiente
        self.tanque_x = tamanho_ambiente // 2
        self.tanque_y = tamanho_ambiente // 2
        
        # Posição do carro (relativa ao ambiente)
        self.carro_x = self.tanque_x
        self.carro_y = self.tanque_y
        
        # Átomos no tanque: lista de posições (x, y) relativas ao tanque
        self.atomos = []
        self.inicializar_atomos()
        
        # Histórico de posições para animação
        self.historico_carro = [(self.carro_x, self.carro_y)]
        
    def inicializar_atomos(self):
        """Inicializa os átomos distribuídos aleatoriamente no tanque"""
        self.atomos = []
        for _ in range(self.capacidade_tanque):
            x = random.randint(-self.tanque_tamanho_half, self.tanque_tamanho_half)
            y = random.randint(-self.tanque_tamanho_half, self.tanque_tamanho_half)
            self.atomos.append((x, y))
    
    @property
    def tanque_tamanho_half(self):
        """Metade do tamanho do tanque"""
        return self.tamanho_tanque // 2
    
    def movimento_atomo(self, atomo_idx):
        """
        Move um átomo em uma direção aleatória (movimento browniano)
        
        Returns:
            True se o átomo colidiu com a parede do tanque
        """
        x, y = self.atomos[atomo_idx]
        
        # Direção aleatória
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        # Nova posição
        novo_x = x + dx
        novo_y = y + dy
        
        # Verifica se colidiu com as paredes do tanque
        colisao_x = abs(novo_x) > self.tanque_tamanho_half
        colisao_y = abs(novo_y) > self.tanque_tamanho_half
        
        if colisao_x or colisao_y:
            # Átomo colide com a parede - move o carro na direção oposta
            self.mover_carro(-dx if colisao_x else 0, -dy if colisao_y else 0)
            # Mantém o átomo dentro do tanque (reflete)
            novo_x = x - dx if colisao_x else novo_x
            novo_y = y - dy if colisao_y else novo_y
        
        # Atualiza posição do átomo
        self.atomos[atomo_idx] = (novo_x, novo_y)
        
        return colisao_x or colisao_y
    
    def mover_carro(self, dx, dy):
        """Move o carro no ambiente"""
        novo_x = self.carro_x + dx
        novo_y = self.carro_y + dy
        
        # Limita o movimento aos limites do ambiente
        self.carro_x = max(0, min(self.tamanho_ambiente - 1, novo_x))
        self.carro_y = max(0, min(self.tamanho_ambiente - 1, novo_y))
        
        self.historico_carro.append((self.carro_x, self.carro_y))
    
    def simular_episodio(self, n_movimentos):
        """
        Simula um episódio completo
        
        Args:
            n_movimentos: Número de movimentos de átomos a simular
        
        Returns:
            Posição final do carro (x, y)
        """
        # Reinicia para início do episódio
        self.carro_x = self.tanque_x
        self.carro_y = self.tanque_y
        self.historico_carro = [(self.carro_x, self.carro_y)]
        self.inicializar_atomos()
        
        # Executa n movimentos aleatórios de átomos
        colisoes = 0
        for _ in range(n_movimentos):
            # Escolhe um átomo aleatório
            atomo_idx = random.randint(0, len(self.atomos) - 1)
            
            # Move o átomo
            if self.movimento_atomo(atomo_idx):
                colisoes += 1
        
        return (self.carro_x, self.carro_y, colisoes)
    
    def obter_posicoes_absolutas_atomos(self):
        """Retorna as posições absolutas dos átomos no ambiente"""
        pos_absolutas = []
        for x_rel, y_rel in self.atomos:
            x_abs = self.tanque_x + x_rel
            y_abs = self.tanque_y + y_rel
            pos_absolutas.append((x_abs, y_abs))
        return pos_absolutas


class AnalisadorEstatistico:
    """Classe para análise estatística dos resultados das simulações"""
    
    def __init__(self):
        self.resultados = []
        self.contagem_posicoes = defaultdict(int)
    
    def adicionar_resultado(self, posicao_final):
        """Adiciona um resultado de simulação"""
        self.resultados.append(posicao_final)
        self.contagem_posicoes[posicao_final] += 1
    
    def gerar_grafico_distribuicao(self, tamanho_ambiente=100, n_movimentos=None):
        """
        Gera gráfico de distribuição das posições finais (similar ao vídeo)
        """
        if not self.resultados:
            print("Nenhum resultado para plotar!")
            return
        
        # Extrai coordenadas
        xs, ys, colisoes = zip(*self.resultados) if len(self.resultados[0]) == 3 else zip(*self.resultados)
        
        # Criação do gráfico
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot das posições finais
        scatter = ax.scatter(xs, ys, c=colisoes if len(self.resultados[0]) == 3 else 'blue', 
                            alpha=0.6, cmap='viridis', s=30)
        
        # Adiciona barra de cores se tiver dados de colisões
        if len(self.resultados[0]) == 3:
            plt.colorbar(scatter, label='Número de colisões no episódio')
        
        # Configurações do gráfico
        ax.set_xlim(0, tamanho_ambiente)
        ax.set_ylim(0, tamanho_ambiente)
        ax.set_xlabel('Posição X')
        ax.set_ylabel('Posição Y')
        ax.set_title(f'Distribuição das Posições Finais do Carro\n'
                    f'{len(self.resultados)} simulações' + 
                    (f' | n={n_movimentos}' if n_movimentos else ''))
        ax.grid(True, alpha=0.3)
        
        # Adiciona ponto inicial
        ax.plot(tamanho_ambiente//2, tamanho_ambiente//2, 'r*', markersize=15, label='Posição Inicial')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Estatísticas básicas
        print(f"\n📊 Estatísticas das {len(self.resultados)} simulações:")
        print(f"  Posição média: ({np.mean(xs):.2f}, {np.mean(ys):.2f})")
        print(f"  Desvio padrão: ({np.std(xs):.2f}, {np.std(ys):.2f})")
        if len(self.resultados[0]) == 3:
            print(f"  Colisões médias por episódio: {np.mean(colisoes):.2f}")
    
    def analisar_variacao_n(self, simulador, n_valores, simulacoes_por_n=100):
        """
        Analisa o efeito de variar o número de movimentos (n)
        """
        desvios = []
        
        for n in n_valores:
            print(f"Simulando com n={n}...")
            resultados_n = []
            
            for _ in range(simulacoes_por_n):
                x, y, _ = simulador.simular_episodio(n)
                resultados_n.append((x, y))
            
            # Calcula desvio padrão das posições
            xs, ys = zip(*resultados_n)
            desvio = (np.std(xs) + np.std(ys)) / 2
            desvios.append(desvio)
            
            print(f"  Desvio: {desvio:.2f}")
        
        # Gráfico de desvio vs n
        plt.figure(figsize=(10, 6))
        plt.plot(n_valores, desvios, 'bo-', linewidth=2, markersize=8)
        plt.xlabel('Número de movimentos (n)')
        plt.ylabel('Desvio padrão médio da posição')
        plt.title('Efeito do número de movimentos na dispersão do carro')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class Animacao:
    """Classe para criar animação da simulação"""
    
    def __init__(self, simulador, n_movimentos=500):
        self.simulador = simulador
        self.n_movimentos = n_movimentos
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.atomos_scatter = None
        self.carro_scatter = None
        self.tanque_patch = None
        self.frame_count = 0
        
    def init_animation(self):
        """Inicializa a animação"""
        self.ax.clear()
        self.ax.set_xlim(0, self.simulador.tamanho_ambiente)
        self.ax.set_ylim(0, self.simulador.tamanho_ambiente)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Simulação Entropia: Carro Movido por Átomos')
        
        # Desenha tanque
        from matplotlib.patches import Rectangle
        tanque = Rectangle((self.simulador.tanque_x - self.simulador.tanque_tamanho_half,
                           self.simulador.tanque_y - self.simulador.tanque_tamanho_half),
                          self.simulador.tamanho_tanque, self.simulador.tamanho_tanque,
                          fill=False, edgecolor='blue', linewidth=2, linestyle='--')
        self.ax.add_patch(tanque)
        
        return []
    
    def update_animation(self, frame):
        """Atualiza um frame da animação"""
        if self.frame_count < self.n_movimentos:
            # Move um átomo aleatório
            atomo_idx = random.randint(0, len(self.simulador.atomos) - 1)
            self.simulador.movimento_atomo(atomo_idx)
            self.frame_count += 1
        
        # Atualiza plot dos átomos
        pos_atomos = self.simulador.obter_posicoes_absolutas_atomos()
        xs_atomos, ys_atomos = zip(*pos_atomos) if pos_atomos else ([], [])
        
        # Limpa e redesenh
        self.ax.clear()
        self.init_animation()
        
        # Plota átomos
        self.ax.scatter(xs_atomos, ys_atomos, c='red', s=20, alpha=0.6, label='Átomos')
        
        # Plota carro e trajetória
        xs_carro, ys_carro = zip(*self.simulador.historico_carro)
        self.ax.plot(xs_carro, ys_carro, 'g-', alpha=0.5, linewidth=1, label='Trajetória')
        self.ax.scatter([self.simulador.carro_x], [self.simulador.carro_y], 
                       c='green', s=100, marker='s', label='Carro')
        
        self.ax.legend(loc='upper right')
        self.ax.text(0.02, 0.98, f'Movimento: {self.frame_count}/{self.n_movimentos}',
                    transform=self.ax.transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        return []
    
    def animar(self):
        """Executa a animação"""
        # Reinicia simulador
        self.simulador.carro_x = self.simulador.tanque_x
        self.simulador.carro_y = self.simulador.tanque_y
        self.simulador.historico_carro = [(self.simulador.carro_x, self.simulador.carro_y)]
        self.simulador.inicializar_atomos()
        self.frame_count = 0
        
        # Cria animação
        anim = FuncAnimation(self.fig, self.update_animation, init_func=self.init_animation,
                           frames=self.n_movimentos, interval=50, blit=False, repeat=False)
        
        plt.tight_layout()
        plt.show()


def main():
    """Função principal para execução do projeto"""
    print("=" * 60)
    print("PROJETO ENTROPIA - Simulador do Carro Movido por Átomos")
    print("=" * 60)
    
    # Configurações iniciais
    TAMANHO_AMBIENTE = 100
    TAMANHO_TANQUE = 20
    CAPACIDADE_TANQUE = 50
    
    # 1. Cria simulador
    simulador = SimuladorEntropia(
        tamanho_ambiente=TAMANHO_AMBIENTE,
        tamanho_tanque=TAMANHO_TANQUE,
        capacidade_tanque=CAPACIDADE_TANQUE
    )
    
    # 2. Cria analisador
    analisador = AnalisadorEstatistico()
    
    # 3. Simulações para análise estatística
    N_SIMULACOES = 1000
    N_MOVIMENTOS = 2000
    
    print(f"\n🔬 Executando {N_SIMULACOES} simulações com n={N_MOVIMENTOS}...")
    
    for i in range(N_SIMULACOES):
        if (i + 1) % 100 == 0:
            print(f"  Simulação {i + 1}/{N_SIMULACOES}")
        
        # Executa um episódio
        resultado = simulador.simular_episodio(N_MOVIMENTOS)
        analisador.adicionar_resultado(resultado)
    
    print("✅ Simulações concluídas!")
    
    # 4. Gera gráfico de distribuição
    print("\n📈 Gerando gráfico de distribuição...")
    analisador.gerar_grafico_distribuicao(
        tamanho_ambiente=TAMANHO_AMBIENTE,
        n_movimentos=N_MOVIMENTOS
    )
    
    # 5. Análise de variação de n
    print("\n📊 Analisando efeito de variar n...")
    n_valores = [100, 500, 1000, 2000, 5000, 10000]
    analisador.analisar_variacao_n(simulador, n_valores, simulacoes_por_n=50)
    
    # 6. Análise de variação de tamanhos
    print("\n🔧 Analisando efeito do tamanho do tanque...")
    tamanhos_tanque = [5, 10, 20, 30, 40]
    desvios_tanque = []
    
    for tamanho in tamanhos_tanque:
        simulador_var = SimuladorEntropia(
            tamanho_ambiente=TAMANHO_AMBIENTE,
            tamanho_tanque=tamanho,
            capacidade_tanque=CAPACIDADE_TANQUE
        )
        
        resultados = []
        for _ in range(100):
            x, y, _ = simulador_var.simular_episodio(N_MOVIMENTOS)
            resultados.append((x, y))
        
        xs, ys = zip(*resultados)
        desvio = (np.std(xs) + np.std(ys)) / 2
        desvios_tanque.append(desvio)
        print(f"  Tanque {tamanho}x{tamanho}: desvio = {desvio:.2f}")
    
    # Gráfico tamanho vs desvio
    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_tanque, desvios_tanque, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('Tamanho do tanque')
    plt.ylabel('Desvio padrão médio da posição')
    plt.title('Efeito do tamanho do tanque na dispersão do carro')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # 7. Opção de animação (bônus)
    print("\n🎬 Deseja ver a animação? (pode ser lento para muitos átomos)")
    resposta = input("Digite 's' para sim ou qualquer tecla para não: ").lower()
    
    if resposta == 's':
        print("Criando animação...")
        animacao = Animacao(simulador, n_movimentos=300)
        animacao.animar()
    
    print("\n" + "=" * 60)
    print("✅ Projeto Entropia concluído!")
    print("=" * 60)


def modo_interativo():
    """Modo interativo para experimentação"""
    print("\n🎮 MODO INTERATIVO")
    print("Configure sua simulação:")
    
    tamanho_ambiente = int(input("Tamanho do ambiente (padrão 100): ") or "100")
    tamanho_tanque = int(input("Tamanho do tanque (padrão 20): ") or "20")
    capacidade = int(input("Número de átomos (padrão 50): ") or "50")
    
    simulador = SimuladorEntropia(tamanho_ambiente, tamanho_tanque, capacidade)
    analisador = AnalisadorEstatistico()
    
    while True:
        print("\nOpções:")
        print("1. Executar uma simulação")
        print("2. Executar múltiplas simulações")
        print("3. Ver animação")
        print("4. Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            n = int(input("Número de movimentos (n): "))
            resultado = simulador.simular_episodio(n)
            print(f"Posição final: {resultado[:2]}, Colisões: {resultado[2]}")
            
        elif opcao == "2":
            n_sim = int(input("Número de simulações: "))
            n_mov = int(input("Número de movimentos por simulação: "))
            
            for i in range(n_sim):
                resultado = simulador.simular_episodio(n_mov)
                analisador.adicionar_resultado(resultado)
                
                if (i + 1) % 10 == 0:
                    print(f"  Concluído: {i + 1}/{n_sim}")
            
            analisador.gerar_grafico_distribuicao(tamanho_ambiente, n_mov)
            
        elif opcao == "3":
            n_mov = int(input("Número de movimentos na animação: "))
            animacao = Animacao(simulador, n_movimentos=n_mov)
            animacao.animar()
            
        elif opcao == "4":
            break


if __name__ == "__main__":
    print("Selecione o modo de execução:")
    print("1. Execução completa do projeto (recomendado)")
    print("2. Modo interativo (experimentação)")
    
    modo = input("Escolha (1 ou 2): ")
    
    if modo == "2":
        modo_interativo()
    else:
        main()