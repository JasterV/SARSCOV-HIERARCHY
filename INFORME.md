# COVID-19 CHALLENGE

La majoría de parts d'aquest projecte estan desenvolupades amb Python. Per a la part de l'alineament de seqüencies hem utilitzat el llenguatje Rust implementant també multiprocessament per a fer més ràpida l'execució.

Podeu trobar la documentació tant del codi de Python com de Rust al link que trobareu al fitxer readme del repositori.

## Preprocessament

+ #### Tractament inicial de les dades

Per realitzar aquesta fase vam definir 2 objectes amb Python: FastaMap i CsvTable.

L'objecte FastaMap ens ajuda amb el tractament de les dades del fitxer fasta com el propi nom indica, aportant les funcionalitats bàsiques que s'espera d'un diccionari de python però afegint a més la resta de mètodes requerits per al projecte.

Per altra banda, l'objecte CsvTable ens ajuda a tractar amb les dades del fitxer csv representades com una llista de diccionaris (cada diccionari representa una fila de la taula). De la mateixa manera, aquest objecte es troba dotat de funcionalitats que esperaríem trobar en una taula d'aquest tipus (Poder iterar sobre els elements, indexar per files, agafar les dades de les columnes... etc.)

+ #### Desenvolupament de l'algoritme

L'objectiu d'aquesta part del projecte es basa en realitzar el que nosaltres vam interpretar com un 'filtrat' de les dades de la taula csv.

L'algorisme que proposem es prou senzill com per obtenir els resultats iterant un sol cop totes les files. El primer pas es basa en agrupar totes les mostres per paisos amb un diccionari. La clau d'aquest diccionari es el país a agrupar i el valor es una llista de tuples. Cada tupla conté 2 valors: L'index de la fila a la que correspón la mostra i la mida de la mostra.

Un cop hem agrupat les mostres d'aquesta manera, seleccionem la mostra de mida mediana mitjançant l'algorisme *Quick Select* per cada llista de tuples del diccionari de paísos creat anteriorment.

D'aquesta manera conseguim agafar el valor medià de cada llista (El qual recordem que es basa en una tupla *(index_fila, mida)* ), i crear una nova llista de diccionaris agafant de la taula original les files corresponents als indexos de cada tupla.

Com que l'objecte CsvTable permet crear una nova instancia a partir d'una llista de diccionaris, podem retornar sense problema un nou objecte CsvTable!

+ #### Complexitat de l'algoritme

Aquest algoritme té un cost O(n^2) en el pitjor dels casos, en el millor té un cost O(n).
A que es degut això? Doncs bé, primer de tot recorrem un sol cop totes les mostres per construir el diccionari de paisos, fins aqui tenim O(n).

Aleshores hem de recorrer cada país del diccionari seleccionant la mostra de mida mitjana amb l'algoritme *Quick Select*, el qual té un cost de O(n^2) en el pitjor dels casos i un cost de O(n) en el millor. 

Imaginem que només hi ha un país, per tant el diccionari només té una llista amb totes els mostres, el cost total en el pitjor dels casos quedaría així:
```
	O(n + n^2) => O(n^2)
```
I en el millor dels casos quedaría:
```
	O(n + n) => O(2n) => O(n)
```
Per molts paísos que hi hagi, els costos sempre seràn iguals, perque per exemple si tinguessim 4 paísos amb les mostres repartides equitativament entre cada país, el cost del pitjor cas sería:
```
	O(n + (n/4)^2 * 4) => O(n + (n^2)/16 * 4) => O(n^2)
```

## Alineament de seqüencies

Aquesta part del projecte l'hem implementat amb Rust. El motiu d'aquest canvi de paradigma es deu a l'eficiencia, control i seguretat que ens aporta aquest llenguatje sobre la gestió de la memòria a l'hora de realitzar l'alineament de seqüencies.

+ #### Algoritme Needleman Wunsch

L'algoritme que hem escollit és ni més ni menys que el famós algoritme de *[Needleman Wunsch](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)*.
Tot i que no és molt complex si parlem de la seva implementació, resulta tenir un cost molt elevat tant de memòria com d'execució degut a com tracta les dades.



## Classificació

