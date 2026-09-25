## **Složitost algoritmu**

- **Horní odhad** - $f\in O(g) \iff \exists c >0 \exists n_0 \forall n > n_0: 0\leq f(n) \leq c\cdot g(n)$
- **Dolní odhad** - $f\in \Omega(g) \iff \exists c >0 \exists n_0 \forall n > n_0: 0\leq f(n) \geq c\cdot g(n)$
- **Přesný odhad** $f\in \Theta(g) \iff f\in O(g) \land f\in \Omega(g)$

## Amortizace X průměr

- rozdíl v přístupu k výpočtu složitosti.
- **Amortizace** - přes posloupnost nejhorších vstupních dat - je zaručená (nevyužívá pravděpodobnost) - zaměřuje se na celkový průměr složitosti v průběhu času a bere v úvahu kompenzaci mezi drahými a levnými operacemi - průměrná cena instrukce přes posloupnost
- **Průměr** - zaměřuje se na průměrný náklad na operaci na základě vstupů a jejich distribuci - ideální, pokud distribuci vstupů můžeme odhadnout
- **Příklad**
  - Average involves a random process. Amortized does not. So, for example, suppose you have a system where (1) 1/2 the times you do an operation, it takes 1 second and (2) all other times it takes 10 seconds. Suppose this is just random as if the system just flips a coin every time you do the operation and, based on the coin flip, it decides to do the fast or slow version. Then the average cost is 1/2 _ 1 + 1/2 _ 10 = 5.5 seconds. But sometimes two operations in a row will both be fast or both be slow. Now suppose you have a similar system, except that it always alternates between fast and slow. Then the "average" time is the same, but you can now guaranteed that two successive operations will take 11 seconds. Never more. Never less. So you have a guarantee on the total cost of a sequence of operations. This is the idea of amortized analysis.

## Datové typy a struktury pro ukládání dat

- **Halda** - efektivní přidávání/ odebírání prvků v závislosti na prioritě → prioritní fronta; stromová struktura, rozlišujeme min/max heap, prvek s vyšší prioritou je rodič; používá _heap sort_, _Dijkstra_, _Huffmanovo kódování_ (komprese), hledání max/ min prvku v množině, operace: insert - O(logn), extract - O(logn), search - O(n), build - O(n\*logn)
- **Fronta** - FIFO; seznam úkolů, které mají být vykonány v pořadí, v jakém byly přijaty; používá _BFS_
- **Zásobník** - LIFO; poslední prvek vložený do zásobníku je také první, který bude odebrán; používá _DFS_, vyhodnocování regexu, správa paměti, volání funkcí, kompilátory

![](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20221220165711/MinHeapAndMaxHeap1.png)

## Základní grafové algoritmy

- BFS - prohledávání do šířky - O(m+n)
- DFS - prohledávání do hloubky - O(m+n)

```c#
//BFS
public static void bfs(Graph G, int startVert) {
       bool[] visited = new bool[G.Size];
       System.Collections.Generic.Queue<int> q = new System.Collections.Generic.Queue<int>();

       visited[startVert] = true;

       q.Enqueue(startVert);

       while(q.Count > 0){
                  int v = q.Dequeue();
           foreach(int adjV in G.adj[v]) {
               if (!visited[adjV]) {
                   visited[adjV] = true;
                   q.Enqueue(adjV);
               }
           }
       }
   }

//DFS
public static void dfs(Graph G, int startVert) {
       bool[] visited = new bool[G.Size];
       System.Collections.Generic.Stack<int> s = new System.Collections.Generic.Stack<int>();

       visited[startVert] = true;

       s.Push(startVert);

       while(s.Count > 0) {
           int v = s.Pop();
           foreach(int adjV in G.adj[v]) {
               if (!visited[adjV]) {
                   visited[adjV] = true;
                   s.Push(adjV);
               }
          }
       }
   }
```

## Atributy

- **Public** - třída je veřejná, může přistupovat kdokoliv
- **Private** - třída je neveřejná, může přistupovat pouze stejná třída
- **Protected** - třída je neveřejná, může přistupovat pouze dědic této třídy nebo stejná třída
- **Sealed** - z metody nelze dědit, není virtuální

![](https://i.stack.imgur.com/TNtq3.png)

## Třídy

- **Struct** - zjednodušená třída, nemůže dědit, užito pro seskupení dat, value type, každá proměnná má svoji kopii dat
- **Abstraktní třída** - nevytváří instance, ale slouží jako základ pro odvození konkrétních tříd, má abstraktní metody (které jsou implicitně virtuální) vyžadující přepsání
- **Statická třída** - třída = objekt, třída je jedinou instancí sebe sama

## Metody

- **Obyčejné metody** - o volání je rozhodnuto v okamžiku překladu
- **Statické metody** - nelze při volání vytvářet její instance a nelze dědit. (členy jsou alokovány ve třídě, ne instanci)
- **Virtuální metody** - o volání rozhodnuto až v okamžiku volání. Může být přepsána (`override`) v odvozených třádách
  - _Využití v praxi:_ vytváří kód, který pracuje s objekty různých tříd pomocí stejného rozhraní, snižuje se tak nutnost kopírovat a upravovat stejný kód pro každou třídu zvlášť
  - **VMT - Tabulka virtuálních metod** - zajišťuje podporu polymorfismu během programu. Je to tabulka ukazatelů na virtuální metody (většinou skrytý ukazatel na začátku objektu). Používá se k určení skutečného typu objektu.

```c#
// Virtual method
public class Animal {
    public virtual void MakeSound() {
        Console.WriteLine("I am an animal.");
    }
}
public class Cat : Animal {
    public override void MakeSound() {
        Console.WriteLine("Meow!");
    }
}
public class Fish : Animal {
	public static void MakeSound()  {
		Console.WriteLine("Blob!");
	}
}
public static void Main() {
	Animal cat = new Cat();
	Animal fish = new Fish();
	cat.MakeSound();	// Meow!
	fish.MakeSound();	// I am an animal.
}
```

- **Abstraktní metody** - je společným předchůdcem jiných tříd, nevytváříme instance. Jsou _virtuální_, slouží k budoucímu předefinování v potomcích

```c#
// Abstract method and class
public abstract class Sound {
    public abstract string MakeSound();
}

public class Animal : Sound {
    public override string MakeSound() {
		return "I am an animal.";
	}

    public static void Main() {
        var animal = new Animal();
        Console.WriteLine("Animal sound: " + animal.MakeSound());	// Animal sound: I am an animal.
    }
}
```

## Návrhové vzory

- **SOLID** - pravidla pro přehledné programování
  - _Princip jedné odpovědnosti (**S**ingle Responsibility Principle)_ - jedna třída by měla mít na starosti pouze jednu a tudíž pouze jeden důvod pro změnu
  - _Princip otevřenosti/ zavřenosti (**O**pen-closed principle)_ - třídy otevřené pro rozšiřování, uzavřené pro změny
  - _Zákon substituce (**L**iskov substitution principle)_ - pokud je někde objekt A, pak musí být možné místo něj použít B, pokud je B odvozený od A (děti za rodiče)
  - _Princip oddělených rozhraní (**I**nterface segregation principle)_ - více specifických rozhraní je lepší než jedno univerzální
  - _Princip obrácení závislosti (**D**ependency Inversion Principle)_ - závislost na abstraktním, ne konkrétním. Konkrétní musí záviset na abstraktním. (kvůli časté změně implementace)
- **Strom hry** - Používá se pro modelování a analýzu rozhodovacích procesů v herách a jiných interaktivních situacích - minimax

## Třídění

- **vnější třídění**
  - k řazení velkých objemů dat, které se nevejdou do RAM. Data jsou rozdělena do menších částí, které se načtou do paměti, seřadí, uloží do dočasných souborů na disku
- **vnitřní třídění**
  - jedna datová struktura, obvykle pole nebo seznam, všechna data v operační paměti

### Důkaz dolního odhadu třídících algoritmů

- pokud třídíme porovnáváním prvků, algoritmus zapíšeme jako rozhodovací strom
- za pomoci rozhodovacího stromu - dostaneme v nejlepším případě $n!$ listů
- binární rozhodovací strom bude mít $2^h$ listů - listy jsou možná seřazení prvků podle výsledků porovnávání
- počítáme $2^h \geq n! \iff h\geq \log n!$
- $n!$ nahradíme za $n\cdot (n-1) \cdot (\frac n2 + 1) \cdot ... \cdot (\frac n2)$, nakonec $(\frac n2)$ krát $(\frac n2)\cdot ... \cdot (\frac n2)\cdot (\frac n2) = (\frac n2)^{(\frac n2)}$
- $h \geq \log (\frac n2)^{(\frac n2)} \iff h \geq (\frac n2) \cdot (\log n - \log 2) \iff h \geq \frac n4 \log n \implies \Omega (n\log n)$
- každý algoritmus tedy musí provést alespoň $\Omega (n\log n)$ porovnání

### Třídící algoritmy:

| Algoritmus                 | Složitost                | Animace                                                                                                                                                                                                          |
| -------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bubble sort                | $O(n^2)$                 | ![](https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif)                                                                                                                           |
| Insertion sort (vkládáním) | $O(n^2)$                 | ![](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Insertion-sort-example-300px.gif/220px-Insertion-sort-example-300px.gif)                                                                           |
| Selection sort             | $O(n^2)$                 | ![](https://upload.wikimedia.org/wikipedia/commons/9/94/Selection-Sort-Animation.gif)                                                                                                                            |
| Heap Sort                  | $O(n \log n)$            | ![](https://upload.wikimedia.org/wikipedia/commons/4/4d/Heapsort-example.gif)                                                                                                                                    |
| Merge sort                 | $O(n \log n)$            | ![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Merge_sort_algorithm_diagram.svg/220px-Merge_sort_algorithm_diagram.svg.png)                                                                       |
| Quick sort                 | $O(n \log n)$ → $O(n^2)$ | ![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Partition_example.svg/220px-Partition_example.svg.png)                                                                                             |
| Counting sort              | $O(n*k), k = max číslo$  | ![](https://s1.qwant.com/thumbr/0x0/9/8/7a6bc587016fec214106f5e97f87ce32ccf640439c532f6421a3dd6d491c02/counting-sort.gif?u=https%3A%2F%2Fmedia.tenor.com%2FzswbYsLbYqEAAAAd%2Fcounting-sort.gif&q=0&b=1&p=0&a=1) |

## Hledání nejkratších cest

$m = |E|, n = |V|$

- **BFS, DFS** - $O(m+n)$
- **Dijkstra** - Hledání nejkratší cesty v ohodnoceném, orientovaném grafu bez záporných hran

  - složitost: $O((m + n) \log n)$ s binární haldou
  - ohodnotím vše jako $\infty$, vezmu počát. bod $A$, podívám se, kam jdou jeho hrany, vyberu menší, ...
  - ```python
      function Dijkstra(Graph, source):

          for each vertex v in Graph.Vertices:
              dist[v] ← INFINITY
              prev[v] ← UNDEFINED
              add v to Q
          dist[source] ← 0

          while Q is not empty:
              u ← vertex in Q with min dist[u]
              remove u from Q

              for each neighbor v of u still in Q:
                  alt ← dist[u] + Graph.Edges(u, v)
                  if alt < dist[v]:
                      dist[v] ← alt
                      prev[v] ← u

          return dist[], prev[]
    ```

  - ![](https://s2.qwant.com/thumbr/0x380/d/2/82f58ea5a7bf35d4549d8bd0f4fc67c4172ac73423856062d121fdfba5ca4e/dijkstra.gif?u=https%3A%2F%2Fsurfingthecode.com%2Fimg%2Fdijkstra.gif&q=0&b=1&p=0&a=1)

- **Bellman-Ford** - Hledání nejkratší cesty v ohodnoceném, orientovaném grafu včetně záporných hran

  - složitost: $O(m \cdot n)$
  - začnu na poč. bodu $A$, podívám se na hrany, aktualizuju vrcholy,
  - Mám n-1 fází, v každé fázi provádím standartní relaxaci na každém vrcholu, vždy začínám od počátečního

  ```python
  function bellmanFord(G, S)
  for each vertex V in G
    distance[V] <- infinite
    previous[V] <- NULL
  distance[S] <- 0

  for i from 1 to size(V)-1
    for each edge (U,V) in G
      tempDistance <- distance[U] + edge_weight(U, V)
      if tempDistance < distance[V]
        distance[V] <- tempDistance
        previous[V] <- U

  for each edge (U,V) in G
    If distance[U] + edge_weight(U, V) < distance[V]
      Error: Negative Cycle Exists

  return distance[], previous[]
  ```

  - ![](https://s2.qwant.com/thumbr/700x0/e/a/347e46333a213704c2b88d92b71f751c90e71860d04cf55b6cf9caee405f81/1*1uN5vzAA0PvZVND8fu5iig.gif?u=https%3A%2F%2Fmiro.medium.com%2Fmax%2F1494%2F1*1uN5vzAA0PvZVND8fu5iig.gif&q=0&b=1&p=0&a=1)

- **Floyd-Warshall** - Hledání všech nejkratších cesty v ohodnoceném orientovaném grafu
  - složitost: $O(n^3)$ - porovnává všechny cesty mezi všemi dvojicemi vrcholů
  - sestavíme matici sousednosti
  - `for k; for i; for j:` - `if ` $dist[i][j]>dist[i][k]+dist[k][j] \implies dist[i][j]=dist[i][k]+dist[k][j]$
    ```python
    let dist be a |V| × |V| array of minimum distances initialized to ∞ (infinity)
    for each edge (u, v) do
      dist[u][v] ← w(u, v) // The weight of the edge (u, v)
    for each vertex v do
      dist[v][v] ← 0
    for k from 1 to |V|
      for i from 1 to |V|
        for j from 1 to |V|
          if dist[i][j] > dist[i][k] + dist[k][j]
            dist[i][j] ← dist[i][k] + dist[k][j]
          end if
    ```
  - ![](https://s1.qwant.com/thumbr/0x380/a/c/74de7c597f215d0aff160dd4ae6963a039a37457ccaee0c0754d440cff9261/39281395-51c2ef60-48d2-11e8-81b5-02ebd87b9aca.PNG?u=https%3A%2F%2Fuser-images.githubusercontent.com%2F32994398%2F39281395-51c2ef60-48d2-11e8-81b5-02ebd87b9aca.PNG&q=0&b=1&p=0&a=0)
- **hledání cyklů** - DFS - ukládáme navštívené vrcholy, nesmíme se dostat na navštívený 2x

## Hledání minimálních koster

- **Borůvka** - složitost: $O(m \log n)$

  - funguje paralelně, nejdřív les se stromy o jednom vrcholu
  - po k-té fázi h má každý stromeček alespoň $2^h$ vrcholů
  - vezmu popořadě vždy vrchol a k němu nejmenší dosažitelnou hranu mezi vrcholem a zbytkem grafu
  - ![](https://upload.wikimedia.org/wikipedia/commons/2/2e/Boruvka%27s_algorithm_%28Sollin%27s_algorithm%29_Anim.gif)

- **Kruskal** - složitost: $O(m \log m)$

  - nejdřív les se stromy o jednom vrcholu
  - beru vždy nejmenší hranu, dokud nedostaneme cyklus, pak bereme jinou
  - ![](https://s2.qwant.com/thumbr/0x0/6/c/ec437b30c3250407167067f44dee35ecdb2de53c63d8124e646f78c554d208/kruskal.gif?u=https%3A%2F%2Fvelog.velcdn.com%2Fimages%2Fuoayop%2Fpost%2Fdefe90c6-4e3a-4b0f-a43f-4c775cd6b866%2Fkruskal.gif&q=0&b=1&p=0&a=1)

- **Jarník** - složitost: $O(n^2)$, reprezentace v binární haldě $O(n\log n + m \log m)$
  - vezmi si vrchol, podívám se na hrany, vezmu tu nejmenší dosažitelnou a jdu do ní, pokračuju...
  - ![](https://s1.qwant.com/thumbr/0x0/9/d/cc1c532f6de16d483194dea0ac419696dbf239a4a1529f29a1e0ab1ef8fc5b/graphs-in-python-minimum-spanning-trees-prims-algorithm-8.gif?u=https%3A%2F%2Fs3.stackabuse.com%2Fmedia%2Farticles%2Fgraphs-in-python-minimum-spanning-trees-prims-algorithm-8.gif&q=0&b=1&p=0&a=1)

## Stromové datové struktury a algoritmy na nich

- **BVS** - binární strom, `search, find, delete` průměrně v $O(\log n)$, nejhůř v $O(n)$
  - každý uzel max dva potomky
  - každému uzlu přiřazen určitý klíč - podle hodnot klíčů jsou uzly uspořádány.
  - levé dítě má menší hodnotu klíče než jeho rodič, pravý naopak větší
  - ![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Binary_search_tree.svg/180px-Binary_search_tree.svg.png)

| Insert                                                                                             | Delete                                                                                                                              | Find                                                                                                  |
| -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| ![](https://blog.penjee.com/wp-content/uploads/2015/11/binary-search-tree-insertion-animation.gif) | ![](https://1.bp.blogspot.com/-NEDj-KtZUGM/YLhtRv-PNGI/AAAAAAAAOvM/UY0WmAxsHSI4kmGeXnelQF4v3lRBLFVPQCLcBGAsYHQ/s320/delete_bst.gif) | ![](https://blog.penjee.com/wp-content/uploads/2015/11/binary-search-tree-sorted-array-animation.gif) |

- **AVL-strom** - binární strom, `search, find, delete` nejhůř v $O(\log n)$
  - každý uzel max 2 potomky
  - levé dítě má menší hodnotu klíče než jeho rodič, pravý naopak větší
  - délka nejdelší větve levého a pravého podstromu každého uzlu se liší nejvýše o 1 (_vyvážení_)
  - ![](https://programmingpraxis.files.wordpress.com/2011/11/avl_tree_rebalancing.png)
- **$(a, b)$-strom** - není binární strom, platí $2 \leq a \leq \frac{b+1}2$
  - kořen nejméně dvě děti, nejvýše $b$ dětí, pokud není listem.
  - všechny vnitřní vrcholy krom kořene mají alespoň $a$ a nejvýše $b$ potomků.
  - všechny listy jsou na stejné úrovni, tzn. všechny cesty z kořene do libovolného listu mají stejnou délku.
  - $b$ chceme obvykle jako $2a +1$ nebo $2a$, ideální $(2,3) nebo $(2,4)$
  - na disku $(256, 512)$, cache $(4, 8)$
  - vhodné pro velký objem dat, snižuje počet operací na disku - ukládání na RAM
  - ![](https://s1.qwant.com/thumbr/0x0/8/d/2bc954f60f2e22f19fe5efb1ec2aa02983cdfa4b8797efab9a4c1195834555/b-tree.png?u=https%3A%2F%2Fstatic.javatpoint.com%2Fds%2Fimages%2Fb-tree.png&q=0&b=1&p=0&a=0)
- **Union find** - používaná pro efektivní reprezentaci disjunktních množin, při hledání komponent v grafu a implementaci operací jako spojení (union) a nalezení (find).
  - `union` dvou množin probíhá tak, že se najde kořen každého stromu (množiny), ke kterému se připojí menší strom, aby se minimalizovala hloubka nového stromu a tím i celková složitost operací.
  - `find` pak slouží k určení kořene daného prvku a tedy ke zjištění, zda dva prvky náleží do stejné množiny.

## Dynamické programování

Řešení úlohy se skládá z řešení menších podúloh, která jsme si vypočetli a zapamatovali.
Zkoušíme všechny možnosti rozdělení a vybíráme to nejlepší.
Pěkný abstraktní pohled, že mám systém podproblémů (tzv. stavy DP) a ty mezi sebou mají nějaké závislosti, které tvoří DAG
Princip DP je projít stavy v topologickém pořadí.

- **Optimální substruktura** - optimální řešení problému lze zrekonstruovat z optimálních řešení jeho podproblémů

- **Rekurze** - proces, který volá opakovaně sebe sama
- **Memoizace** - rekurze s ukládáním výsledků pro pozdější použití, aby se nemusel provádět výpočet znovu

Zobecnění principů dynamického programování:

1. Začneme s exponenciálním algoritmem
2. Všimneme si, že často počítáme to samé
3. Zavedeme si proto paměť na známé výsledky
4. Rekurzi nahradíme vyplňování keše ve správném pořadí

Techniky:

- **Memoizace** - Top Down, rekurzivní, ukládáme si vypočítané výsledky od keše
- **Tabulace** - Bottom Up, iterativní, od nejmenšího po největší

### Příklady

- **Závorkování násobení matic**

  - $O(n^3)$
  - Násobení 2 matic $A(m*n)$ a $B(n*p)$ stojí $m*n*p$ operací
  - Pro násobení matic platí asocitivita
  - pokud $i=j$, tak $m(i,j) = 0$
  - pokud $i\neq j$, tak $m(i,j) = \min [m(i,k), + m(k+1, j) + p_{i-1}p_kp_j]$, kde $k\in [i, j-1]$

- **Celočíselný problém batohu (0-1 Knapsack)**
  - O(C\*n) - lze problém omezit polynomem, ne velikostí vstupu
  - Máme batoh, který má pevně danou nosnost. Máme množinu věcí, které mají svoji cenu a hmotnost. Úkolem je dát do batohu některé věci tak, aby součet vah nepřekročil nosnost a přitom součet cen byl co největší.
  - Funguje na základě vyplňování tabulky
  - Sloupce reprezentují váhy 0 - maximální váha
  - Řádky reprezentují předměty
  - Hodnota buňky [i,j] je maximální hodnota z prvních i předmětů s celkovou váhou $\leq$ váha j

```python
// Input:
// Values (stored in array v)
// Weights (stored in array w)
// Number of distinct items (n)
// Knapsack capacity (W)
// NOTE: The array "v" and array "w" are assumed to store all relevant values starting at index 1.

array m[0..n, 0..W]
for j from 0 to W do:
    m[0, j] := 0
for i from 1 to n do:
    m[i, 0] := 0

for i from 1 to n do:
    for j from 0 to W do:
        if w[i] > j then:
            m[i, j] := m[i-1, j]
        else:
            m[i, j] := max(m[i-1, j], m[i-1, j-w[i]] + v[i])
```

- ![](https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Knapsack_problem_dynamic_programming.gif/440px-Knapsack_problem_dynamic_programming.gif)

## Diskrétní simulace

Využívá se ke zkoumání a analýze chování složitých systémů - jsou závislé na čase, instrukcích apod. Umožňují testování různých scénářů za různých podmínek... používá se převážně v dopravě, logistice atd.
Čas je modelován jako posloupnost událostí.
Provádí se v krocích, kde každý krok reprezentuje nějaký okamžik, ve kterém se odehrávají dané události. V každém kroku jsou vyhodnoceny všechny události ve frontě.

**Složky diskrétní simulace**

- Simulační jádro
- Čas
- Události
- Kalendář / Fronta událostí - kdy události mají nastat, přidávat a ubírat události
- Výstup / Statistiky - čas konce simulace
- Koncové podmínky - prázdný kalendář

**Stavy procesů**

- Naplánovaný - čeká v kalendáři
- Čeká (pasivní) - čeká na probuzení
- Běží - obsluhován jako událost
- Ukončený - doběhl a je bez událostí

**Programování řízené událostmi** - hlavní část programu reaguje na události (uživatelské vstupy, data). Jaké akce by měly být vyvolány jako reakce na tyto události.

**_Příklad z hodiny - Obchodní dům:_**
Jeden stav/ událost = příchod zákazníka, čas strávený v obchodě, čas ve výtahu apod.

## Objektivně orientované programování

- **OOP** - zaměření se na organizaci kódu kolem objektů. Umožňuje abstrakci dat, takže minimum opakujícího se kódu. Díky tomu může být kód snadno program udržován a rozšířen.
- **Třídy** - abstraktní popis objektů, který určuje, jaké proměnné objekt obsahuje a jaké metody má k dispozici.
- **Objekty** - instance třídy, která má své vlastní specifické stavy a chování.
- **Zapouzdření** - mechanismus, který umožňuje skrýt interní implementaci třídy a zpřístupnit ji pouze prostřednictvím veřejných metod
- **Dědičnost** - sdílení vlastností tříd - umožňuje vytvářet nové třídy na základě existujících tříd s přidanými nebo upravenými vlastnostmi a metodami.
- **Dolymorfismus** - schopnost objektů různých typů vykonávat stejnou operaci s různým chováním

### Dekompozice

- rozložení složitého celku na menší, snadno řešitelné části
- **Modulární dekompozice** - rozdělení systému na menší, snadněji spravovatelné a testovatelné moduly, které jsou navzájem nezávislé a provádějí jasně definované úkoly. Umožňuje programátorům oddělit různé části aplikace do samostatných modulů, což zlepšuje přehlednost, udržovatelnost a opětovné použití kódu.
- **Funkční dekompozice** - rozdělení funkcionality do menších samostatných celků, které jsou snadněji udržovatelné a testovatelné.
  - _Třídy_
  - _Abstraktní třídy_: nemohou být přímo instancovány, ale slouží jako základ pro další třídy. Tyto třídy definují společné vlastnosti a metody, které se používají v různých verzích a specializacích tříd.
  - _Rozhraní_: speciální abstraktní třídy, které definují sadu veřejných metod, které musí být implementovány třídami, které rozhraní používají. Umožňují oddělit implementaci od rozhraní a usnadnit vývoj a údržbu kódu.
  - _Kompozice_: skládá třídy z jiných tříd, čímž se dosáhne složitějších funkcionalit. Například třída "auto" může být složena z tříd pro motor, palivový systém a podvozek.
- **Objektová dekompozice**
  - _Agregace_:umožňu je seskupit několik objektů do většího celku, přičemž tyto objekty si zachovávají svou autonomii a mohou být použity v různých kontextech.
  - Kompozice, Zapouzdření, Dědičnost
  - SOLID

## Generické programování - C#

- **Generické funkce a třídy** -typy funkcí/ tříd umožňující definovat obecné typy nezávislé na konkrétních datových typech. To znamená, že můžete napsat jednu funkci nebo třídu, která může pracovat s různými typy dat, aniž byste museli psát samostatnou verzi pro každý typ.

  - _Zjednodušení kódu a snadnější údržba_ - místo opakovaného psaní kódu pro různé datové typy můžeme použít jednu obecnou funkci nebo třídu pro všechny typy.
  - _Znovupoužitelnost_ - užitečné pro knihovny/ frameworky, kde se očekává, že budou použity s různými datovými typy.
  - _Bezpečnost typů_ -umožňují kompilátoru ověřit, zda jsou argumenty funkce/ třídy správného typu, což může pomoci zabránit chybám při běhu programu.
  - Generická funkce - funkce pro seřazení pole, která pracuje s libovolným typem dat.
  - Generická třídy - kolekce, jako je seznam nebo slovník, která může uchovávat libovolný typ dat.

- **delegáty** - typ reference na metodu nebo seznam metod, který umožňuje předat funkci jako argument do jiného kódu a zavolat ji později. Běžně používány pro události, kde se jedna část kódu musí ozvat druhé části, že nastala určitá událost.
  - lze definovat jako třídy, které obsahují odkaz na metodu s konkrétním signaturou. To znamená, že delegát může být použit ke směrování na metodu s určitým počtem parametrů a návratových hodnot. Pokud potřebujete volat více metod najednou, můžete použít multicastový delegát, což je delegát, který dokáže směrovat více metod současně.
  - _Oddělení logiky_ - Kód, který spouští událost, nemusí vědět, jaké operace budou vykonány při jejím zpracování. Tuto logiku lze oddělit a implementovat v jiném místě pomocí delegátů.
  - _Flexibilita_ - Delegáty umožňují dynamicky změnit chování programu během běhu. Například můžete přidávat a odebírat metody ze seznamu delegátů v závislosti na událostech, které se vyskytují.
  - _Opakované použití_ - Delegáty mohou být opakovaně použity pro různé účely, což eliminuje potřebu psát stejný kód vícekrát.
  - Běžně používány pro zachycení událostí uživatelského rozhraní (např. kliknutí tlačítka).

## Hashovací tabulky

- find v $O(1)$
- máme nějaké univerzum klíčů $U$ a klíče $K$ - každému klíči je přiřazena nějaká hodnota (hash) - neboli klíč se převede na číslo
- kolizi můžeme řešit např. řetězením - "spoják" nebo otevřenou adreasí - při kolizi hledám nejbližší volné místo
- vhodné pro implementaci slovníku, cache pamětí, databází apod.


----

> K tvorbě dokumentu přispěl Matěj Foukal