# COVID-19 CHALLENGE

La majoría de parts d'aquest projecte estan desenvolupades amb Python. Per a la part de l'alineament de seqüencies hem utilitzat el llenguatje Rust implementant també multiprocessament per a fer més ràpida l'execució.

Podeu trobar la documentació tant del codi de Python com de Rust al link que trobareu al fitxer readme del repositori.

# Preprocessament

## Tractament inicial de les dades

Per realitzar aquesta fase vam definir 2 objectes amb Python: FastaMap i CsvTable.

L'objecte FastaMap ens ajuda amb el tractament de les dades del fitxer fasta com el propi nom indica, aportant les funcionalitats bàsiques que s'espera d'un diccionari de python però afegint a més la resta de mètodes requerits per al projecte.

Per altra banda, l'objecte CsvTable ens ajuda a tractar amb les dades del fitxer csv representades com una llista de diccionaris (cada diccionari representa una fila de la taula). De la mateixa manera, aquest objecte es troba dotat de funcionalitats que esperaríem trobar en una taula d'aquest tipus (Poder iterar sobre els elements, indexar per files, agafar les dades de les columnes... etc.)

## Desenvolupament de l'algoritme

L'objectiu d'aquesta part del projecte es basa en realitzar el que nosaltres vam interpretar com un 'filtrat' de les dades de la taula csv.

L'algorisme que proposem es prou senzill com per obtenir els resultats iterant un sol cop totes les files. El primer pas es basa en agrupar totes les mostres per paisos amb un diccionari. La clau d'aquest diccionari es el país a agrupar i el valor es una llista de tuples. Cada tupla conté 2 valors: L'index de la fila a la que correspón la mostra i la mida de la mostra.

Un cop hem agrupat les mostres d'aquesta manera, seleccionem la mostra de mida mediana mitjançant l'algorisme *Quick Select* per cada llista de tuples del diccionari de paísos creat anteriorment.

D'aquesta manera conseguim agafar el valor medià de cada llista (El qual recordem que es basa en una tupla *(index_fila, mida)* ), i crear una nova llista de diccionaris agafant de la taula original les files corresponents als indexos de cada tupla.

Com que l'objecte CsvTable permet crear una nova instancia a partir d'una llista de diccionaris, podem retornar sense problema un nou objecte CsvTable!

## Complexitat de l'algoritme

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

# Alineament de seqüencies

Aquesta part del projecte l'hem implementat amb Rust. El motiu d'aquest canvi de paradigma es deu a l'eficiencia, control i seguretat que ens aporta aquest llenguatje sobre la gestió de la memòria a l'hora de realitzar l'alineament de seqüencies.

## Algoritme Needleman Wunsch

L'algoritme que hem escollit és ni més ni menys que el famós algoritme de *[Needleman Wunsch](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)*.
Tot i que no és molt complex si parlem de la seva implementació, resulta tenir un cost molt elevat tant de memòria com d'execució degut a com tracta les dades.

Es planteja com a objectiu calcular la distancia entre 2 seqüencies i es segueixen els següents passos:

+ Defineix 3 valors per a les següents situacions: GAP (Cal afegir o eliminar un simbol), MISMATCH (2 simbols són diferents) i MATCH (2 símbols són iguals). En el nostre cas el valor per a MATCH es 0, MISMATCH 1 i GAP 2.

+ Crea una matriu *(N + 1) * (M + 1)* on N i M representen la llargada de cada seqüencia. 

+ Recorre la primera fira i la primera columna de la matriu contant cada casella com un GAP.

+ Recorre la resta de la matriu (N * M caselles) comparant així cada símbol de la 1a seqüencia amb cadascún de la 2a.

	Introdueix en cada casella el valor òptim (o mínim) a col·locar a partir dels anteriors de la següent manera:
``` Rust
	// c1 i c2 son els simbols a comparar
	// check_match retorna 0 si c1 i c2 són iguals o 1 si son diferents
	let fit = matrix[(i, j)] + check_match(c1, c2);
    let delete = matrix[(i, j + 1)] + GAP;
    let insert = matrix[(i + 1, j)] + GAP;
	let min_val = min(min(fit, delete), min(fit, insert));
	matrix[(i + 1, j + 1)] = min_val;
```
	
## Complexitat de l'algoritme

Un cop ja coneguda l'implementació de l'algoritme de **Needleman-Wunsch**, ja podem parlar de la seva complexitat.

Tal com hem vist, per a realitzar l'alineament es necessita crear una matriu de mida (N + 1) * (M + 1) on N i M representen la llargada de les 2 seqüencies. Seguidament el que fem es recorrer tota la matriu exceptuant la primera fila i la primera columna que es recorren anteriorment.

Per tant podem concluir en que la complexitat d'aquest algorisme es **O(N * M)**.

## Anàlisi experimental

+ ## Cost en memòria 

	Com hem dit al principi d'aquest apartat, l'algoritme implementat consumeix molta memoria quan comencem a treballar amb seqüencies grans.

	En el nostre cas hem intentat reduir al mínim aquest impacte aprofitant la facilitat que ens aporta el llenguatje ***Rust*** en quant a gestió de la memoria.

	I perquè diem que aquest algoritme consumeix molta memoria? Doncs bé, tot recau en el fet d'haver de crear una matriu de mida **(N + 1) * (M + 1)**.

	Si pensem en seqüencies petites de fins a 100 caracters (Per posar un exemple), la matriu arriba a tenir unes 101 * 101 cel·les, es a dir, 10201 cel·les. 

	Anem a seguir amb l'exemple donat. Si a cada casella introduim un nombre enter de 64 bits (8 bytes), la matriu sencera ocupara en memoria 10201*8 bytes, es a dir, 0.08 MB.

	Sembla poc oi? Doncs anem a fer els càlculs per a seqüencies reals:

	Una seqüencia RNA en el pitjor cas pot arribar a tenir una llargada aproximada de 30000 caracters. En el pitjor dels casos (Si comparessim 2 seqüencies d'aquesta llargada), suposaría crear una matriu de 30001 * 30001 cel·les, es a dir, 900060001 cel·les.

	Si l'emplenem amb nombres enters de 64 bits, la matriu arribarà a ocupar en memoria **7.2 Gygabytes**!!

	Ara bé, com hem afrontat nosaltres aquest problema fins el punt de poder arribar a fer multiprocessament per a realitzar més d'una comparació a l'hora?.

	Primer de tot ens vam donar compte de que no necessitavem enters de 64 bits. De fet canviant els valors MATCH, MISMATCH i GAP de 1, -1 i -2 respectivament a 0, 1 i 2, podíem deixar d'utilitzar nombres amb signe. I no només això, sino que si les seqüencies poden arribar a tenir fins a 30000 caràcters, la matriu mai arribarà a emmagatzemar nombres que superin a 60000! (En el cas que contessim tot GAPs). Per tant, hem passat d'utilitzar enters de 64 bits a utilitzar nombres sense signe de 16 bits!!

	Per tant, si tornem a realitzar els càlculs, en el pitjor dels casos una matriu ocuparà 900060001 * 2 bytes, es a dir, **1,8 Gygabytes!**

+ ## Temps d'execució

	Gràcies a l'optimització de la gestió de la memòria explicada anteriorment, el temps d'execució s'ha vist reduit en picat.

	Això és deu a la reducció del nombre de dades amb les quals s'ha de treballar al *Heap* (Zona de memòria a la qual suposa un cost elevat accedir en compariació al *Stack*), ja que és on s'emmagatzema cada matriu que es crea.

	Actualment treballant amb valors del tipus **u16**, una sola comparació entre 2 mostres mitjançant alineament de seqüencies tarda de mitjana 1 segon.

	Anteriorment, treballant amb valors del tipus **i16**, una comparació podía arribar a tardar uns 3.5 segons de mitjana, i treballant amb valors del tipus **i64**, en un *PC* amb mínim 8 GB de RAM, podía tardar uns 7 segons.

# Classificació

