# time-checker (Proiectul 3: Recognising time in texts)

Echipă:
* Bobric Maria-Cristina, 3B2
* Crăciun Răzvan-Ioan, 3B2
* Grădinariu Tudor, 3B2
* Iacob Constantin-Cristian, 3B2
* Petriuc Cezar-Cristian, 3B2

Status:
** OUTDATED **
Până acum am creat un script care extrage textul din corpusul Ro-TimeBank si il separa in doua fisiere diferite: TIMEXS_RAW.txt si OTHER_ROW.txt
astfel incat in fisierul timex se afla toate cuvintele care apartin unei expresii temporale ( <TIMEX> tags in corpus) iar in fisierul other, celealte cuvinte din text.

Aceste fisiere sunt folosite ca date pentru un clasificator bayesian care primeste ca parametru o lista de cuvinte si returneaza cuvintele pentru care probabilitatea
de a apartine unei expresii temporale este mai mare decat cea contrara.

Momentan nu avem date suficiente pentru ca acest model sa detecteze majoritatea cuvintelor care fac parte din expresii temporale, dar pentru cuvinele care sunt in output,
putem spune cu certitudine suficient de mare ca apartin unei expresii temporale.

Exemplu:
'''La 4 iulie 2019, Arjen Robben a ales să se retragă din fotbalul profesionist la doar 35 de ani, el spunând că aceasta a fost o decizie dificilă.
Ultimul său meci a fost în luna mai a anului 2019 după câteva luni în care a stat pe bancă din cauza unei accidentări.'''

Output:
Origin: 52 words. Result: 16 words
Duration 0.02 seconds
['iulie', 'ani', 'ultimul', 'luna', 'anului', 'luni']

De asemenea, pentru o filtrare mai grosiera a textului am introdus o varianta biased a aceluiasi clasificator cu urmatoarele adaugiri:
- pentru cuvinele noi (care nu apar in corpus) se presupune ca acestea fac parte dintr-o expresie temorala
- pentru numere care pot fi convertite direct in int (1997, 23 etc.) se presupune ca acestea fac parte dintr-o expresie temorala
- pentru orice alt cuvant probabilitatea de a face parte dintr-o expresie temporala este crescuta cu 1%

Output pentru acelasi exemplu:
Origin: 52 words. Result: 16 words
Duration 0.02 seconds
['4', 'iulie', '2019', 'arjen', 'robben', 'fotbalul', 'profesionist', '35', 'ani', 'ultimul', 'meci', 'luna', 'anului', '2019', 'luni', 'accidentări']

Urmează ca pentru săptămâna viitoare să finalizăm componenta ce foloseşte regex-uri pentru indentificarea expresiilor şi să le integrăm
