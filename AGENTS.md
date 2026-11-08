# AGENTS.md

Repozytorium na rozwiązania zestawów zadań. Wszystko w Pythonie.

## Zasady

- Rozwiązania piszemy jako **bibliotekę wielokrotnego użytku**: wspólne struktury i algorytmy (grafy, wektory, macierze, itp.) lądują w współdzielonych modułach, a nie kopiowane między zestawami.
- Kod z zestawu na zestaw ma się dać reużywać — nowe zestawy importują z istniejących modułów zamiast duplikować logikę.
- Każdy zestaw to osobny pakiet/katalog, np. `zestaw1/`, `zestaw2/`, ze skryptem wejściowym do danego zadania; logika właściwa trafia do libki.
