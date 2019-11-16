from math import inf as infinity
from random import choice
import platform
import time
from os import system


# Caio Fábio Gomes Alves - 116119050
# Lucas Evangelista de Oliveira - 119121314


# Variáveis globais
HUMAN = -1
COMP = +1

# Tabuleiro
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0],]


#Função para avaliação heurística do estado
def evaluate(state):
    if vitoria(state, COMP):
        score = +1
    elif vitoria(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

#Posições de vitória
def vitoria(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

# Testa quem venceu o jogo
def FimDeJogo(state):
    return vitoria(state, HUMAN) or vitoria(state, COMP)

# Guarda os espaços vazios
def empty_cells(state):
    cells = []
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

# O movimento so é valido se posição estiver vazia
def movimento_valido(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

# Muda o movimento no tabuleiro, para o jogador atual
def set_move(x, y, player):
    if movimento_valido(x, y):
        board[x][y] = player
        return True
    else:
        return False


# Implementação do algoritmo Minimax
def minimax(state, depth, player):
  
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or FimDeJogo(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


#Limpa o console no Windows e Linux
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# Imprime o tabuleiro no console no estado atual
def render(state, c_choice, h_choice):

    chars = {-1: h_choice, +1: c_choice, 0: ' '}
    str_line = '###############'


    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)

# Se a profundidade for menor que 9, chama a função do MiniMax
def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or FimDeJogo(board):
        return

    clean()
    print(f'Aguarde o computador jogar [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or FimDeJogo(board):
        return

    # Dicionário de movimentos válidos
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Sua vez [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use números de 1 a 9! >>> '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Este campo já foi utilizado!')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('...')
            exit()
        except (KeyError, ValueError):
            print('Escolha invalida')

# Função principal
def main():

    # Limpa o console
    clean()
    print('*** Jogo da velha (Tic Tac Toe) com aplicação do algoritmo Minimax ***')
    # O valor das variáveis abaixo so pode ser X ou O
    h_choice = ''
    c_choice = ''
    # Usuario começa?
    first = ''

    # Usuário quem escolhe a letra
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Escolha X ou O\n>>> ').upper()
        except (EOFError, KeyboardInterrupt):
            print('...')
            exit()
        except (KeyError, ValueError):
            print('Exception: Escolha da letra')

    # Escolha oposta ao do usuário
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Usuário começa?
    clean()
    while first != 'S' and first != 'N':
        try:
            first = input('Você deseja começar?[s/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('...')
            exit()
        except (KeyError, ValueError):
            print('Exception: Escolha de quem começa')

    # Jogo em loop
    while len(empty_cells(board)) > 0 and not FimDeJogo(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Printa resultado do jogo
    if vitoria(board, HUMAN):
        clean()
        print(f'Sua vez [{h_choice}]')
        render(board, c_choice, h_choice)
        print('\nVocê venceu! :)')
    elif vitoria(board, COMP):
        clean()
        print(f'Aguarde o computador jogar [{c_choice}]')
        render(board, c_choice, h_choice)
        print('\nVocê perdeu! :(')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('\nEmpate! :o')
    exit()


if __name__ == '__main__':
    main()
