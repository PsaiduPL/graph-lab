|     |     |     | Przykładowe |     |     |     | wejście | – zestaw | 4.  |
| --- | --- | --- | ----------- | --- | --- | --- | ------- | -------- | --- |
Cały program może wykonywać wszystkie zadania dla jednego wylosowanego grafu: najpierw losu-
jemy digraf (zad. 1), potem sprawdzamy, czy jest silnie spójny (zad. 2). Jeśli tak, to losujemy wagi
| i wywołujemy |            | algorytm   | Johnsona     |     | (zad.    | 3 + 4). |     |     |     |
| ------------ | ---------- | ---------- | ------------ | --- | -------- | ------- | --- | --- | --- |
| Ad. 1.       | Skierowany |            | graf losowy  |     |          |         |     |     |     |
|              | Dane       | wejściowe: |              |     |          |         |     |     |     |
|              | •          | n – liczba | wierzchołków |     | digrafu, |         |     |     |     |
• p – prawdopodobieństwo, że pomiędzy dwoma wierzchołkami istnieje krawędź skierowana.
Wyjście programu: dowolna reprezentacja grafu (np. jak na rys. 1. lub listingach 1., 2., 3.).
3
2
3
-5
6
9
4
6
|     |     |     | 1   |     | 2   | 5   | 4   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 10  |     | -4  |     | 9   |     |
7
4
-1
|     |     |     |     |     |     | 4   |     | -4  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
5
Rysunek 1: Dane wyjściowe: przykładowy losowy digraf o siedmiu wierzchołkach.
|     | 1.  | 2 3 5 |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
1
|     | 2.  | 1 3 4 | 5 7 |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
2
|     | 3.  | 6   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3
| 4   | 4.  | 2 7   |         |          |            |     |       |              |           |
| --- | --- | ----- | ------- | -------- | ---------- | --- | ----- | ------------ | --------- |
| 5   | 5.  | 7     |         |          |            |     |       |              |           |
| 6   | 6.  | 2     |         |          |            |     |       |              |           |
| 7   | 7.  | 6     |         |          |            |     |       |              |           |
|     |     |       | Listing | 1: Lista | sąsiedztwa |     | grafu | skierowanego | z rys. 1. |
| 1   | 0 1 | 1 0 1 | 0 0     |          |            |     |       |              |           |
|     | 1 0 | 1 1 1 | 0 1     |          |            |     |       |              |           |
2
|     | 0 0 | 0 0 0 | 1 0 |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
3
| 4   | 0 1 | 0 0 0 | 0 1     |            |     |            |     |                    |           |
| --- | --- | ----- | ------- | ---------- | --- | ---------- | --- | ------------------ | --------- |
| 5   | 0 0 | 0 0 0 | 0 1     |            |     |            |     |                    |           |
| 6   | 0 1 | 0 0 0 | 0 0     |            |     |            |     |                    |           |
| 7   | 0 0 | 0 0 0 | 1 0     |            |     |            |     |                    |           |
|     |     |       | Listing | 2: Macierz |     | sąsiedztwa |     | grafu skierowanego | z rys. 1. |
1

| 1 -1 -1 | -1  | 1 0   | 0   | 0 0 | 0    | 0   | 0 0 | 0 0 |     |
| ------- | --- | ----- | --- | --- | ---- | --- | --- | --- | --- |
| 1 0     | 0   | -1 -1 | -1  | -1  | -1 0 | 1   | 0 0 | 1 0 |     |
2
| 0 1 | 0   | 0 1 | 0   | 0 0 | -1  | 0   | 0 0 | 0 0 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3
| 0 0 | 0   | 0 0 | 1   | 0 0 | 0   | -1  | -1 0 | 0 0 |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
4
| 5 0 0 | 1   | 0 0     | 0          | 1 0 | 0          | 0   | 0 -1  | 0 0          |           |
| ----- | --- | ------- | ---------- | --- | ---------- | --- | ----- | ------------ | --------- |
| 6 0 0 | 0   | 0 0     | 0          | 0 0 | 1          | 0   | 0 0   | -1 1         |           |
| 7 0 0 | 0   | 0 0     | 0          | 0 1 | 0          | 0   | 1 1   | 0 -1         |           |
|       |     | Listing | 3: Macierz |     | incydencji |     | grafu | skierowanego | z rys. 1. |
Ad. 2. Algorytm Kosaraju (oznaczanie silnie spójnych składowych)
| Dane | wejściowe: | digraf | z   | 1. zadania. |     |     |     |     |     |
| ---- | ---------- | ------ | --- | ----------- | --- | --- | --- | --- | --- |
Wyjście programu:dowolnysposób,np.wypisaniewierzchołkównależącychdoposzczególnych
składowych (przykładowy graf z rys. 1. ma tylko jedną silnie spójną składową ⇒ jest silnie
spójny).
Ad. 3, 4. Losowy silnie spójny digraf z wagami, algorytm Bellmana-Forda, algorytm Johnsona
| Dane | wejściowe: | digraf | z   | 1. zadania. |     |     |     |     |     |
| ---- | ---------- | ------ | --- | ----------- | --- | --- | --- | --- | --- |
Wyjście programu: dowolna reprezentacja grafu z losowymi wagami (np. wizualizacja: rys. 2)
| oraz macierz |     | odległości |     | (przykład: | listing | 4). |     |     |     |
| ------------ | --- | ---------- | --- | ---------- | ------- | --- | --- | --- | --- |
Uwaga: bardzo możliwe, że dla podanego w treści projektu przedziału wag [−5,10] wylosowany
digraf będzie miał cykl o ujemnej sumie wag. Żeby tego uniknąć, mogą Państwo ustalić inny prze-
dział wag, byle tylko nadal niektóre z losowanych wag były ujemne (albo można też zmodyfikować
| wylosowane |     | już wagi, | itd.). |     |     |     |     |     |     |
| ---------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- |
3
|     |     |     |     | 3   |     |     |     | 2   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
-5
|     |     |     |     |     |     |     | 9   |     | 6   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4
|     |     | 1   | 6   | 2   | 5   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4
|     |     |     | 10  |     | -4  |     | 9   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
7
4
-1
|     |     |     |     |     | 4   |     | -4  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
5
Rysunek 2: Dane wyjściowe: przykładowy losowy digraf z losowymi wagami. W digrafie nie ma cyklu
o ujemnej sumie wag. Macierz odległości dla tego digrafu przedstawiono na listingu 4.
2

| 1 0 6 | 1 2   | -1 -1 -5 |     |
| ----- | ----- | -------- | --- |
| 10 0  | -5 -4 | 4 -3 0   |     |
2
| 21 11 | 0 7 | 15 2 11 |     |
| ----- | --- | ------- | --- |
3
| 15 5 | 0 0 | 9 2 5 |     |
| ---- | --- | ----- | --- |
4
| 5 19 9  | 4 5 | 0 0 -4 |     |
| ------- | --- | ------ | --- |
| 6 19 9  | 4 5 | 13 0 9 |     |
| 7 23 13 | 8 9 | 17 4 0 |     |
Listing 4: Dane wyjściowe: macierz odległości dla digrafu z rys. 2; element w wierszu w i kolumnie k
| oznacza długość | najkrótszej | ścieżki od wierzchołka | w do k |
| --------------- | ----------- | ---------------------- | ------ |
3
