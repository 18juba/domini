import random
import matplotlib.pyplot as plt
from collections import deque
import os

def limpar_terminal():
    sistema = os.name
    if sistema == 'posix':
        os.system('clear')
    elif sistema == 'nt':
        os.system('cls')

class Peca:
    def __init__(self, v1, v2):
        self.__valor1 = v1
        self.__valor2 = v2
    
    def obter_valor1(self):
        return self.__valor1
    
    def obter_valor2(self):
        return self.__valor2
    
    def obter_valor(self):
        return self.__valor1 + self.__valor2

    def __str__(self):
        return f"[{self.__valor1}|{self.__valor2}]"

class Conjunto:
    def __init__(self):
        self.__pecas = []
        for i in range(7):
            for j in range(i, 7):
                self.__pecas.append(Peca(i, j))
    
    def embaralhar(self):
        random.shuffle(self.__pecas)
    
    def comprar(self):
        if self.__pecas:
            return self.__pecas.pop()
        else:
            return None
    
    def obter_pecas(self):
        return self.__pecas

class Tabuleiro:
    def __init__(self):
        self.__pecas = deque()
        self.__extremo_esquerdo = None
        self.__extremo_direito = None
    
    def obter_extremo_esquerdo(self):
        return self.__extremo_esquerdo
    
    def obter_extremo_direito(self):
        return self.__extremo_direito
    
    def obter_pecas(self):
        return self.__pecas
    
    def esta_vazio(self):
        return len(self.__pecas) == 0
    
    def colocar_peca(self, peca, lado):
        if self.esta_vazio():
            self.__pecas.append(peca)
            self.__extremo_esquerdo = peca.obter_valor1()
            self.__extremo_direito = peca.obter_valor2()
        else:
            if lado == 'esquerda':
                if peca.obter_valor1() == self.__extremo_esquerdo:
                    novo_valor = peca.obter_valor2()
                elif peca.obter_valor2() == self.__extremo_esquerdo:
                    novo_valor = peca.obter_valor1()
                else:
                    novo_valor = self.__extremo_esquerdo
                self.__pecas.appendleft(peca)
                self.__extremo_esquerdo = novo_valor
            elif lado == 'direita':
                if peca.obter_valor1() == self.__extremo_direito:
                    novo_valor = peca.obter_valor2()
                elif peca.obter_valor2() == self.__extremo_direito:
                    novo_valor = peca.obter_valor1()
                else:
                    novo_valor = self.__extremo_direito
                self.__pecas.append(peca)
                self.__extremo_direito = novo_valor

    def __str__(self):
        return ' '.join(str(p) for p in self.__pecas)

def soma_pontos(mao):
    return sum(peca.obter_valor() for peca in mao)

class Jogador:
    def __init__(self, nome):
        self.__nome = nome
        self.__mao = []
    
    def obter_mao(self):
        return self.__mao

    def adicionar_peca(self, peca):
        self.__mao.append(peca)
    
    def remover_peca(self, peca):
        self.__mao.remove(peca)

    def nome(self):
        return self.__nome

    def escolher_jogada(self, jogadas_possiveis):
        raise NotImplementedError
    
    def jogar(self, tabuleiro, estoque):
        jogadas = []
        if tabuleiro.esta_vazio():
            for peca in self.__mao:
                jogadas.append((peca, 'direita'))
        else:
            for peca in self.__mao:
                lados_validos = []
                if self.jogavel(peca, tabuleiro.obter_extremo_esquerdo()):
                    lados_validos.append('esquerda')
                if self.jogavel(peca, tabuleiro.obter_extremo_direito()):
                    lados_validos.append('direita')
                if lados_validos:
                    for lado in lados_validos:
                        jogadas.append((peca, lado))
        
        if jogadas:
            escolha = self.escolher_jogada(jogadas)
            if escolha:
                peca_jogada, lado = escolha
                self.remover_peca(peca_jogada)
                return escolha
        
        while True:
            peca_comprada = estoque.comprar()
            if peca_comprada is None:
                return None
            self.adicionar_peca(peca_comprada)
            lados_validos = []
            if tabuleiro.esta_vazio():
                lados_validos.append('direita')
            else:
                if self.jogavel(peca_comprada, tabuleiro.obter_extremo_esquerdo()):
                    lados_validos.append('esquerda')
                if self.jogavel(peca_comprada, tabuleiro.obter_extremo_direito()):
                    lados_validos.append('direita')
            if lados_validos:
                self.remover_peca(peca_comprada)
                return (peca_comprada, lados_validos[0])
    
    def jogavel(self, peca, extremo):
        return peca.obter_valor1() == extremo or peca.obter_valor2() == extremo

class Humano(Jogador):
    def escolher_jogada(self, jogadas_possiveis):
        print("\nSua mão:")
        for i, peca in enumerate(self.obter_mao()):
            print(f"{i}: {peca}")

        if not jogadas_possiveis:
            print("Nenhuma jogada possível. Você precisa comprar uma peça.")
            return None
        
        print("\nJogadas possíveis:")
        for i, (peca, lado) in enumerate(jogadas_possiveis):
            print(f"{i}: {peca} -> {lado}")

        while True:
            escolha = input("\nEscolha uma jogada pelo número (ou 'p' para comprar): ")
            if escolha.lower() == 'p':
                return None
            if escolha.isdigit():
                escolha = int(escolha)
                if 0 <= escolha < len(jogadas_possiveis):
                    return jogadas_possiveis[escolha]
            print("Escolha inválida. Tente novamente.")

class ComputadorAleatorio(Jogador):
    def escolher_jogada(self, jogadas_possiveis):
        return random.choice(jogadas_possiveis)

class ComputadorInteligente(Jogador):
    def escolher_jogada(self, jogadas_possiveis):
        melhor_jogada = None
        melhor_valor = -1
        for jogada in jogadas_possiveis:
            peca = jogada[0]
            valor_peca = peca.obter_valor()
            if valor_peca > melhor_valor:
                melhor_valor = valor_peca
                melhor_jogada = jogada
        return melhor_jogada

class Placar:
    def __init__(self):
        self.__jogadores = []
    
    def obter_jogadores(self):
        return self.__jogadores

    def adicionar_jogador(self, jogador):
        self.__jogadores.append(jogador)

    def obter_pontos(self, jogador):
        return self.__jogadores.index(jogador)

class Jogo:
    def __init__(self, jogador1, jogador2):
        self.__jogador1 = jogador1
        self.__jogador2 = jogador2
        self.__pontos = {jogador1.nome(): 0, jogador2.nome(): 0}
    
    def obter_jogador1(self):
        return self.__jogador1
    
    def obter_jogador2(self):
        return self.__jogador2
    
    def obter_pontos(self):
        return self.__pontos

    def distribuir_pecas(self, estoque):
        for _ in range(7):
            self.__jogador1.adicionar_peca(estoque.comprar())
            self.__jogador2.adicionar_peca(estoque.comprar())
    
    def jogar_rodada(self):
        estoque = Conjunto()
        estoque.embaralhar()
        self.__jogador1._Jogador__mao = []
        self.__jogador2._Jogador__mao = []
        self.distribuir_pecas(estoque)
        tabuleiro = Tabuleiro()
        turno = random.choice([0, 1])
        passes_consecutivos = 0
        tem_humano = isinstance(self.__jogador1, Humano) or isinstance(self.__jogador2, Humano)

        while True:
            if turno == 0:
                jogador_atual = self.__jogador1
                adversario = self.__jogador2
            else:
                jogador_atual = self.__jogador2
                adversario = self.__jogador1
            
            if tem_humano:
                limpar_terminal()
                print("\nTabuleiro atual:")
                if not tabuleiro.esta_vazio():
                    print(tabuleiro)
                else:
                    print("[Tabuleiro vazio]")
                print(f"\nVez de: {jogador_atual.nome().upper()}")
                if isinstance(jogador_atual, Humano):
                    input("Pressione Enter para continuar...")
            
            jogada = jogador_atual.jogar(tabuleiro, estoque)
            if jogada is not None:
                peca, lado = jogada
                tabuleiro.colocar_peca(peca, lado)
                passes_consecutivos = 0
                
                if tem_humano:
                    print(f"\n{jogador_atual.nome()} jogou {peca} no lado {lado}")
                    if isinstance(adversario, Humano):
                        input("Pressione Enter para continuar...")
            else:
                passes_consecutivos += 1
                if tem_humano:
                    print(f"\n{jogador_atual.nome()} passou a vez!")
                if passes_consecutivos >= 2:
                    pontos_jogador = soma_pontos(jogador_atual.obter_mao())
                    pontos_adversario = soma_pontos(adversario.obter_mao())
                    if pontos_jogador < pontos_adversario:
                        return jogador_atual, pontos_adversario
                    elif pontos_adversario < pontos_jogador:
                        return adversario, pontos_jogador
                    else:
                        return None, 0
            
            if len(jogador_atual.obter_mao()) == 0:
                if tem_humano:
                    print(f"\n{jogador_atual.nome()} ganhou a rodada!")
                pontos = soma_pontos(adversario.obter_mao())
                return jogador_atual, pontos
            
            turno = 1 - turno

    def jogar_partida(self):
        tem_humano = isinstance(self.__jogador1, Humano) or isinstance(self.__jogador2, Humano)
        while max(self.__pontos.values()) < 100:
            vencedor, pontos_rodada = self.jogar_rodada()
            if vencedor is not None:
                self.__pontos[vencedor.nome()] += pontos_rodada
                if tem_humano:
                    print(f"\nPlacar atual:")
                    for jogador, pontos in self.__pontos.items():
                        print(f"{jogador}: {pontos} pontos")
                    input("\nPressione Enter para continuar...")
                    limpar_terminal()
            
            if max(self.__pontos.values()) >= 100:
                break
        
        if self.__pontos[self.__jogador1.nome()] >= 100:
            return self.__jogador1, self.__pontos
        else:
            return self.__jogador2, self.__pontos

def simular_partidas(num_partidas):
    __resultados_Aleatorio = []
    __resultados_Inteligente = []
    __partidas = []
    __total_Aleatorio = 0
    __total_Inteligente = 0

    for i in range(1, num_partidas + 1):
        jogador_Aleatorio = ComputadorAleatorio("Neymar")
        jogador_Inteligente = ComputadorInteligente("Computador Inteligente")
        jogo = Jogo(jogador_Aleatorio, jogador_Inteligente)
        vencedor, placar_final = jogo.jogar_partida()
        if vencedor is not None:
            if vencedor.nome() == "Neymar":
                __total_Aleatorio += 1
            elif vencedor.nome() == "Computador Inteligente":
                __total_Inteligente += 1
        __partidas.append(i)
        __resultados_Aleatorio.append(__total_Aleatorio)
        __resultados_Inteligente.append(__total_Inteligente)
    
    plt.plot(__partidas, __resultados_Aleatorio, label="Neymar", color="blue", linestyle="solid")
    plt.plot(__partidas, __resultados_Inteligente, label="Computador Inteligente", color="red", linestyle="solid")
    plt.xlabel("Partidas")
    plt.ylabel("Vitórias")
    plt.title("Evolução dos resultados nas simulações")
    plt.legend()
    plt.show()

# =============================================================================
# Execução principal: permite jogar ou simular partidas.
# =============================================================================

rodando = True

while rodando:
    print("Dominó")
    print("Deseja jogar contra a máquina ou simular partidas ?")
    selecao = int(input("1 para jogar, 2 para simular partidas: "))

    if selecao == 1:
        nome = input("Digite seu nome: ")
        jogador_humano = Humano(nome)
        print("Qual adversário você quer enfrentar ?")
        dificuldade = int(input("1 - Neymar \n2 - Computador Inteligente:\n"))
        while dificuldade not in [1, 2]:
            dificuldade = int(input("Escolha uma opção válida (1 ou 2): "))
        if dificuldade == 1:
            jogador_maquina = ComputadorAleatorio("Neymar")
        else:
            jogador_maquina = ComputadorInteligente("Computador Inteligente")
        jogo = Jogo(jogador_humano, jogador_maquina)

        vencedor, placar_final = jogo.jogar_partida()

        print("\nFim da partida!")
        print(f"Placar final: {placar_final}")
        print(f"Vencedor: {vencedor.nome()}" if vencedor else "Empate!")
    elif selecao == 2:
        num_partidas = int(input("Digite o número de partidas: "))
        simular_partidas(num_partidas)
    
    finalizar = input("Deseja finalizar o jogo ? (S/N): ")
    if finalizar.lower() == 's':
        limpar_terminal()
        print("Obrigado por jogar!")
        rodando = False
        continue
    
    limpar_terminal()