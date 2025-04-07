# Cell Expansion Wars
Paweł Dolak 193582
https://github.com/paweldol2003/Cell-Expansion-Wars.git

**Cell Expansion Wars** to strategiczna gra czasu rzeczywistego inspirowana mechaniką ekspansji komórek. Gracz kontroluje komórki, wysyła jednostki do zdobywania innych, a także musi mierzyć się z wrogiem sterowanym przez AI. Celem gry jest przejęcie wszystkich komórek przeciwnika.

## Funkcje

- **Sterowanie komórkami** gracza przy użyciu myszy
- **Animowane połączenia** i ruch jednostek między komórkami
- **Rundy turowe** – gracz i AI wykonują ruchy naprzemiennie co 5 sekund
- **Różne typy komórek**:
  - `normal` – standardowa komórka
  - `attack` – zwiększa siłę ofensywną
  - `defence` – zwiększa odporność na ataki
  - `hex` – specjalna komórka, może mieć 3 połączenia (inne tylko 2)
- **Strategiczne połączenia** – maksymalnie 2 dla zwykłych komórek, 3 dla `hex`
- **Menu kontekstowe** (PPM) umożliwiające usuwanie połączeń
- **Pulsujące efekty wizualne** wskazujące możliwe kierunki ataku
- **Przesuwanie planszy** za pomocą prawego przycisku myszy
- **Logger** z rotacją:
  - Wyświetla komunikaty na ekranie gry oraz w pliku logu
  - Ułatwia debugowanie i testowanie zachowania gry
- **System podpowiedzi strategicznych**:
  - Proponuje najlepszy ruch w turze gracza na podstawie analizy stanu planszy (pozostałe życie komórki)
  - Wyświetla sugestię graficznie (np. jako strzałkę)

## Sterowanie

- **LPM** – wybór komórki i wysyłanie jednostek (przeciąganie i łączenie poprzez kliknięcia myszą)
- **PPM na komórce** – otwarcie menu kontekstowego
- **PPM poza komórką + przeciąganie** – przesuwanie planszy
- **SPACJA** – włączenie/wyłączenie podpowiedzi



## Wymagania

środowisko Conda – plik `environment.yml` zawiera zależności

##Spełnione założenia

QGraphicsScene – implementacja sceny gry (1 pkt)
Dziedziczenie po QGraphicsItem – jednostki jako osobne obiekty (1 pkt)
Interaktywność jednostek – klikalność, przeciąganie, menu kontekstowe (3 pkt)
Sterowanie jednostkami – ruch na siatce planszy (1 pkt)
Zaciąganie grafik jednostek z pliku .rc (1 pkt)
Podświetlanie możliwych ruchów i ataków w zależności od mnożnika (2 pkt)
System walki uwzględniający poziomy, mnożenie jednostek  (2 pkt)
Mechanizm tur i licznik czasu na wykonanie ruchu (zegar rundowy) (2 pkt)
System podpowiedzi strategicznych oparty na AI (np. najlepszy ruch w turze) (1 pkt)
Logger wyświetlający komunikaty na konsoli i w interfejsie QTextEdit z rotującym logowaniem (1 pkt)

##Spełnione założenia z laboratorium Config & history

Tryb gry: 1 gracz / 2 graczy lokalnie / gra sieciowa (grupa radio buttons) – 0.5 pkt
Adres IP i port (line edit z maską, walidacją i podpowiedzią) – 0.5 pkt
Zapis i odczyt historii gry  (XML) – 1 pkt
Zapis i odczyt historii  gry (JSON) – 1 pkt

## Uruchomienie

```bash
python main.py
```

## Struktura projektu

- `main.py` – punkt startowy gry
- `game_scene.py` – główna scena gry
- `cell.py` – definicja komórki i jej właściwości
- `animated_connection.py` – animacje połączeń i jednostek
- `enemyAI.py` – prosta sztuczna inteligencja sterująca przeciwnikiem
- `stages.py` – definicje poziomów
- `menu_scene.py` – ekran menu
- `logger.py` – system logowania z rotacją
- `resources.py` zawiera zakodowane grafiki .png
- `suggestion_handler.py` - przeniesiony system sugestii
- `game_saver.py`,`game_loader.py` - obsługa zapisu


## Plany rozwoju

- Rozbudowany system AI (priorytety, taktyki)
- Tryb wieloetapowy z progresją trudności
- UI do edycji map i połączeń
- Pełne rozwinięcie graficzne 
