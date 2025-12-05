import random

class Nim:

    def __init__(self, initial = [1, 3, 5, 7]):
        
        '''
            Initialize game board. 
            Each game board has
                - 'piles'  : a list of how many elements remain in each pile
                - 'player' : 0 or 1 to indicate which player's turn
                - 'winner' : None, 0, or 1 to indicate who the winner is
        '''
        
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):

        '''
            self.avaiable_actions(piles) takes a 'piles' list as input and returns all of the avaiable actions '(i, j)' in that state. Action '(i, j)' represents the action of removing 'j' items from pile 'i'.
        '''
        # cria uma lista de movimentos
        moves = []
        for i, pile in enumerate(piles): # verifo para cada pilha a quantidade que há na pilha
            for remove in range(1, pile + 1): #ando na pilha lecionada
                moves.append((i, remove)) # adciono no moves uma tupla contendo o qualpilha, quantos remover
        return moves # retorna movimentos
        
    
    @classmethod
    def other_player(cls, player):

        '''
            self.other_player(player) returns the playe that is not 'player'. Assumes 'player' is either 0 or 1.
        '''
        return 0 if player == 1 else 1
    
    def switch_player(self):

        '''
            Switch the current player to the other player.
        '''
        self.player = Nim.other_player(self.player)

    def move(self, action):

        '''
            Make the move 'action' for the current player. 'action' must be a tuple '(i, j)'.
        '''
        pile, count = action  # separo a tupla em 2 tipos sendo a pilha e quantidade
        if action in self.available_actions(self.piles) : # verifico se é um movimento valido
            self.piles[pile] -= count  #removo da pilha que eu quero a quantidade que é valida
            if all(p == 0 for p in self.piles):   # verifico se a pilha não está vazia
                self.winner = Nim.other_player(self.player) # se estiver dou a vitoria ao outro jogador
                return # retorno para fechar o jogo
            self.switch_player() # caso a pilha não esteja vazia eu mudo para o proximo jogador
        else:
            raise ValueError("Movimento não valido!") #eu lanço um erro caso não seja um movimento valido
        

class AlphaBetaPrunning:
    def choose_action(self, state, depth, alpha, beta):
        def minimax(state, depth, alpha, beta, is_maximizing):
            # Se atingir a profundidade máxima ou o estado final, retorna a avaliação do estado
            if depth == 0 or self.is_terminal(state):
                return self.evaluate(state)
            
            # Caso seja o jogador maximizador
            if is_maximizing:
                max_eval = float('-inf') # pego o menor valor possível
                for action in Nim.available_actions(state): # veerico as listas de ações possíveis
                    new_state = self.result(state, action) # crio um novo estado com a jogada
                    eval = minimax(new_state, depth - 1, alpha, beta, False) # vou para a proxima jogada
                    max_eval = max(max_eval, eval)  
                    alpha = max(alpha, eval)
                    if beta <= alpha:  # Caso o beta seja menor ou igual ao alpha, interrompo a busca
                        break 
                return max_eval  # retorno o maior valor gerado
            else:  # Caso seja o jogador minimizador
                min_eval = float('inf') # pego o maior numero possível
                for action in Nim.available_actions(state): # pego uma das possíveis ações
                    new_state = self.result(state, action) # faço essa jogada em uma copia de pilha
                    eval = minimax(new_state, depth - 1, alpha, beta, True) # vou para o priximo depth passando que é o menor valor possível
                    min_eval = min(min_eval, eval) # verifico se o resultado do eval vai ser o menor possível
                    beta = min(beta, eval) # beta reebe o menor valor
                    if beta <= alpha:  #  Caso o beta seja menor ou igual ao alpha, interrompo a busca
                        break
                return min_eval # retono o menor valor
            
        best_action = None  # Inicializa a melhor ação como nula
        best_value = float('-inf')  # Define o pior caso inicial como um valor muito baixo

        # Avalia todas as jogadas possíveis para escolher a melhor
        for action in Nim.available_actions(state):  
            new_state = self.result(state, action)  # Simula o estado após realizar a jogada
            eval = minimax(new_state, depth - 1, alpha, beta, False)  # Calcula a avaliação da jogada
            
            # Lógica para forçar o oponente a ficar com apenas uma peça
            eval += self.evaluate_position_forcing(state, action)

            # Se a avaliação da jogada for melhor que a melhor encontrada até agora, atualiza os valores
            if eval > best_value:  
                best_value = eval  # Atualiza a melhor pontuação encontrada
                best_action = action  # Define essa ação como a melhor opção até o momento
                alpha = max(alpha, best_value)  # Atualiza o valor de alpha para a poda alfa-beta

        # Retorna a melhor ação encontrada ou uma aleatória caso nenhuma tenha sido escolhida
        return best_action if best_action else random.choice(Nim.available_actions(state))
        
    def is_terminal(self, state):
        # Verifica se todas as pilhas estão vazias, ou seja, se o jogo acabou
        return all(p == 0 for p in state)

    def evaluate_position_forcing(self, state, action):
        """
        A função tenta forçar a IA a deixar o oponente com apenas uma peça.
        """
        new_state = self.result(state, action)
        # Checar se o novo estado deixa o oponente com 1 peça.
        for idx, pile in enumerate(new_state):
            if pile == 1:  # Se a pilha tem 1 peça, é um bom alvo para forçar o oponente a ficar com 1 peça.
                return 1  # Recompensa a IA por forçar o oponente a jogar 1 peça.
        return 0  # Não mudou a situação para forçar o oponente.

    def evaluate(self, state):
        # Calcula a avaliação do estado usando o XOR das pilhas
        result = 0  
        for pile in state:
            result ^= pile  # Aplica a operação XOR acumulativa para calcular o Nim-sum

        # Se o resultado for 0, o oponente está em uma posição vencedora
        if result == 0:
            return -1  # Perdedora
        else:
            return 1  # Vencedora


    def result(self, state, action):
        # Retorna um novo estado após aplicar a ação escolhida
        pile, count = action # Separo o action em pilha e quantidade
        new_state = state.copy() # crio uma cópia da pilha
        new_state[pile] -= count # eu subtraio na pilha cópia a quantidade que eu quero
        return new_state #retorno a pilha cópia





def play(ai, human = None):

    # if no player order set, chose human's order randomly
    if human is None:
        human = 0 if random.uniform(0, 1) < 0.5 else 1

    # create new game
    game = Nim()
    
    
    # Definir valores 
    depth = 70
    alpha = float('-inf')  # Melhor valor encontrado para o maximizador
    beta = float('inf')  # Melhor valor encontrado para o minimizador

    while True:

        # print contents of piles
        for i, pile in enumerate(game.piles):
            print(f'Pile {i} : {pile}')

        # compute avaiable actions
        avaiable_actions = Nim.available_actions(game.piles)

        # let human make a move
        if game.player == human:
            print('Your turn')
            while True:
                pile, count = map(int, input('Choose a pile and count: ').split())
                if (pile, count) in avaiable_actions:
                    break
                print('Invalid move, try again')
        # have AI make a move
        else:
            print('AI turn')
            pile, count = ai.choose_action(game.piles, depth, alpha, beta)
            print(f'AI chose to take {count} from pile {pile}.')

        # make move
        game.move((pile, count))

        # check the winner
        if game.winner is not None:
            print('GAME OVER')
            winner = 'Human' if game.winner == human else 'AI'
            print(f'Winner is {winner}')
            break


play(AlphaBetaPrunning()) 
