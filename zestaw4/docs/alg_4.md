41
|     |          |     |     |          | Algorytmy |     | do  | zestawu |     | nr  |     |     |
| --- | -------- | --- | --- | -------- | --------- | --- | --- | ------- | --- | --- | --- | --- |
| 1.  | Algorytm |     |     | Kosaraju |           |     |     |         |     |     |     |     |
Algorytm Kosaraju, oznaczający silnie spójne składowe w grafie skierowanym, polega na dwóch prze-
| szukiwaniach |        | w      | głąb:         | w liniach | 1–10        | oraz | 12–22. |     |     |     |     |     |
| ------------ | ------ | ------ | ------------- | --------- | ----------- | ---- | ------ | --- | --- | --- | --- | --- |
|              | • d[v] | – czas | odwiedzenia   |           | wierzchołka |      | v.     |     |     |     |     |     |
|              | • f[v] | – czas | przetworzenia |           | wierzchołka |      | v.     |     |     |     |     |     |
• comp[v] – numer silnie spójnej składowej, do której należy wierzchołek v.
| Algorytm |           | 1: kosaraju(G) |             |     |            |     |          |              |     | . G –       | skierowany       | graf wejściowy |
| -------- | --------- | -------------- | ----------- | --- | ---------- | --- | -------- | ------------ | --- | ----------- | ---------------- | -------------- |
| 1:       | for każdy |                | wierzchołek |     | v należący |     | do grafu | G            | do  |             |                  |                |
|          | d[v]      | ← −1           |             |     |            |     |          | . Oznaczenie |     | wierzchołka | nieodwiedzonego. |                |
2:
| 3:  | f[v]    | ←   | −1  |     |     |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | end for |     |     |     |     |     |     |     |     |     |     |     |
4:
5: t ← 0
|     | for każdy |     | wierzchołek |     | v należący |     | do grafu | G   | do  |     |     |     |
| --- | --------- | --- | ----------- | --- | ---------- | --- | -------- | --- | --- | --- | --- | --- |
6:
| 7:  | if  | d[v] | = −1 | then |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
DFS_visit(v,G,d,f,t)
8:
| 9:  | end     | if  |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | end for |     |     |     |     |     |     |     |     |     |     |     |
10:
11: Utwórz graf GT, będący transpozycją G . W GT zwroty krawędzi są odwrócone.
|     | nr ← | 0   |     |     |     |     |     |     | .   | Numer silnie | spójnej | składowej. |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | ---------- |
12:
| 13: | for każdy |     | wierzchołek |     | v   | należący | do  | grafu GT  | do  |             |     |                |
| --- | --------- | --- | ----------- | --- | --- | -------- | --- | --------- | --- | ----------- | --- | -------------- |
|     | comp[v]   |     | ← −1        |     |     |          |     | .         |     |             |     |                |
| 14: |           |     |             |     |     |          |     | Wszystkie |     | wierzchołki | są  | nieodwiedzone. |
| 15: | end for   |     |             |     |     |          |     |           |     |             |     |                |
GT
16: for każdy wierzchołek v należący do w kolejności malejących czasów f[v] do
| 17: | if  | comp[v] | =    | −1  | then |     |     |     |     |     |     |     |
| --- | --- | ------- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
| 18: |     | nr ←    | nr+1 |     |      |     |     |     |     |     |     |     |
| 19: |     | comp[v] | ←    | nr  |      |     |     |     |     |     |     |     |
components_r(nr,v,GT,comp)
20:
| 21: | end     | if   |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22: | end for |      |     |     |     |     |     |     |     |     |     |     |
|     | return  | comp |     |     |     |     |     |     |     |     |     |     |
23:
1Na podstawie: Cormen Thomas H., Leiserson Charles E., Rivest Ronald L., Wprowadzenie do algorytmów, Wyd. 4,
| Warszawa, |     | Wydawnictwo |     | Naukowo | – Techniczne, |     | 2001, | ISBN 83-204-2665-0. |     |     |     |     |
| --------- | --- | ----------- | --- | ------- | ------------- | --- | ----- | ------------------- | --- | --- | --- | --- |
1

Uwaga:algorytmrekurencyjnyDFS_visit(v,G,d,f,t)musimiećbezpośrednidostępdozmiennej
t, żeby móc ją edytować – nie wystarczy przekazanie parametru t przez wartość.
| Algorytm | 2:  | DFS_visit(v,G,d,f,t) |     |     |     |     |     |
| -------- | --- | -------------------- | --- | --- | --- | --- | --- |
1: t ← t+1
| 2:  | d[v] ← t |     |     |     |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- |
3: for każdy wierzchołek u ∈ G będący sąsiadem v do . Przejście po krawędzi (v,u)
| 4:  | if d[u]              | = −1 | then |     |     |     |     |
| --- | -------------------- | ---- | ---- | --- | --- | --- | --- |
| 5:  | DFS_visit(u,G,d,f,t) |      |      |     |     |     |     |
|     | end                  | if   |      |     |     |     |     |
6:
| 7:  | end for |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- |
t ← t+1
8:
9: f[v] ← t . W implementacji ze stosem: tutaj należy dodać v do stosu.
| Algorytm | 3:        | components_r(nr,v,GT,comp) |      |        |                 |      |     |
| -------- | --------- | -------------------------- | ---- | ------ | --------------- | ---- | --- |
| 1:       | for każdy | wierzchołek                |      | u ∈ GT | będący sąsiadem | v do |     |
|          | comp[u]   | =                          | −1   |        |                 |      |     |
| 2:       | if        |                            | then |        |                 |      |     |
| 3:       | comp[u]   | ←                          | nr   |        |                 |      |     |
components_r(nr,u,GT,comp)
4:
| 5:  | end     | if  |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- |
| 6:  | end for |     |     |     |     |     |     |
W implementacji ze stosem wierzchołek v należy dodać do stosu w momencie zakończenia jego
przetwarzaniaprzezpierwszeprzeszukiwaniewgłąb,tj.w9.krokuprocedury DFS_visit(v,G,d,f,t).
Wówczas główna pętla drugiego przeszukiwania w głąb, tj. pętla z 16. kroku procedury kosaraju(G),
| przechodzi | po       | wierzchołkach |                | w kolejności | ściągania | ich ze stosu. |     |
| ---------- | -------- | ------------- | -------------- | ------------ | --------- | ------------- | --- |
| 2.         | Algorytm |               | Bellmana-Forda |              |           |               |     |
Algorytm 4: bellman_ford(G,w,s) . Graf G ma n wierzchołków. w – macierz wag krawędzi,
| s – | wierzchołek | startowy. |     |     |     |     |     |
| --- | ----------- | --------- | --- | --- | --- | --- | --- |
init(G,s)
1:
| 2:  | for i ← | 1 to n−1      | do  |                |          |      | . n−1 iteracji. |
| --- | ------- | ------------- | --- | -------------- | -------- | ---- | --------------- |
|     | for     | każda krawędź |     | (u,v) należąca | do grafu | G do |                 |
3:
| 4:  | relax(u,v,w) |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- |
|     | end          | for |     |     |     |     |     |
5:
| 6:  | end for   |                     |       |          |          |     |     |
| --- | --------- | ------------------- | ----- | -------- | -------- | --- | --- |
|     |           |                     | (u,v) |          |          | G   |     |
| 7:  | for każda | krawędź             |       | należąca | do grafu | do  |     |
| 8:  | if d      | [v] > d [u]+w[u][v] |       | then     |          |     |     |
|     |           | s s                 |       |          |          |     |     |
9: return FALSE . W grafie jest cykl o ujemnej wadze osiągalny ze źródła s.
| 10: | end     | if   |     |     |     |     |     |
| --- | ------- | ---- | --- | --- | --- | --- | --- |
| 11: | end for |      |     |     |     |     |     |
| 12: | return  | TRUE |     |     |     |     |     |
2

| 3.  | Algorytm |     | Johnsona |     |     |     |     |     |     |     |     |     |
| --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
• d [v] – długość najkrótszej ścieżki z dodatkowego wierzchołka s do v, obliczona w 2. kroku.
s
• D – wynikowa macierz odległości w grafie G (długości najkrótszych ścieżek między każdą parą
wierzchołków).
|     | • w – macierz | z   | przeskalowanymi |     | wagami | (nieujemnymi). |     |     |     |     |     |     |
| --- | ------------- | --- | --------------- | --- | ------ | -------------- | --- | --- | --- | --- | --- | --- |
b
• dbu [v] – długość najkrótszej ścieżki z wierzchołka u do v dla zmodyfikowanych wag w .
b
| Algorytm | 5:            | johnson(G,w) |     |     |     |     |     |     |     |     |     |     |
| -------- | ------------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|          | G0 ← add_s(G) |              |     |     |     |     |     |     |     |     |     |     |
1:
bellman_ford(G0,w,s)
| 2:  | if    |     |     | =   | FALSE | then |     |     |             |      |           |        |
| --- | ----- | --- | --- | --- | ----- | ---- | --- | --- | ----------- | ---- | --------- | ------ |
|     | ERROR |     |     |     |       |      |     |     | . G zawiera | cykl | o ujemnej | wadze. |
3:
4: else
|     | for | każdy | wierzchołek |     | v należący |     | do G0 | do  |     |     |     |     |
| --- | --- | ----- | ----------- | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- |
5:
6: h[v] ← d [v] . Tablica odległości d pochodzi z algorytmu Bellmana-Forda.
|     |     |     | s   |     |     |     |     | s   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | end | for |     |     |     |     |     |     |     |     |     |     |
7:
| 8:  | for    | każda      | krawędź           | (u,v)      | należąca | do  | grafu | G0  | do  |     |     |     |
| --- | ------ | ---------- | ----------------- | ---------- | -------- | --- | ----- | --- | --- | --- | --- | --- |
|     |        | w [u][v] ← | w[u][v]+h[u]−h[v] |            |          |     |       |     |     |     |     |     |
| 9:  |        | b          |                   |            |          |     |       |     |     |     |     |     |
| 10: | end    | for        |                   |            |          |     |       |     |     |     |     |     |
|     | Utwórz | macierz    |                   | D rozmiaru |          | n×n |       |     |     |     |     |     |
11:
| 12:      | for    | każdy        | wierzchołek |                   | u należący |          | do G     | do   |             |     |            |     |
| -------- | ------ | ------------ | ----------- | ----------------- | ---------- | -------- | -------- | ---- | ----------- | --- | ---------- | --- |
|          |        | dijkstra(G,w |             | ,u)               |            | .        |          | dbu  | [v]         |     | v          | G.  |
| 13:      |        |              |             | b                 |            | Aby      | obliczyć |      | dla każdego |     | należącego | do  |
| 14:      |        | for każdy    | wierzchołek |                   | v          | należący | do       | G do |             |     |            |     |
| 15:      |        | D[u][v]      | ←           | dbu [v]−h[u]+h[v] |            |          |          |      |             |     |            |     |
| 16:      |        | end for      |             |                   |            |          |          |      |             |     |            |     |
| 17:      | end    | for          |             |                   |            |          |          |      |             |     |            |     |
| 18:      | return | D            |             |                   |            |          |          |      |             |     |            |     |
| 19:      | end if |              |             |                   |            |          |          |      |             |     |            |     |
| Algorytm | 6:     | add_s(G)     |             |                   |            |          |          |      |             |     |            |     |
|          | Utwórz | G0 ← G∪s     |             |                   |            |          |          |      |             |     |            |     |
1:
| 2:  | for każdy | wierzchołek |       | v należący |     | do  | grafu | G do |     |     |     |     |
| --- | --------- | ----------- | ----- | ---------- | --- | --- | ----- | ---- | --- | --- | --- | --- |
|     |           |             | (s,v) |            | G0  |     |       |      |     |     |     |     |
| 3:  | Dodaj     | krawędź     |       | do         |     |     |       |      |     |     |     |     |
| 4:  | w[s][v]   | ← 0         |       |            |     |     |       |      |     |     |     |     |
| 5:  | end for   |             |       |            |     |     |       |      |     |     |     |     |
| 6:  | return    | G0          |       |            |     |     |       |      |     |     |     |     |
3
