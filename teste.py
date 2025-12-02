import random
import time
import turtle
import matplotlib.pyplot as plt
import numpy as np


size_tank = 3     #tamanho do tank
size_ambiente = 5   #tamanho do ambiente
n_movimentos = 900  #numero de passos de movimento na simulação
delay = 0.05        #atraso em segundos entre cada movimento

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

    def simular_sem_animacao(self, n_movimentos):
        """Executa a simulação sem animação gráfica"""
        for _ in range(n_movimentos):
            self.movento_aleatorio_atomo()
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

def roda_multiplas_simulacoes(n_simulacoes=1000):
    """Roda múltiplas simulações e coleta dados estatísticos"""
    resultados = []
    
    print(f"Rodando {n_simulacoes} simulações...")
    
    for i in range(n_simulacoes):
        # Cria nova simulação
        entropia = Entropia()
        
        # Roda simulação sem animação
        estatisticas = entropia.simular_sem_animacao(n_movimentos)
        resultados.append(estatisticas)
        
        # Progresso
        if (i + 1) % 100 == 0:
            print(f"  Concluído: {i + 1}/{n_simulacoes}")
    
    print("Simulações concluídas!")
    return resultados

def plotar_resultados(resultados):
    """Cria gráficos de coluna com os resultados das simulações"""
    
    # Extrai dados
    atomos_ambiente = [r['atomos_no_ambiente'] for r in resultados]
    atomos_tank = [r['atomos_no_tank'] for r in resultados]
    
    # Configuração do estilo
    plt.style.use('default')
    
    # Cria figura com 2 gráficos de coluna
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Histograma da distribuição de átomos no ambiente
    ax1 = axes[0]
    
    # Cria bins para o histograma
    bins_ambiente = range(min(atomos_ambiente), max(atomos_ambiente) + 2)
    
    # Conta frequências manualmente para rótulos
    contagem_ambiente = {}
    for valor in atomos_ambiente:
        contagem_ambiente[valor] = contagem_ambiente.get(valor, 0) + 1
    
    # Cria o histograma
    n_ambiente, bins_ambiente, patches_ambiente = ax1.hist(
        atomos_ambiente, 
        bins=bins_ambiente, 
        alpha=0.7, 
        color='skyblue', 
        edgecolor='black',
        align='left'
    )
    
    ax1.set_xlabel('Número de Átomos no Ambiente')
    ax1.set_ylabel('Frequência')
    ax1.set_title('Distribuição de Átomos no Ambiente')
    ax1.grid(True, alpha=0.3)
    
    # Adiciona valores nas colunas
    for i, (retangulo, altura) in enumerate(zip(patches_ambiente, n_ambiente)):
        if altura > 0:  # Só mostra rótulo se houver valor
            ax1.text(
                retangulo.get_x() + retangulo.get_width() / 2,
                altura + max(n_ambiente)*0.01,
                f'{int(altura)}',
                ha='center',
                va='bottom',
                fontsize=9
            )
    
    # Adiciona média ao gráfico
    media_ambiente = np.mean(atomos_ambiente)
    ax1.axvline(media_ambiente, color='red', linestyle='--', linewidth=2, 
                label=f'Média: {media_ambiente:.2f}')
    
    # Adiciona linha no total máximo de átomos
    total_atomos = resultados[0]['total_atomos']
    ax1.axvline(total_atomos, color='green', linestyle=':', linewidth=2,
                label=f'Total átomos: {total_atomos}')
    
    ax1.legend()
    ax1.set_xticks(list(range(min(atomos_ambiente), max(atomos_ambiente) + 1)))
    
    # 2. Histograma da distribuição de átomos no tanque
    ax2 = axes[1]
    
    # Cria bins para o histograma
    bins_tank = range(min(atomos_tank), max(atomos_tank) + 2)
    
    # Conta frequências manualmente para rótulos
    contagem_tank = {}
    for valor in atomos_tank:
        contagem_tank[valor] = contagem_tank.get(valor, 0) + 1
    
    # Cria o histograma
    n_tank, bins_tank, patches_tank = ax2.hist(
        atomos_tank, 
        bins=bins_tank, 
        alpha=0.7, 
        color='lightcoral', 
        edgecolor='black',
        align='left'
    )
    
    ax2.set_xlabel('Número de Átomos no Tanque')
    ax2.set_ylabel('Frequência')
    ax2.set_title('Distribuição de Átomos no Tanque')
    ax2.grid(True, alpha=0.3)
    
    # Adiciona valores nas colunas
    for i, (retangulo, altura) in enumerate(zip(patches_tank, n_tank)):
        if altura > 0:  # Só mostra rótulo se houver valor
            ax2.text(
                retangulo.get_x() + retangulo.get_width() / 2,
                altura + max(n_tank)*0.01,
                f'{int(altura)}',
                ha='center',
                va='bottom',
                fontsize=9
            )
    
    # Adiciona média ao gráfico
    media_tank = np.mean(atomos_tank)
    ax2.axvline(media_tank, color='blue', linestyle='--', linewidth=2, 
                label=f'Média: {media_tank:.2f}')
    
    # Adiciona linha no total máximo de átomos
    ax2.axvline(total_atomos, color='green', linestyle=':', linewidth=2,
                label=f'Total átomos: {total_atomos}')
    
    ax2.legend()
    ax2.set_xticks(list(range(min(atomos_tank), max(atomos_tank) + 1)))
    
    # Estatísticas gerais
    stats_text = f"""
    Estatísticas Gerais ({len(resultados)} simulações):
    • Total de átomos por simulação: {total_atomos}
    • Média no ambiente: {media_ambiente:.2f} átomos ({media_ambiente/total_atomos*100:.1f}%)
    • Média no tanque: {media_tank:.2f} átomos ({media_tank/total_atomos*100:.1f}%)
    • Desvio padrão ambiente: {np.std(atomos_ambiente):.2f}
    • Desvio padrão tanque: {np.std(atomos_tank):.2f}
    • Moda ambiente: {max(contagem_ambiente, key=contagem_ambiente.get)} átomos
    • Moda tanque: {max(contagem_tank, key=contagem_tank.get)} átomos
    """
    
    # Adiciona texto com estatísticas
    plt.figtext(0.02, 0.02, stats_text, fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))
    
    plt.suptitle(f'Distribuição de Átomos após {n_movimentos} Movimentos\n' +
                f'(Baseado em {len(resultados)} simulações)', fontsize=14, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0.1, 1, 0.96])
    
    # Ajusta layout para garantir que tudo caiba
    plt.subplots_adjust(bottom=0.25)
    
    # Salva a figura
    plt.savefig('distribuicao_entropia_colunas.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Para rodar a animação individual:
    # roda_entropia()
    
    # Para rodar múltiplas simulações e criar gráficos:
    n_simulacoes = 1000  # Número de simulações a rodar
    resultados = roda_multiplas_simulacoes(n_simulacoes)
    plotar_resultados(resultados)