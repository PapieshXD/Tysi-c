import random

class Card:
    def __init__(self, value, suit, game_value):
        self.value = value
        self.suit = suit
        self.game_value = game_value

    def __repr__(self):
        return f"{self.value} {self.suit}"

suits = ["karo", "kier", "trefl", "pik"]
values = ['9', '10', 'Walet', 'Dama', 'Król', 'As']
game_values = {'9': 0, '10': 10, 'Walet': 2, 'Dama': 3, 'Król': 4, 'As': 11}

cards = [Card(value, suit, game_values[value]) for suit in suits for value in values]

class Pile_of_cards:
    def __init__(self):
        self.hand = []
        
    def add_card_to_hand(self, num):
        for _ in range(num):
            if cards:
                self.hand.append(cards.pop(0))
                
    def show_hand(self):
        return self.hand

class Player(Pile_of_cards):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.points = 0
        self.bid = 0
        self.fold = False
        self.deklarowane_punkty = 0

    def __repr__(self):
        return f"Player({self.name}, Hand: {self.hand}, Points: {self.points}, Bid: {self.bid}, Fold: {self.fold})"
        
def meld(self):
    melds = {"pik": 40, "trefl": 60, "karo": 80, "kier": 100}
    for suit, meld_value in melds.items():
        if any(card.value == "Król" and card.suit == suit for card in self.hand) and \
           any(card.value == "Dama" and card.suit == suit for card in self.hand):
            print(f"{self.name} melduje {meld_value} ({suit})")
            self.points += meld_value
            return suit
    return None

def rozdawanie_kart(gracze_lista, ilosc_kart, czy_kupka, ilosc_kart_kupka):
    if not cards:
        print("Brak kart do rozdania. Koniec gry.")
        return None

    random.shuffle(cards)
    for gracz in gracze_lista:
        gracz.add_card_to_hand(ilosc_kart)

    if czy_kupka:
        kupka = Pile_of_cards()
        kupka.add_card_to_hand(ilosc_kart_kupka)
        return kupka

    return None

def licytacja(gracze_lista):
    licytacja_wartosc = 100
    for i in range(len(gracze_lista)):
        gracze_lista[i].bid = licytacja_wartosc
    gracze_lista[0].bid += 1 
    print(gracze_lista[0].name, "rozpoczyna licytację od", licytacja_wartosc)

    while True:
        for gracz in gracze_lista:
            if gracz.fold:
                continue

            print(gracz.name, "Twoje karty:", gracz.show_hand())
            
            decyzja = input("Czy przebijasz? (tak/nie) ").lower()
            if decyzja == "tak":
                while True:
                    try:
                        przebicie = int(input("O ile przebijasz? "))
                        if przebicie <= 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("Podaj poprawną wartość.")
                gracz.bid += przebicie
                licytacja_wartosc += przebicie
                print(gracz.bid)
            elif decyzja == "nie":
                gracz.fold = True
                print(f"{gracz.name} pasuje")
            else:
                print("Nieprawidłowa odpowiedź. Spróbuj ponownie.")
            
            print("Aktualna wartość licytacji:", licytacja_wartosc)
            aktywni_gracze = [gr for gr in gracze_lista if not gr.fold]
            
            if len(aktywni_gracze) == 1:
                zwyciezca = aktywni_gracze[0]
                print(zwyciezca.name, "wygrywa licytację")
                return zwyciezca

def next_person():
    print("\n" * 50)

def show_playable_cards(hand):
    print("Karty do zagrania:")
    for idx, card in enumerate(hand):
        print(f"{idx}: {card}")

def show_discardable_cards(hand):
    print("Karty do odrzucenia:")
    for idx, card in enumerate(hand):
        print(f"{idx}: {card}")

def obsluga_musika(gracz, kupka, liczba_graczy, gracze_lista):
    print("Musik:", kupka.show_hand())
    if liczba_graczy == 2:
        wybor = int(input("Wybierz 1 lub 2 stos kart: ")) - 1
        wybrane_karty = kupka.hand[wybor*2: (wybor+1)*2]
        gracz.hand.extend(wybrane_karty)
        odrzucone_karty = kupka.hand[(1-wybor)*2: (2-wybor)*2]
        print("Odrzucone karty:", odrzucone_karty)
    else:
        gracz.hand.extend(kupka.hand)
        print("Gracz zabiera musik.")
    while len(gracz.hand) > 7:
        show_discardable_cards(gracz.hand)
        while True:
            try:
                odrzucana_karta = int(input(f"Masz {len(gracz.hand)} kart, wybierz którą odrzucić (0-{len(gracz.hand)-1}): "))
                if odrzucana_karta < 0 or odrzucana_karta >= len(gracz.hand):
                    raise ValueError
                break
            except ValueError:
                print("Podaj poprawny numer karty.")
        gracz.hand.pop(odrzucana_karta)

def deklaracja_punktow(gracz):
    while True:
        try:
            deklaracja = int(input(f"{gracz.name}, zadeklaruj liczbę punktów, którą zamierzasz zdobyć: "))
            if deklaracja >= gracz.bid and deklaracja % 10 == 0:
                gracz.deklarowane_punkty = deklaracja
                print(f"{gracz.name} zadeklarował {deklaracja} punktów.")
                break
            else:
                print("Deklaracja musi być wielokrotnością 10 i nie może być mniejsza niż wylicytowana wartość.")
        except ValueError:
            print("Podaj poprawną wartość.")

def rozgrywka(gracz):
    while True:
        print(f"--- Runda {len(gracz.hand) + 1} ---")
        if not gracz.hand:
            print(f"{gracz.name} nie ma już kart.")
            break
        
        while True:
            try:
                zagrywana_karta = int(input(f"{gracz.name}, twoje karty: {gracz.hand}, wybierz kartę do zagrania (0-{len(gracz.hand)-1}): "))
                if zagrywana_karta < 0 or zagrywana_karta >= len(gracz.hand):
                    raise ValueError
                break
            except ValueError:
                print("Podaj poprawny numer karty.")
        karta = gracz.hand.pop(zagrywana_karta)
        print(f"{gracz.name} zagrywa {karta}")

        for przeciwnik in players:
            if przeciwnik != gracz and przeciwnik.hand:
                print(f"{przeciwnik.name}, twoje karty: {przeciwnik.show_hand()}")
                while True:
                    try:
                        zagrywana_karta_przeciwnika = int(input(f"{przeciwnik.name}, wybierz kartę do zagrania (0-{len(przeciwnik.hand)-1}): "))
                        if zagrywana_karta_przeciwnika < 0 or zagrywana_karta_przeciwnika >= len(przeciwnik.hand):
                            raise ValueError
                        break
                    except ValueError:
                        print("Podaj poprawny numer karty.")
                karta_przeciwnika = przeciwnik.hand.pop(zagrywana_karta_przeciwnika)
                print(f"{przeciwnik.name} zagrywa {karta_przeciwnika}")

                if karta.suit == karta_przeciwnika.suit:
                    if karta.game_value > karta_przeciwnika.game_value:
                        gracz.points += karta.game_value + karta_przeciwnika.game_value
                        print(f"{gracz.name} wygrywa rundę i zdobywa {karta.game_value + karta_przeciwnika.game_value} punktów.")
                    else:
                        przeciwnik.points += karta.game_value + karta_przeciwnika.game_value
                        print(f"{przeciwnik.name} wygrywa rundę i zdobywa {karta.game_value + karta_przeciwnika.game_value} punktów.")
                else:
                    if karta.suit == "kier" or karta_przeciwnika.suit == "kier":
                        if karta.suit == "kier":
                            gracz.points += karta.game_value + karta_przeciwnika.game_value
                            print(f"{gracz.name} wygrywa rundę i zdobywa {karta.game_value + karta_przeciwnika.game_value} punktów.")
                        else:
                            przeciwnik.points += karta.game_value + karta_przeciwnika.game_value
                            print(f"{przeciwnik.name} wygrywa rundę i zdobywa {karta.game_value + karta_przeciwnika.game_value} punktów.")
                    else:
                        print("Runda kończy się remisem.")

        print(f"Stan punktów po rundzie {len(gracz.hand)}:")
        for player in players:
            print(f"{player.name}: {player.points} punktów")


        players_with_cards = [player for player in players if player.hand]
        if not players_with_cards:
            print("Brak kart do zagrania. Koniec gry.")
            break

    if players_with_cards:
        print("--- Koniec gry ---")
        for player in players:
            if player.points >= player.deklarowane_punkty:
                print(f"{player.name} zdobywa {player.points} punktów i spełnia swoją deklarację!")
            else:
                print(f"{player.name} zdobywa {player.points}, ale nie spełnia swojej deklaracji.")

        zwyciezca = max(players, key=lambda p: p.points)
        print(f"Zwycięzcą jest {zwyciezca.name} z {zwyciezca.points} punktami.")

def main():
    while True:
        print("=== Menu Główne ===")
        print("1. Gra 2-osobowa")
        print("2. Gra 3-osobowa")
        print("3. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == '3':
            break
        elif choice == '1':
            gra_dwuosobowa()
        elif choice == '2':
            gra_trzyosobowa()
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

def gra_dwuosobowa():
    global players
    player_1 = Player(input("Podaj nazwę pierwszego gracza: "))
    player_2 = Player(input("Podaj nazwę drugiego gracza: "))
    next_person()
    players = [player_1, player_2]
    random.shuffle(players)
    kupka = rozdawanie_kart(players, 8, 1, 4)
    obsluga_musika(players[0], kupka, 2, players)
    deklaracja_punktow(players[0])
    rozgrywka(players[0])

def gra_trzyosobowa():
    global players
    player_1 = Player(input("Podaj nazwę pierwszego gracza: "))
    player_2 = Player(input("Podaj nazwę drugiego gracza: "))
    player_3 = Player(input("Podaj nazwę trzeciego gracza: "))
    next_person()
    players = [player_1, player_2, player_3]
    random.shuffle(players)
    kupka = rozdawanie_kart(players, 7, 1, 3)
    zwyciezca = licytacja(players)
    obsluga_musika(zwyciezca, kupka, 3, players)
    deklaracja_punktow(zwyciezca)
    rozgrywka(zwyciezca)

main()
