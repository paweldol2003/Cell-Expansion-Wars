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


## Wymagania

środowisko Conda – plik `environment.yml` zawiera zależności

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

## Plany rozwoju

- Zapis/odczyt stanu gry
- Rozbudowany system AI (priorytety, taktyki)
- Tryb wieloetapowy z progresją trudności
- UI do edycji map i połączeń
- Pełne rozwinięcie graficzne 
