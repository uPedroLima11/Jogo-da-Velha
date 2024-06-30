import json
import os

def criar_tabuleiro():
    return [[" "] * 3 for _ in range(3)]

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" | ".join(linha))

def verificar_vencedor(tabuleiro, jogador):
    for linha in tabuleiro:
        if all(casa == jogador for casa in linha):
            return True

    for i in range(3):
        if all(tabuleiro[j][i] == jogador for j in range(3)):
            return True

    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == jogador:
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == jogador:
        return True

    return False

def imprimir_pontuacao(pontuacao):
    print("\nPontuação Atual:")
    for jogador, vitorias in pontuacao.items():
        print(f"{jogador}: {vitorias} vitória(s)")

def ler_pontuacao_arquivo(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return {}

def salvar_pontuacao_arquivo(arquivo, pontuacao):
    with open(arquivo, 'w') as f:
        json.dump(pontuacao, f)

def jogar_jogo_da_velha(pontuacao):
    tabuleiro = criar_tabuleiro()

    jogador1 = input("Jogador 1, digite seu nome: ")
    jogador2 = input("Jogador 2, digite seu nome: ")

    imprimir_tabuleiro(tabuleiro)

    print("**Caso os jogadores desejem sair da partida, basta digitar \"sair\".**")

    jogador_atual = jogador1
    simbolo_atual = "X"
    while True:
        print(f"Vez do jogador {jogador_atual}:")

        jogada = input("Digite sua jogada (linha, coluna) ou \"sair\": ")

        if jogada.lower() == "sair":
            print(f"Partida cancelada pelos jogadores {jogador1} e {jogador2}.")
            break

        linha, coluna = map(int, jogada.split(","))

        linha -= 1
        coluna -= 1

        if not (0 <= linha < 3 and 0 <= coluna < 3 and tabuleiro[linha][coluna] == " "):
            print("Jogada inválida. Tente novamente.")
            continue

        tabuleiro[linha][coluna] = simbolo_atual

        imprimir_tabuleiro(tabuleiro)

        if verificar_vencedor(tabuleiro, simbolo_atual):
            print(f"Jogador {jogador_atual} ({simbolo_atual}) venceu!")
            pontuacao[jogador_atual] = pontuacao.get(jogador_atual, 0) + 1
            break

        if all(all(x != " " for x in linha) for linha in tabuleiro):
            print("Empate!")
            break

        if jogador_atual == jogador1:
            jogador_atual = jogador2
            simbolo_atual = "O"
        else:
            jogador_atual = jogador1
            simbolo_atual = "X"

    imprimir_pontuacao(pontuacao)

    salvar_pontuacao_arquivo("pontuacao.json", pontuacao)

    jogar_novamente = input("Jogar novamente? (s/n): ")
    if jogar_novamente.lower() == "s":
        jogar_jogo_da_velha(pontuacao)

pontuacao = ler_pontuacao_arquivo("pontuacao.json")
jogar_jogo_da_velha(pontuacao)
