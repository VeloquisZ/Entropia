import random as rd
import turtle
import time

rd.seed()
Carro=int(input("tamanho do tanque do carro?minimo:3"))
Fora=int(input("tamanho da area externa?"))
passos=int(input("quantas vezes você quer repetir? preferencia multiplo de 100"))
# Variáveis de átomos
bolas = [[1,1],[1,2],[1,3],
         [2,1],[2,2],[2,3],
         [3,1],[3,2],[3,3]]

# Funções de validação de áreas
def area_do_carro(p):
    if p[0]<1 or p[0]>Carro:
        return False
    if p[1]<1 or p[1]>Carro:
        return False
    return True            

def area_do_ambiente(p):
    if p[0]<1 or p[0]>Fora:
        return False
    if p[1]<(-1*Fora) or p[1]>-1:
        return False
    return True            

def area_d_t(p):
    return p==[1,0]

def ocupado(p):
    return p not in bolas

def escolhe_bola():
    return rd.choice(bolas)

def escolhe_movimento():
    proxima_bola = escolhe_bola()
    dex = bolas.index(proxima_bola)
    se_moveu = 0
    
    para_cima = [proxima_bola[0]+1, proxima_bola[1]]
    para_baixo = [proxima_bola[0]-1, proxima_bola[1]]
    para_esq = [proxima_bola[0], proxima_bola[1]-1]
    para_dir = [proxima_bola[0], proxima_bola[1]+1]
    
    movimento = [para_cima, para_baixo, para_esq, para_dir]
    movimentar = rd.choice(movimento)
    
    if (area_do_carro(movimentar) or area_d_t(movimentar) or area_do_ambiente(movimentar)) and ocupado(movimentar):
        if proxima_bola == [1,1] and movimentar == [1,0]:
            if ocupado([1,-1]):
                se_moveu = 1
                bolas[dex] = [1,-1]
        elif proxima_bola == [1,-1] and movimentar == [1,0]:
            if ocupado([1,1]):
                se_moveu = -1
                bolas[dex] = [1,1]
        else:
            bolas[dex] = movimentar
    
    return se_moveu

def desenhar_grade():
    screen = turtle.Screen()
    screen.bgcolor("white")#Cord de fundo
    screen.title("Simulação de Movimento de Bolas")#Titulo
    screen.tracer(0)  # Deixa a animação mais suave
    
    # Configurar tartarugas
    grade_do_carro = turtle.Turtle()
    grade_de_fora = turtle.Turtle()
    grade_de_transição=turtle.Turtle()
    bolas_turtle = turtle.Turtle()
    carro_turtle= turtle.Turtle()
    
    # Configurar aparência
    for t in [carro_turtle,grade_do_carro, grade_de_fora,grade_de_transição,bolas_turtle]:#definição geral dos desenhos
        t.hideturtle()
        t.speed(0)
        t.pensize(2)
    
    # Desenhar grade do carro
    grade_do_carro.color("blue")
    grade_do_carro.penup()
    
    # Desenhar linhas do carro
    for i in range(Carro+1):
        y = i * 40
        grade_do_carro.goto(0, y)
        grade_do_carro.pendown()
        grade_do_carro.goto(((Carro)*40), y)
        grade_do_carro.penup()
    
    # Desenhar colunas do carro
    for i in range(Carro+1):
        x = i * 40
        grade_do_carro.goto(x, 0)
        grade_do_carro.pendown()
        grade_do_carro.goto(x, ((Carro)*40))
        grade_do_carro.penup()
    
    # Desenhar grade do exterior
    grade_de_fora.color("black")
    grade_de_fora.penup()
    
    # Desenhar linhas  do exterior
    for i in range(Fora+1):
        y = i * 40
        grade_de_fora.goto((-40), y)
        grade_de_fora.pendown()
        grade_de_fora.goto(((Fora+1)*-40), y)
        grade_de_fora.penup()
    
    # Desenhar colunas do exterior
    for i in range(Fora+1):
        x = (-i * 40)-40
        grade_de_fora.goto(x, 0)
        grade_de_fora.pendown()
        grade_de_fora.goto(x,((Fora)*40))
        grade_de_fora.penup()
        # Desenhar linhas da transição
    grade_de_transição.color("grey")
    grade_de_transição.penup()    
    for i in range(2):
        y = i * 40
        grade_de_transição.goto(0, y)
        grade_de_transição.pendown()
        grade_de_transição.goto(-40, y)
        grade_de_transição.penup()
    
    # Desenhar pontos de referência para o carro
    grade_pontos = turtle.Turtle()
    grade_pontos.hideturtle()
    grade_pontos.penup()
    for i in range(10):
        grade_pontos.goto(i * 50, -150)
        grade_pontos.dot(10, "black")
        grade_pontos.write(f"{i}", align="center", font=("Arial", 8, "normal"))

    # Adicionar rótulos
    grade_do_carro.goto(120, -50)
    grade_do_carro.write(f"Carro {Carro}X{Carro}", align="center", font=("Arial", 12, "bold"))
    
    grade_de_fora.goto(-250, -50)
    grade_de_fora.write(f"Exterior {Fora}X{Fora}", align="center", font=("Arial", 12, "bold"))
    
    grade_de_transição.goto(-20, -50)
    grade_de_transição.write("Transição (1x1)", align="center", font=("Arial", 12, "bold"))
    
    # Configurar tartaruga do carro
    carro_turtle.penup()
    carro_turtle.goto(0, -130)  # Posição inicial abaixo dos pontos
    carro_turtle.shape("turtle")
    carro_turtle.shapesize(2)  # Tamanho 50 (25 * 2)
    carro_turtle.color("green")
    carro_turtle.showturtle()
    
    return bolas_turtle, carro_turtle

def desenhar_bolas(bolas_turtle):
    bolas_turtle.clear()
    bolas_turtle.color("purple")
    
    for bola in bolas:
        linha, coluna = bola
        
        # Determinar posição baseada na localização da bola
        if coluna > 0:  # Dentro do carro
            x = (coluna - 1) * 40 + 20  # Centralizar na célula
            y = (linha - 1) * 40 + 20
        else:  # No exterior
            x = coluna * 40 - 20  # Ajustar posição para área externa
            y = (linha - 1) * 40 + 20
        
        bolas_turtle.penup()
        bolas_turtle.goto(x, y)
        bolas_turtle.pendown()
        bolas_turtle.dot(25)  # Tamanho das bolas

def animar_carro(carro_turtle, distancia_total):
    # calcular posição baseada na distância acumulada
    posicao = (distancia_total % 10) * 50
    # mostra a posição
    carro_turtle.goto(posicao, -130)

def animacao(passos, delay=0.1):
    bolas_turtle, carro_turtle = desenhar_grade()
    distancia_total = 0
    
    for i in range(passos):
        distancia_total += escolhe_movimento()
        desenhar_bolas(bolas_turtle)
        animar_carro(carro_turtle, distancia_total)
        turtle.update()  # Atualiza
        time.sleep(delay)
        
        #progresso a cada 100 passos
        if i % 100 == 0:
            print(f"Passo {i}, Distância acumulada: {distancia_total}")
    
    print(f"Simulação completa! Distância total: {distancia_total}")
    turtle.done()

# Executar a animação
if __name__ == "__main__":
    animacao(passos, delay=0.05)