import random


class Carta:
    naipes = ["♦️", "♠️", "♥️", "♣️"]
    forca_naipes = {"♦️": 1, "♠️": 2, "♥️": 3, "♣️": 4}

    def __init__(self, naipe, numero):
        self.naipe = naipe
        self.numero = numero
        self.label = self.numero

        if self.numero == 8:
            self.label = "Dama"
        if self.numero == 9:
            self.label = "Valete"
        if self.numero == 10:
            self.label = "Reis"
        if self.numero == 11:
            self.label = "Ás"
        if self.numero == 12:
            self.label = "2"
        if self.numero == 13:
            self.label = "3"

    def comparar(self, other, vira):
        if self.numero > other.numero:
            return 1
        elif self.numero < other.numero:
            return -1
        return 0

    def __str__(self):
        return f"{self.label} de {self.naipe}"

    def __eq__(self, other):
        if self.numero != other.numero:
            return False

        if self.naipe != other.naipe:
            return False

        return True


class Jogador:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
        self.cartas = []
        self.pontos = 0

    def venceu(self):
        return self.pontos >= 12

    def jogar(self):
        pass

    def __str__(self):
        retorno = f"Jogador {self.nome} tem {self.pontos} pontos: "
        for carta in self.cartas:
            retorno += carta.__str__() + " | "
        return retorno


class Jogador_Humano(Jogador):
    def jogar(self):
        print(self)
        indice = input(
            f"Qual índice de carta você deseja jogar (de 1 a {len(self.cartas)})?"
        )
        carta_escolhida = self.cartas[int(indice) - 1]
        del self.cartas[int(indice) - 1]
        return carta_escolhida


class Jogador_IA(Jogador):
    def __init__(self, id, nome):
        super().__init__(id, nome)

    def melhor_carta(self, cartas_disponiveis, carta_vira, carta_adversario=None):
        # Se a carta do adversário não foi jogada, então temos que escolher uma carta qualquer
        if not carta_adversario:
            return random.choice(cartas_disponiveis)

        cartas_possiveis = []
        for carta in cartas_disponiveis:
            # Se a carta do jogador é do mesmo naipe da carta vira, então só pode jogar cartas do mesmo naipe ou trunfo
            if carta.naipe == carta_vira.naipe:
                if (
                    carta.naipe == carta_adversario.naipe
                    and carta.numero > carta_adversario.numero
                ):
                    cartas_possiveis.append(carta)
                elif carta.naipe != carta_adversario.naipe:
                    cartas_possiveis.append(carta)
            # Se a carta do jogador não é do mesmo naipe da carta vira, então só pode jogar trunfo
            elif (
                carta.naipe == carta_vira.naipe
                and carta.numero > carta_adversario.numero
            ):
                cartas_possiveis.append(carta)

        # Se não há cartas possíveis, joga a de menor valor
        if not cartas_possiveis:
            return min(cartas_disponiveis, key=lambda x: x.numero)

        # Escolhe a carta de maior valor dentre as possíveis
        return max(cartas_possiveis, key=lambda x: x.numero)

    def jogar(self, rodada, ambiente):
        print(self)
        carta_escolhida = self.melhor_carta(
            self.cartas, ambiente.vira, ambiente.carta_turno
        )
        self.cartas.remove(carta_escolhida)
        print(f"IA => carta: {str(carta_escolhida)}")
        return carta_escolhida


class Rodada:
    def __init__(self, j1, j2):
        self.vira = None
        self.distribuir_cartas(j1, j2)
        print(f"Vira: {self.vira}")

    def distribuir_cartas(self, j1, j2):
        self.vira = Carta(random.choice(Carta.naipes), random.randint(4, 13))
        cartas_rodada = []
        while len(cartas_rodada) < 6:
            sorteada = Carta(random.choice(Carta.naipes), random.randint(4, 13))

            if (sorteada not in cartas_rodada) and (sorteada != self.vira):
                cartas_rodada.append(sorteada)

        j1.cartas = cartas_rodada[0:3]
        j2.cartas = cartas_rodada[3:6]

    def __str__(self):
        return f"Vira: {self.vira}"


class Ambiente:
    def __init__(
        self, vira, cartas_adversario, carta_turno, pontos_adversario, vencedores_turno
    ):
        self.vira = vira

        self.cartas_adversario = cartas_adversario

        self.carta_turno = carta_turno
        self.pontos_adversario = pontos_adversario

        self.vencedores_turno = vencedores_turno

        self.peso_rodada = 1
        self.mostrar_maior = False

    def __str__(self):
        vira = str(self.vira)
        cartas = ""
        for carta in self.cartas_adversario:
            cartas += str(carta) + " | "
        cturno = str(self.carta_turno)
        pontos = self.pontos_adversario
        return f"Ambiente: Vira: {vira} | Cartas adversário: {cartas} Mesa: {cturno} | Pontos adv: {pontos}"


class Jogo:
    def __init__(self):
        self.jogador_humano = Jogador_Humano(1, "Humano")
        self.jogador_ia = Jogador_IA(2, "IA")

        self.pontos_jogador_humano = 0
        self.pontos_jogador_ia = 0

    def jogar_rodada(self, rodada):
        carta_jogador_humano = self.jogador_humano.jogar()

        ambiente = Ambiente(
            rodada.vira,
            self.jogador_ia.cartas,
            carta_jogador_humano,
            self.pontos_jogador_ia,
            [],
        )

        carta_jogador_ia = self.jogador_ia.jogar(rodada, ambiente)

        resultado = carta_jogador_humano.comparar(carta_jogador_ia, rodada.vira)

        if resultado == 1:
            self.pontos_jogador_humano += 1
        elif resultado == -1:
            self.pontos_jogador_ia += 1

        print(f"Vira: {rodada.vira}")
        print(f"{self.jogador_humano.nome} jogou {carta_jogador_humano}")
        print(f"{self.jogador_ia.nome} jogou {carta_jogador_ia}")

        if resultado == 1:
            print(f"{self.jogador_humano.nome} ganhou a rodada")
        elif resultado == -1:
            print(f"{self.jogador_ia.nome} ganhou a rodada")
        else:
            print("Rodada empatada")

    def jogar(self):
        while not self.jogador_humano.venceu() and not self.jogador_ia.venceu():
            rodada = Rodada(self.jogador_humano, self.jogador_ia)
            self.jogar_rodada(rodada)
            print(
                f"{self.jogador_humano.nome} {self.pontos_jogador_humano} x {self.pontos_jogador_ia} {self.jogador_ia.nome}"
            )

        if self.jogador_humano.venceu():
            print(f"{self.jogador_humano.nome} venceu o jogo!")
        else:
            print(f"{self.jogador_ia.nome} venceu o jogo!")


jogo = Jogo()
jogo.jogar()
