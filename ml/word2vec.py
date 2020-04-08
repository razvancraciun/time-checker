import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from stemming.run_stemmer import run_stemmer
from nltk.tokenize import RegexpTokenizer

import os
import random

VOCABULARY_PATH = RAW_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/vocabulary/vocabulary.txt'

class Word2Vec(nn.Module):
    def __init__(self, n_words):
        super(Word2Vec, self).__init__()

        self.reprs = nn.Linear(n_words, 300)
        self.output = nn.Sequential(
            nn.Linear(300, n_words),
            nn.Softmax(dim=1)
        )

        self.loss = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.parameters(), lr=0.01)
    
    def forward(self, x):
        y = self.reprs(x)
        y = self.output(y)
        return y

    def train(self, generator, epochs):
        for epoch in range(epochs):
            print(epoch)
            self.optimizer.zero_grad()
            x, y = generator.get_pairs()

            outputs = self(x)
            loss = self.loss(outputs, y)
            loss.backward()
            self.optimizer.step()

class PairGenerator:
    def __init__(self, text, vocabulary, window_size = 1):
        tokenizer = RegexpTokenizer(r'\w+')
        self.words = tokenizer.tokenize(text.lower())
        self.words = run_stemmer(self.words)
        self.words = list(map(lambda word: voc_index(word, vocabulary), self.words))
        self.words = [word for word in self.words if word is not None]
        self.window_size = window_size
        self.voc_size = len(vocabulary)

    def get_pairs(self):
        xs = list(map(lambda x: one_hot(x, self.voc_size), self.words))
        ys = []
        for index in range(len(self.words)):
            low = max(0, index - self.window_size)
            high = min(len(self.words) - 1, index + self.window_size)
            y = random.choice(self.words[low:high])
            ys.append(y)
        return torch.tensor(xs, dtype=torch.float), torch.tensor(ys, dtype=torch.long)

def load_vocabulary(path):
    vocabulary = []
    with open(path, 'r') as f:
        vocabulary = f.readlines()
        vocabulary = list(map(lambda x: x.strip(), vocabulary))
    return vocabulary


''' Returns a numpy array '''
def voc_index(stem, vocabulary):
    try:
        index = vocabulary.index(stem)
        return index
    except:
        return

def one_hot(index, length):
    result = [0 for _ in range(length)]
    result[index] = 1
    return result

voc = load_vocabulary(VOCABULARY_PATH)

text = '''Perioada ilegalistă
Nicolae Ceaușescu arestat de poliția din Târgoviște (1936)
TimbruNicolaeCeausescu.png

În noiembrie 1933 a devenit membru al Uniunii Tineretului Comunist din România, formațiune politică aflată în ilegalitate la acea vreme[19]. A fost arestat prima oară în 1933 pentru agitație comunistă în timpul unei greve. În 1934 a fost atras în Comitetul raional din Negru unde a lucrat până în august când a fost desemnat să muncească în mișcarea antifascistă. A făcut parte din Comitetul Na­țional antifascist și în Comitetul Central al tineretului antifascist. Au urmat încă trei arestări – pentru colectare de semnături în sprijinul eliberării unor muncitori feroviari acuzați de activitate comunistă și pentru alte acțiuni similare, dar a fost pus imediat în libertate. În urma acestor arestări, a fost etichetat de autoritățile vremii drept „agitator comunist periculos”, precum și „distribuitor activ de material de propagandă comunistă și antifascistă”.

După eliberarea din arest, Ceaușescu a dispărut pentru o vreme, el povestind în autobiografia sa de după război că a activat în rețelele comuniste din Oltenița și „regionala Prahova” (ceea ce în organizarea interbelică a PCdR însemna județele Prahova și Dâmbovița).[19]
Procesul de la Brașov și detenția la Doftana

Cert este că în 1936 Ceaușescu era secretar regional al UTC și încerca, împreună cu agitatorul polonez Vladislav (sau Vladimir) Tarnovski, să coaguleze celulele comuniste. În ianuarie 1936 cei doi au vizitat celula comunistă constituită în comuna Ulmi de lângă Târgoviște, încercând să-i atragă pe membrii ei cu funcții mai înalte în ierarhia comunistă. Întâlnirea a fost deconspirată de un informator al Siguranței, Ion Olteanu, iar Ceaușescu a fost din nou arestat împreună cu Tarnovski, Gheorghe Dumitrache (organizatorul celulei) și alți comuniști.[20] În cursul anchetei și interogatoriilor separate, Ceaușescu a rămas singurul care a refuzat să recunoască, împotriva tuturor evidențelor, activitatea subversivă. La sfârșitul lunii grupul a fost transferat la Palatul de Justiție din Brașov, unde a fost judecat. În perioada judecării procesului a fost încadrat în PCdR[19]. Ceaușescu a fost condamnat la doi ani și jumătate de închisoare (doi ani pentru acțiunile propriu-zise și șase luni pentru ultraj în urma protestelor vehemente la adresa curții). El și Tarnovski au primit cele mai mari pedepse din lotul de 13 activiști comuniști condamnați. Transferat ulterior la Închisoarea Doftana, Ceaușescu i-a întâlnit pe Vasile Luca, Alexandru Moghioroș și apoi pe Gheorghe Gheorghiu-Dej, Chivu Stoica și Gheorghe Apostol.[21] Propaganda comunistă avea să creeze multiple legende romanțate în jurul detenției la Doftana.
Ceaușescu (al doilea din stânga) în lagărul de la Târgu Jiu

Eliberat la termen în 1938, Ceaușescu a rămas în libertate doar doi ani, întrucât în 1939 a fost condamnat în lipsă la 3 ani de închisoare pentru continuarea propagandei comuniste, fiind din nou arestat în 1940. În această scurtă perioadă de libertate, a cunoscut-o pe Elena Petrescu, activistă comunistă din București.[22] Încarcerat la închisoarea din Jilava, Ceaușescu a continuat întâlnirile cu Elena, profitând de permisiunea primită din partea conducerii penitenciarului de a primi tratament stomatologic la Spitalul Militar.[23] Transferat în 1942 la Caransebeș și în 1943 la Văcărești, la terminarea detenției în 1943 nu a fost eliberat, în condițiile în care generalul Antonescu se ferea să elibereze activiști comuniști ce i-ar fi subminat regimul, ci a fost transferat în lagărul de la Târgu Jiu, unde erau aduși comuniștii. A fost eliberat la 4 august 1944.
Perioada postbelică

După cel de-al doilea război mondial, în timp ce controlul sovietic asupra României devenea tot mai pronunțat, Ceaușescu a fost numit secretar al Uniunii Tineretului Comunist – UTC - (1944-1945).[24]
Gheorghiu-Dej, Ceaușescu și delegații în februarie 1948

După preluarea puterii de către Partidul Comunist Român, în urma abdicării regelui Mihai I, la 30 decembrie 1947 a fost proclamată Republica Populară Română și în februarie 1948 a avut loc primul congres al PMR. Ulterior, la 13 mai 1948, Nicolae Ceaușescu a fost numit subsecretar de stat în ministerul Agriculturii,[25] în Guvernul Petru Groza (4), iar la 18 martie 1950, generalul-maior Ceaușescu a fost numit ministru adjunct la Ministerul Apărării Naționale și Șef al Direcției Superioare Politice a Armatei.[17][26] Nicolae Ceaușescu a devenit general în ianuarie 1950, deși nu făcuse armata.[27]
Ceaușescu în timpul procesului de colectivizare

În funcția de subsecretar de stat în ministerul Agriculturii a activat direct la cooperativizarea forțată a agriculturii și a ordonat reprimarea sau arestarea țăranilor care se împotriveau cooperativizării. În 1952, devine membru al Comitetului Central (CC) al Partidului Muncitoresc Român (PMR), la doar câteva luni după eliminarea „facțiunii moscovite” (condusă de Ana Pauker) din conducerea partidului. În 1954, Ceaușescu devine membru deplin al Biroului Politic al PMR, responsabil cu problemele de cadre, iar ulterior ajunge să ocupe poziția numărul doi în ierarhia PMR.[28]

În toamna anului 1956, aflându-se la Cluj, Ceaușescu a avut un rol important în reprimarea mișcărilor de simpatie față de revoluția ungară.
Gheorghiu-Dej și Hrușciov la Aeroportul Băneasa din București. Ceaușescu în plan secundar (stânga), iunie 1960
Elena Ceaușescu soția lui Nicolae Ceaușescu

La 4 decembrie 1957, având gradul de general-locotenent de armată (fiind șeful Direcției Superioare Politice a Armatei și adjunct al Ministrului Forțelor Armate), Ceaușescu a condus unitățile militare care au înăbușit răscoala țăranilor din Vadu Roșca (jud. Vrancea) care se împotriveau colectivizării forțate. Flancat de două tancuri, Ceaușescu ordonă personal deschiderea focului de pe mitralierele aflate în camioanele care însoțeau tancurile. 9 țărani sunt uciși de gloanțe (Aurel Dimofte, Ionuț Cristea, Ion Arcan, Dumitru Crăciun, Toader Crăciun, Stroie Crăciun, Dumitru Marin, Marin Mihai, Dana Radu) și alți 48 sunt răniți.[29][30][31][32][33][34][35][36][37][38] Varujan Vosganian, politician, economist și scriitor de origine armeană, relatează în cartea sa autobiografică „Cartea șoaptelor” întreaga desfășurare a evenimentelor.

    „Tancurile se opriră și odată cu ele și camioanele, care făcură un viraj și se proptiră cu spatele la baricadă, ridicând prelatele și scoțând la iveală, într-adevăr, țevile lungi și perforate ale mitralierelor. Din camioane coborâră câțiva ofițeri în uniformele Securității, iar în fruntea lor același bărbat scund, cu căciula militară și scurtă bleumarin. Ei se opriră în dreptul tancurilor. Atunci unii dintre oameni ieșiră în fața baricadei. Bărbatul mărunțel ridică mâna dreaptă și ei crezură că vrea să le vorbească. Clopotele amuțiră. Oamenii făcură un pas înapoi. Lângă Nițu Stan, Costică Arbănaș căzu în genunchi și-și desfăcu la piept, rupând-o, cămașa. Lângă el, Aurică Dimofte, Stroie Crăciun, și, strângând în mână toporul, Ionică Areaua. Apoi ceilalți veniră unul câte unul. Cocoțată pe cabina mașinii răsturnate, Dana lui Radu rămase încremenită, strângându-și basmaua la piept. Atunci se întâmplară câteva lucruri dintr-odată. Bărbatul acela, Ceaușescu, își lăsă brațul în jos cu o mișcare iute. Clopotul porni să bată din nou, acoperind șuierul gloanțelor, dar rămaseră focul stârnit de țevi și plumbii care umplură aerul. Primul căzu Aurel Dimofte, întâi în genunchi, privindu-și nedumerit palmele lipite de pieptul din care țâșnea sângele și apoi prăvălit, tot cu genunchii îndoiți, pe spate, împins de gloanțele ce continuau să i se îndese în trup. Dana lui Radu fu secerată cu atâta putere, încât țâșni în sus, ca o păpușă de câlți, și rămase câteva clipe în aer, proptită de gloanțe, înainte de a se prăbuși pe capotă, cu brațele desfăcute. Pe Costică Arbănaș, în genunchi, gloanțele îl feriră ca printr-o minune, dar rămase așa, neclintit, cu găvanele golite, într-un plâns pe care nici măcar nu și-l simțea. Nițu Stan se aruncă în țărână și se rostogoli spre margine, dar se întoarse să-l tragă pe Stroie Crăciun, care gemea întruna: „Stane, nu mă lăsa...”, până când sângele îi țâșni pe gură, sufocându-l.... Clopotul continua să bată... Mitralierele răpăiră clopotnița, dar clopotul continua să bată. Tancurile porniră încet, continuând să răpăie și spulberară baricada ca pe un mușuroi, scuturând peste blindajul lor laolaltă scânduri și trupuri. Răniții se târau din calea lor, ca să nu-i strivească șenilele. Mitralierele măturau acum doar clopotnița, se dădea o luptă gigantică între dangătul clopotului și șuierul gloanțelor în care clopotul, chiar dacă turla, cu tencuiala mușcată de gloanțe, sfârtecată și înăbușită în fumul alb al văruielii, rămăsese ca o scurteică zdrențuită, ieșea biruitor. Până când țeava unuia dintre tancuri se ridică încet și slobozi un obuz care ținti chiar în miezul clopotniței. Ionuț Cristea murise cu siguranță mai demult și clopotul luptase singur mai departe. Obuzul ucise și clopotul. Când dangătul tăcu, atunci tăcură și gloanțele. „Nu se mai termina, își aminteau unii, credeam că o să ne omoare pe toți”. „A ținut doar ca la zece minute, spuneau alții, a fost ca o grindină, ca o răpăială de vară.” ”
    — Varujan Vosganian , Cartea șoaptelor, 2009, pp. 256-272[39]

18 țărani au fost întemnițați pentru „rebeliune” și „uneltire contra ordinii sociale”, petrecând între 15-25 de ani de închisoare la Gherla și Aiud.[39]

După datele PMR-ului, între 1949-1952 au avut loc peste 80.000 de arestări de țărani, dintre care 30.000 finalizate cu sentințe de închisoare.[40]
Ceaușescu la conducerea României (1965—1989)
Articol principal: Epoca de aur-epoca Ceaușescu.
Articol principal: Republica Socialistă România.
Politica externă
Fragmente audio:

    Fragmente din discursul din 1968
    Meniu
    0:00
    Probleme în ascultarea fișierului? Consultați pagina de ajutor.


Întâlnirea președintelui american Richard Nixon și vicepreședintelui Gerald Ford cu Nicolae Ceaușescu în 1973
Ceaușescu petrecând timp cu Jacques Chirac pe litoralul românesc din Neptun (1975)
Nicolae Ceaușescu și soția sa cu împăratul Hirohito în timpul unei vizite în Tokyo din 1975
Cuplul prezidențial român este primit de către Elisabeta a II-a la Palatul Buckingham în iunie 1978
Ceaușescu cu Pol Pot, 1978
Ceaușescu este întâmpinat de regele Juan Carlos I al Spaniei în Madrid, 1979
Relația cu Pactul de la Varșovia

În primii ani de regim, Ceaușescu s-a îndepărtat de linia de obedientă față de Moscova a predecesorilor săi. Astfel, la puțini ani după preluarea puterii, Ceaușescu nu doar că a refuzat să participe la intervenția trupelor Pactului de la Varșovia în Cehoslovacia din 1968, ci chiar a condamnat-o explicit într-un discurs public, ținut la 21 august 1968. Prin discursul său, Ceaușescu a indus teamă, devenind astfel un adevărat erou.[41] Teama a fost exprimată de o frază rostită în fața a 100.000 de oameni: „se vor găsi mâine unii care să spună că și aici, în această adunare, se manifestă tendințe contrarevoluționare.”

La începutul carierei sale ca șef al statului, Nicolae Ceaușescu s-a bucurat de o oarecare popularitate, adoptând un curs politic independent față de Uniunea Sovietică. În anii 1960 Ceaușescu a pus capăt participării active a României în Pactul de la Varșovia, deși formal țara va continua să facă parte din această organizație până la dizolvarea acesteia (1 iulie 1991). Pactul de la Varșovia și NATO au fost părți în Războiul rece pentru mai mult de 35 de ani. La 20 august 1968, Cehoslovacia a fost invadată de către trupele Pactului de la Varșovia, cu excepția României și Iugoslaviei. Prin refuzul său de a permite armatei române să ia parte la invazia Cehoslovaciei alături de trupe ale țărilor membre ale Tratatului de la Varșovia și o atitudine de condamnare publică activă a acestui act, Ceaușescu reușește pentru o vreme să atragă atât simpatia compatrioților săi, cât și pe cea a lumii occidentale.
Relația cu Statele Unite

În timpul administrației Nixon, Statele Unite au manifestat o oarecare deschidere față de România, pe fondul răcirii relațiilor dintre România și URSS după invazia Cehoslovaciei de către URSS din 1968, invazie intens criticată de președintele român. Nixon a vizitat România pe 2 august 1969, iar în urma discuțiilor purtate cu președintele român, Nixon și-a făcut impresia că „Ceaușescu este un marxist stalinist dur, iar discuțiile cu el exclud platitudinile uzuale diplomatice.”[42][43]

Vizita președintelui Nixon în România a făcut parte din turneul mondial al președintelui american început în luna iunie în Guam, în care a făcut cunoscute principiile a ceea ce avea să fie denumită ulterior „Doctrina Nixon”.[44] Ea a reprezentat prima vizită a unui președinte american într-o țară comunistă, fapt care a provocat reacții ostile, atât din partea Uniunii Sovietice cât și a Taiwanului, pe atunci deținând locul Chinei în Consiliul de Securitate al ONU. Astfel Moscova a trimis un avertisment clar României prin intermediul ministrului de externe Andrei Gromîko, care a precizat că „Doctrina Brejnev” era valabilă pentru toți membrii Tratatului de la Varșovia și că acesta „nu va permite niciodată să se aducă atingere securității statelor semnatare și cuceririlor socialismului din aceste țări”, accentuând explicit calitatea de membru a României. [45] La rândul lor, naționaliștii chinezi ai lui Cian Kai-și i-au chestionat pe oficialii americani dacă „vizita președintelui Nixon în România va avea implicații pentru relațiile SUA cu China comunistă și dacă SUA doreau ca România să intermedieze îmbunătățirea contactelor lor cu Pekinul”.[46]

Pe parcursul vizitei Nixon i-a solicitat lui Nicolae Ceaușescu ca România să joace un rol de mediator între România și China.[47] După vizită, oficialitățile americane apreciau că la acel moment „suntem pe cale să dezvoltăm o relație specială cu România”.[48] Faptul că Statele Unite ale Americii considerau relația cu România ca utilă din punct de vedere politic, „ca un ghimpe în coasta Uniunii Sovietice”, avea să ducă la o dezvoltare a sa pe perioada mandatelor președintelui Nixon. Astfel, Nicolae Ceaușescu a efectuat o vizită de răspuns în SUA, în octombrie 1970. A urmat acordarea de către partea americană a unei serii de favoruri economice, culminând cu acordarea „clauzei națiunii celei mai favorizate.” Totodată, SUA a sprijinit intrarea României într-o serie de organisme internaționale cum ar fi Acordul General pentru Tarife și Comerț - G.A.T.T., în 1971, sau Fondul Monetar Internațional și Banca Internațională pentru Reconstrucție și Dezvoltare, în 1972.”[49]»

În contextul relațiilor tensionate dintre România și Uniunea Sovietică și al deschiderii administrației Nixon față de România în acea perioadă, Nicolae Ceaușescu dorea să cumpere din SUA rachete antiaeriene și antitanc (Stinger, Redeye și TOW).[43][50] Pe fondul deschiderii SUA inițiate de administrația Nixon, Nicolae Ceaușescu a făcut o vizită în Statele Unite în anul 1973,[51] iar România comunistă a obținut, în 1975, clauza națiunii celei mai favorizate, printr-o serie de concesii făcute Washingtonului, inclusiv acceptul de a permite emigrarea evreilor către Israel sau Statele Unite ale Americii.[52]
Relația cu Vaticanul

În data de 26 mai 1973, în cursul unei vizite oficiale în Italia, Ceaușescu a fost primit în audiență particulară de către papa Paul al VI-lea, ocazie cu care Ceaușescu a afirmat cu privire la chestiunea Bisericii Române Unite, interzisă cu 25 de ani în urmă, că o socotește închisă pentru totdeauna, care pentru autoritățile române nu există.[53] Anterior ambasadorul Cornel Burtică s-a întâlnit de mai multe ori cu Agostino Casaroli, ministrul de externe al Vaticanului, ocazii cu care cei doi au ajuns la un acord în acest sensul reglementării situației Bisericii Române Unite.[54] Nicolae Ceaușescu s-a arătat dispus la o ameliorare a relațiilor dintre România și Sfântul Scaun doar cu condiția „totalei abandonări de către Vatican a problemei fostului cult greco-catolic”, fapt neacceptat de Vatican.[55]
Politica internă și politica economică

La trei zile de la moartea lui Gheorghiu-Dej, în martie 1965, Ceaușescu preia funcția de secretar general al Partidului Muncitoresc Român (acesta era numele Partidului Comunist Român la acea vreme, după asimilarea forțată, în 1948, a unei aripi a Partidului Social Democrat). Una dintre primele acțiuni ale lui Ceaușescu, odată ajuns la putere, a fost redenumirea Partidului Muncitoresc Român în Partidul Comunist Român. În același timp, el afirmă că România a devenit o țară socialistă și decide schimbarea numelui oficial al țării din Republica Populară Română (R.P.R.) în Republica Socialistă România (R.S.R.). Grupul „baronilor” (Maurer, Bodnăraș, Stoica), Ion Gheorghe Maurer în primul rând, nu a socotit ascensiunea lui Ceaușescu drept periculoasă și a permis încălcarea articolului 13 din statutul abia adoptat la congresul al IX-lea al PCR, care interzisese cumulul de funcții și a îngăduit secretarului general al PCR (ambele denumiri au fost adoptate la numitul congres) să ocupe, în 1967, funcția de președinte al Consiliului de Stat. Ceaușescu a lărgit continuu atribuțiile Consiliului de Stat, subordonând atât Consiliul Economic, creat în 1967 cât și pe cel al apărării, creat în 1968. Pe nesimțite Consiliul de Stat s-a transformat dintr-un organ onorific într-unul de conducere efectivă, dublând sau preluând din atribuțiile guvernului condus de Maurer. Pe de altă parte, în 1969, la congresul al X-lea, două treimi din membrii Prezidiului Permanent fuseseră promovați după 1965 prin grija lui Ceaușescu. Preluarea puterii era acum desăvârșită. [56]

A existat o dispută între Ceaușescu și Maurer asupra căilor de dezvoltare a societății românești. Disputa, despre care se știe încă foarte puțin, avea în centru problema ritmului de industrializare pe care Ceaușescu îl dorea accelerat, cu un accent și mai sporit pe industria grea și pe care primul-ministru Maurer l-ar fi vrut mai măsurat, fără neglijarea industriei bunurilor de consum, în acord cu resursele interne, umane, naturale și tehnologice ale țării. Maurer a pierdut această dispută.[57] La numai câteva luni de la plenara din noiembrie 1971, care-și însușise pe deplin tezele din iulie 1971, lansate de Ceaușescu la întoarcerea din China, Maurer cu linia sa economică, de orientare relativ liberală, era criticat indirect dar public de secretarul general. El este acuzat de neîncredere în politica partidului și de defetism economic. Maurer a fost îndepărtat în martie 1974 după alegerea lui Ceaușescu în funcția de președinte.[58] Prim-ministru devine Manea Mănescu. La congresul al XI-lea din noiembrie 1974 Maurer își pierde și locul în Comitetul Central.[59]

Pe de altă parte în aprilie 1972 Ceaușescu anunță că rotirea cadrelor va deveni un principiu de bază al partidului și promisiunea devine realitate: demnitarii statului și activiștii de toate gradele sunt schimbați periodic, în funcție de bunul plac al secretarului general, împiedicând astfel formarea unei baze proprii de putere. În iunie 1973 intră în Comitetul Executiv și Elena Ceaușescu, care avea să devină o a doua putere în stat.[60]

La 28 martie 1974 Marea Adunare Națională a instituit funcția de președinte al Republicii Socialiste România, iar Nicolae Ceaușescu a fost ales în unanimitate și devine astfel primul președinte al României. Prin politica sa externă, condusă cu abilitate, a încercat să se elibereze de dominația sovietică, atrăgând simpatia și aprecierile unor mari lideri politici ca Charles de Gaulle și Richard Nixon. În realitate, singurul scop era consolidarea puterii dictatoriale. În CAER, la indicația lui, delegațiile române se opun la toate propunerile venite din partea URSS. De exemplu, România este una dintre cele doar două țări comuniste europene care au participat la Jocurile Olimpice organizate la Los Angeles, în Statele Unite ale Americii în 1984. De asemenea, România a fost singura țară din blocul răsăritean, cu excepția URSS, care la acea vreme, întreținea relații diplomatice cu Comunitatea Europeană, cu Israelul și cu R. F. Germania. Un tratat incluzând România pe lista țărilor favorizate de Comunitatea Europeană este semnat în 1974, iar în 1980 este semnat un acord vizând schimburile de produse industriale între România și Comunitatea Europeană. Acest fapt a determinat vizitarea oficială a României de către doi președinți ai Statelor Unite ale Americii (Nixon și Ford).

După anul 1974, legăturile dintre Nicolae Ceaușescu și Leonid Ilici Brejnev au cunoscut o oarecare îmbunătățire, această apropiere culminând în 1976 cu vizita președintelui român în Basarabia și Crimeea și cu vizita liderului sovietic la București. Există informații (Vlad Georgescu, 1992, op. cit. p. 298) că pentru a face pe placul conducerii sovietice, Bucureștiul a transmis rușilor date despre activitatea unor naționaliști basarabeni care se adresaseră președintelui Ceaușescu cu speranța de a fi sprijiniți. Ca urmare, ei au fost arestați și condamnați la detenție în lagărele din Siberia, înainte de a li se îngădui, unora dintre ei, să emigreze definitiv dincoace de Prut.

În ciuda cursului independent în relațiile politice internaționale, introdus încă de Gheorghiu Dej, Ceaușescu se opune cu încăpățânare introducerii oricăror reforme liberale pe plan intern. În anii 1980, după venirea lui Mihail Gorbaciov la conducerea Uniunii Sovietice, opoziția lui Ceaușescu față de linia sovietică este dictată în principal de rezistența lui față de destalinizare. Securitatea continuă să își mențină controlul draconic asupra mediilor de informare și înăbușă în fașă orice tentativă de liberă exprimare și opoziție internă.

Întreruperea căldurii

Temperaturile din case ajung iarna între 5-12 grade în apartamentele celor mai mulți dintre românii care stau la bloc. Raportul Comisiei Prezidențiale pentru Analiza Dictaturii Comuniste din România (pag 423) face referire la „obligarea populației la un trai în condiții insuportabile, la temperaturi sub 10 grade C”.[61][62]

Lipsa apei calde

Apa caldă este livrată din ce în ce mai rar, cam două ore zilnic iar adesea la etajele superioare aceasta nu ajungea deloc.[61]

Întreruperea curentului

Lumina începe să fie întreruptă în fiecare zi cel puțin o oră, seara. „Din ianuarie 1982 s-a început limitarea distribuirii energiei electrice către populație; până la căderea regimului comunist în 1989, livrarea curentul electric către populație se oprea de câteva ori pe zi, fără niciun program ori logică aparente și fără anunțarea prealabilă a consumatorilor casnici. Simultan, cetățenii erau îndemnați să economisească energia electrică prin scoaterea din funcțiune pe timpul iernii a frigiderelor, prin neutilizarea mașinilor de spălat și a altor bunuri electrocasnice sau prin nefolosirea ascensoarelor”.[63] Benzina, deși raționalizată, devine greu de găsit. Consumul de energie pentru populație a scăzut forțat cu 20% în 1979 și 1982, apoi cu 50% în 1983, iar în 1985 cu încă 50% față de anii precedenți.[64]

Lipsa principalelor bunuri de consum

Articol principal: Republica Socialistă România#Lipsa principalelor bunuri de consum.

În perioada 1981-1989 în magazine nu se găseau în mod curent carne și produse din carne, ouă, lapte și produse lactate, fructe de import, cafea, ciocolată, orez, făină. Oamenii se hrăneau în mod obișnuit cu legume, fructe și pește, toate autohtone.[65][66][67][68][69] „Lipsurile de tot felul, mai ales cele alimentare au devenit acute și cronice din toamna lui 1981”.[70]

Prețuri comparative 1985-2010

Prețurile raportate la salarii erau mai mari în 1985 față de 2010 la principalele alimente de bază și anume: carne de vită cu oase (113%), carne de porc cu oase (104%), ouă (45%), orez cu bob lung (68%), zahăr (41%), cafea (420%), unt (51%), făină (12%), ulei (40%), portocale (98%). Existau câteva alimente la care prețurile erau mai mici în 1985 față de 2010 și anume: cartofi (61%), mere (74%), ceapă (16%), pește (16%), brânză, când se găsea (50%).[71][72]

La sfârșitul anilor 80 întreținerea unui apartament de 3 camere – 3 persoane, într-un cartier bucureștean mărginaș, era de circa 300 de lei pe lună, adică 10% din salariu mediu. În 2013 ea are circa aceeași valoare, 300 lei, ceea ce înseamnă 18% din salariu mediu. Dar în 2013 există căldură în case și apă caldă.

O Dacie costa 70 000 lei, adică 23,3 salarii medii, în 2013 un Logan costa 30 000 lei, adică 18,68 salarii medii.

În anii 80, un apartament de 3 camere în Drumul Taberei costa 160.000 de lei – 53,3 salarii medii, iar în 2013 prețul apartamentului respectiv (cu termopane, ușă metalică, gresie etc.) era de circa 242.000 lei – 150,68 salarii.[73]

Datoria externă

În ciuda regimului său dictatorial, relativa sa independență față de Moscova are drept rezultat o atitudine binevoitoare (deși departe de a fi dezinteresată sau neprofitabilă) din partea statelor occidentale. Regimul Ceaușescu beneficiază de unele împrumuturi pentru finanțarea programelor sale economice. În anii „Epocii Ceaușescu” se construiesc Metroul din București, Canalul Dunăre-Marea Neagră, zeci de mii de noi blocuri de locuințe. În ultimă instanță, datoria creată a devenit o povară pentru economia românească, între 1971-1982, datoria externă crescând de la 1,2 miliarde $ la aproape 13 miliarde $. În 1982, veniturile comerțului exterior al României au scăzut cu 17% față de anul precedent. Ceaușescu s-a văzut pus în situația de a nu-și putea plăti creditorii occidentali, țara fiind declarată în incapacitate de plată.[74]

Ceaușescu a dispus achitarea rapidă a datoriilor externe, fără a mai lua noi credite. În acest scop, o mare parte a producției agricole și industriale a țării ia calea exportului, privând astfel populația până și de cele mai elementare alimente și bunuri de consum. Începând cu anii 1986-1987 se instituie raționalizarea produselor de bază, iar benzina și alimente ca pâinea, uleiul, zahărul, făina, orezul au început să fie distribuite pe bonuri sau cartele.[75] Bunurile destinate exportului au standarde de calitate ridicată și sunt vândute de obicei în pierdere, la prețuri de dumping. Bunurile destinate consumului intern sunt de calitate inferioară, așa că oamenii de rând sunt bucuroși atunci când pot cumpăra bunuri refuzate la export din motive calitative.

Plata întregii datorii externe, în valoare nominală de 60 de miliarde de lei (10 miliarde dolari), se încheie în primăvara lui 1989, cu câteva luni înaintea căderii regimului comunist.[76] Ceaușescu urmărea organizarea unui referendum prin care să se introducă în constituția României interdicția de a contracta împrumuturi externe. Pentru a evita deprecierea leului, Ceaușescu a continuat exporturile excesive, acumulând aur în Banca Națională. Se spune totuși că Ceaușescu, ar fi avut de gând să facă leul convertibil încă de prin anii '70, deci cu aproximativ 30 de ani mai devreme față de când acest lucru s-a înfăptuit.[77]

Emigrarea etnicilor germani

Potrivit declarațiilor lui Heinz-Günter Hüsch, avocatul care a reprezentat RFG în negocierile cu România în perioada 1968-1989, în martie – decembrie '70, s-a negociat plecarea a 4.000 de etnici germani din România. Pentru '71 – 6.000 de etnici germani, la fel în 1972, în 1973 - 4.000 de etnici germani. Decretul Consiliului de Stat nr.402 din 1 noiembrie 1982[78] prevedea următoarele: „Persoanele care cer și li se aprobă stabilirea definitivă în străinătate sînt obligate să plătească integral datoriile pe care le au față de stat, unități socialiste și alte organizații. De asemenea, au obligația să achite în întregime pensiile de întreținere și orice alte datorii față de persoanele fizice. Persoanele cărora li s-a aprobat stabilirea definitivă în străinătate sînt obligate să restituie, în valută, statului roman, cheltuielile efectuate pentru școlarizare, specializare și perfecționare, inclusiv bursele, în cadrul învățămîntului liceal, superior, postuniversitar și doctorat.” Sumele plătite de statul german pentru compensarea cheltuielilor de școlarizare erau împărțite pe categorii: 1.800 de mărci germane pentru persoanele cu studii medii, 5.500 de mărci germane pentru studenți și 7.000 de mărci germane pentru cei cu studii superioare încheiate. În 1988 suma cerută pentru fiecare persoană era unică – 8.950 de mărci. Banii ajungeau într-un cont al Băncii Române de Comerț Exterior. „În 99% din cazuri, banii au fost folosiți pentru plata datoriei externe a României”, a arătat Florian Banu, cercetător în cadrul CNSAS, care a publicat un studiu pe această temă. În urma negocierilor purtate de Heinz-Günter Hüsch cu reprezentanții Securității, din România au plecat între 1968 și 1989 peste 200.000 de etnici germani.[79][80]

Politica demografică și sanitară

Articol principal: Politica demografică a regimului Ceaușescu.

Stimularea forțată a sporului natural al populației a reprezentat una din prioritățile regimului Ceaușescu. Un element important al acestei politici este reprezentat de abrogarea, în 1966, a decretului din 1957 care permitea avorturile la cerere (la acea dată, avortul nu era permis decât în unele țări comuniste). Prin decretul 770/1966 se permitea avortul terapeutic efectuat în primele trei luni de sarcină numai pe baza unor stricte indicații medicale și doar în cazuri excepționale se accepta sacrificarea fătului și până la șase luni. Acest decret cu putere de lege a fost înăsprit prin Decretul 441 din 26 decembrie 1985, care permitea avorturile doar în cazul femeilor care au depășit vârsta de 42 de ani sau care au dat deja naștere la cel puțin cinci copii. În teorie, mamele a 5 sau mai mulți copii ar fi avut dreptul la privilegii substanțiale. Mamele „eroine” a 10 sau mai mulți copii aveau dreptul să primească gratuit din partea statului un automobil ARO, transportul cu trenul, precum și o vacanță pe an într-o stațiune balneară.

În timp ce sporul populației era încurajat, mii de copii erau abandonați în orfelinate. Se estimează că, la începutul anului 1990, în România orfelinatele „adăposteau” aproximativ 100.000 de copii[81] în condiții de trai tragice.[82] Rata mortalității infantile rămânea cea mai mare din Europa.[83]

În perioada 1988-1992, mii de copii din toată România au fost infectați cu HIV. În majoritatea cazurilor a fost vorba despre o combinație de nepricepere medicală, indiferență și dotări precare. Parțial cuantificabilă ani mai târziu, „rețeta” exploziei SIDA din România este construită în jurul a două tragedii: injecții cu seringi expirate și microtransfuzii de sânge.[82] Regimul Ceaușescu a ignorat problema epidemiei de HIV/SIDA pe motive ideologice, considerând-o specifică societății capitaliste. În România anilor 1980 nu se practica testarea HIV a donatorilor de sânge și a sângelui pentru transfuzii. Acest fapt, la care se adaugă folosirea de ace de transfuzie inadecvat sterilizate în orfelinate, a condus România pe locul doi în topul infecțiilor pediatrice cu HIV în Europa (în anul 2004 s-a asigurat medicația și tratamentul pentru 6000 de bolnavi de HIV SIDA).[84]

Programul de sistematizare rurală

Articol principal: Sistematizare (istoria României).

Cu prilejul vizitelor efectuate în 1971 în China și Coreea de Nord, Ceaușescu e fascinat de ideea transformării naționale totale, așa cum era ea prefigurată în programul Partidului Muncitoresc Coreean și deja pusă în aplicare sub egida Revoluției Culturale din China. La scurtă vreme după întoarcerea sa în țară, Ceaușescu începe transformarea sistemului autohton după modelul nord-coreean, influențat fiind de filozofia Juche a președintelui Kim Ir Sen. Cărți nord-coreene pe această temă sunt traduse în română și distribuite pe scară largă în țară.
Vizita oficială a lui Nicolae Ceaușescu și a Elenei Ceaușescu în Republica Populară Chineză. Vizita protocolară la Ciu Enlai - iunie 1971
Nicolae Ceaușescu și Kim Ir Sen cu prilejul vizitei delegației de partid și de stat în R.P.D. Coreea, 15 iunie 1971

Începând cu 1972 Ceaușescu a trecut la punerea în aplicare a unui proiect de „sistematizare” a localităților urbane și rurale. Prezentat de către mașina de propagandă ca fiind un pas major pe calea „construirii societății socialiste multilateral dezvoltate”, programul debutează la sate prin demolări în masă ale gospodăriilor țărănești și strămutarea familiilor afectate în apartamente de bloc.[85] Demolarea satelor este de fapt o încununare a politicii de industrializare forțată, care a dus la destructurarea societății rurale românești. Apogeul acestui program a fost însă reprezentat de demolarea a numeroase monumente istorice, inclusiv biserici și remodelarea Bucureștiului în stil ceaușist (peste o cincime din centrul capitalei a fost afectată). Casa Poporului (actualmente sediul Parlamentului) este reprezentativă. 400 de arhitecți în frunte cu arhitectul-șef, Anca Petrescu, au proiectat clădirea. Au fost rase de pe fața pământului trei cartiere - Uranus, Antim și parțial Rahova - și 17 biserici. Zilnic, peste 20.000 de muncitori lucrau în trei schimburi. În cinci ani, a răsărit ca din pământ a doua clădire, ca mărime, din lume, după Pentagon, cu un volum de 2.500.000 mc, cu peste 7.000 de încăperi, unele de mărimea unui stadion. Nota de plată a fost de circa 2 miliarde dolari în condițiile în care poporul era confruntat cu frig și grave lipsuri alimentare.[16] Proteste venite din partea unor organizații neguvernamentale internaționale au jucat un rol important în stăvilirea acestor planuri megalomane și probabil în salvarea a ceea ce a mai rămas din monumentele istorice aflate pe lista neagră a dictatorului.

Termocentrala de la Anina

Termocentrala de la Anina a fost una dintre ideile de suflet ale lui Ceaușescu. Ea a costat 1 miliard de dolari[86] (9 miliarde de lei la vremea respectivă, jumătate cât a costat Casa Poporului). 8000 de muncitori au fost aduși din toate colțurile țării. În aproape 100 de blocuri trăiau oameni din Moldova, Oltenia și Maramureș. Se intenționa producerea de energie electrică prin arderea șisturilor bituminoase în combinație cu cărbune, păcură ori gaz. Angajații termocentralei de la Anina aveau salarii de cca 13 000 lei, de patru ori cât medicii din București. Construcția a început în 1976, a început să funcționeze în 1984 (dar fără a produce vreodată curent), a fost închisă în 1988, a fost vândută la fier vechi în 2003. Termocentrala de la Anina a fost un eșec foarte costisitor.[87]

Fuga lui Pacepa

În 1977 Ion Mihai Pacepa, pe atunci director adjunct al Departamentului de Informații Externe (spionaj) al Securității, părăsește țara și obține azil politic în Statele Unite. Plecarea lui Pacepa dă o grea lovitură regimului comunist, iar încercările lui Ceaușescu de a restructura Securitatea nu reușesc să-i îndepărteze pe toți colaboratorii lui Pacepa și să limiteze pierderile. În cartea sa Red Horizons: Chronicles of a Communist Spy Chief (ISBN 0-89526-570-2) (în românește: Orizonturi roșii: Cronicile unui spion comunist), apărută în 1986, Pacepa dezvăluie detalii despre colaborarea regimului Ceaușescu cu organizații teroriste arabe, activitățile intense de spionaj contra industriei americane, precum și planurile bine ticluite de a atrage susținere politică din partea lumii occidentale. După plecarea lui Pacepa, izolarea României pe plan internațional se accentuează, paralel cu o înrăutățire a situației economice. Serviciile străine de informații își intensifică eforturile de infiltrare a Securității, în timp ce controlul lui Ceaușescu asupra aparatului începe să se clatine.[88][89]

Învățământul

O atenție specială a fost acordată reorganizării până la dezorganizare a învățământului, aproape toate progresele perioadei precedente fiind anulate. Legea educației din 1978 a introdus principiul drag președintelui al integrării învățământului cu producția, alungând practic din școli multe discipline și punând liceele și facultățile sub tutela unor uzine și dându-le planuri de producție. Din punct de vedere practic rezultatele acestei legături dintre învățământ și producție sunt neglijabile, greutățile uzinelor tutelare făcând de cele mai multe ori activitatea productivă a școlilor și facultăților irelevantă pentru economia națională. Învățământul a ajuns o instituție de pe băncile căreia elevii și studenții ies cu o formație intelectuală redusă în multe domenii de activitate. Numărul studenților era în continuă scădere. A fost reintrodusă obligativitatea prezentării unei recomandări din partea UTC pentru intrarea în facultățile de științe sociale. Cadrele didactice au fost epurate începând din anul 1974 când președintele țării a declarat că „nu poate lucra în învățământul superior acela care se sustrage de la activitatea de educare a tinerei generații în spiritul concepției marxist-leniniste, al programului partidului nostru”. De atunci această poziție a fost extinsă la învățământul de toate gradele. Din 1975, admiterea la doctorat nu s-a mai putut face decât cu aprobarea comitetului municipal de partid, această autoritate fiind transferată ulterior unei comisii speciale a Comitetului Central. Clasa conducătoare era hotărâtă să îngăduie accesul la învățământul superior numai persoanelor care i se păreau de încredere și pe care nădăjduia să le poată controla.[90]

Dărâmarea de biserici și mănăstiri

Întrevederea dintre Nicolae Ceaușescu (flancat de Manea Mănescu și Ștefan Voitec) și patriarhul Iustin Moisescu,
București, 18 iunie 1977

Nicolae Ceaușescu a ordonat dărâmarea de biserici și mănăstiri, între care Biserica Văcărești și Mănăstirea Văcărești (1716), Mănăstirea Cotroceni (1679), Mănăstirea Mihai Vodă (1594) sau Biserica Sf. Vineri (1854) pentru a face loc Casei Poporului. În total au fost distruse în București 23 de biserici.[91] Iată lista lor:

    Biserica Sf. Nicolae-Sârbi, începutul secolului XVI, demolată în 1985.
    Biserica Crângași (1564) și cimitirul adiacent, distruse în 1986.
    Biserica Alba-Postavari (1568), cu picturi murale de Anton Serafim, demolată în martie 1984.
    Biserica Sf. Nicolae-Jitnita (1590) din Calea Văcărești, demolată în iulie 1986.
    Clădirea Mănăstirii Mihai Vodă, 1591, demolată în 1984.
    Biserica Spirea Veche, secolul XVI, reînnoită în secolul XVIII, demolată în aprilie 1984.
    Biserica Enei (1611), avariată de o macara în timpul lucrărilor de reconstrucție după cutremurul din 1977 și demolată în primăvara aceluiași an. Acest lăcaș de cult cu un ansamblu important de pictură murală a fost prima victimă a demolărilor regimului ceaușist.
    Biserica Sf. Vineri-Hereasca din secolul XVII, demolată în iunie 1987, doar la câțiva ani după renovare. Biserica era împodobită cu picturi de Dumitru Belizarie.
    Biserica Sf. Spiridon-Vechi din secolul XVII, demolată în iulie 1987. În timpul demolării a fost furată icoana dăruită bisericii de către Patriarhul Silvestru al Antiohiei la 1748.
    Mănăstirea Cotroceni din 1679, cu biserica din 1598, demolată în 1985.
    Biserica Olteni, ctitorită în 1696, demolată în iunie 1987. În 1821, în timpul luptelor dintre eteriști și otomani, biserica servise arnăuților drept loc de rezistență și fusese avariată de bombardamente. Între 1863 și 1865 biserica fusese restaurată în stil neogotic. Picturile murale executate de Gheorghe Tattarescu au fost parțial distruse, parțial furate în timpul demolării.
    Aripile de nord și de est ale Mănăstirii Antim (1713-1715), demolate în 1984.
    Mănăstirea Văcărești (1716-1722), cea mai însemnată mănăstire din București, demolată între 1984 și 1987. Dintr-o suprafață de cca 2.500 m² de frescă datând din timpul edificării au putut fi salvați de către prof. Dan Mohanu și studenții săi de la Institutul de Arte Plastice Nicolae Grigorescu doar cca 140 m². Pictura murală care împodobea paraclisul locului de închinare a voievodului a fost aproape complet distrusă, cu excepția unor fragmente cu icoane sau scene biblice care au fost probabil furate de muncitorii șantierului de demolare.
    Biserica Bradu Staicu, 1726, restaurată în 1875 de arhitectul Al. Freiwald, demolată în octombrie 1987. Odată cu biserica a dispărut pilonul mesei altarului, considerat a fi mai vechi decât biserica.
    Biserica Mănăstirii Pantelimon, 1750, demolată în 1986.
    Biserica Izvor, 1785, demolată în 1984.
    Biserica Sf. Troita-Izvor, 1804, descrisă de Barbu Ștefănescu Delavrancea în nuvela Hagi-Tudose, demolată în octombrie 1987. Odată cu demolarea au dispărut numeroase obiecte de cult.
    Biserica Gherghiceanu, 1939, demolată în 1984.
    Biserica Crângași 2, 1943, demolată în 1982.
    Biserica Mărgeanului, 1946, demolată în 1981.
    Biserica Doamna Oltea, 1947, demolată în 1986.[92]

Grație și eforturilor lui Eugen Iordăchescu, inginer în domeniul translatării de clădiri, au fost salvate de la demolare printre altele: Biserica Mihai Vodă, Biserica Schitul Maicilor (1726, din vremea Voievodului Nicolae Mavrocordat), Biserica Sfântul Ilie Rahova (1706, cu picturi de Gheorghe Tattarescu, Palatul Sinodal din incinta Mănăstirii Antim și altele. Eugen Iordăchescu a asigurat translatarea a 12 biserici de interes major, 10 în București și două în afara lui.[93] Pentru că muncitorii au refuzat să dărâme Biserica Sf. Vineri, autoritățile comuniste au adus pușcăriașii care au dărâmat biserica în iunie 1987.[91]

Controlul cultelor religioase

Toate cultele religioase au fost infiltrate cu agenți ai Securității și s-au aflat sub controlul strict al Departamentului Cultelor. Inclusiv Biserica Română Unită cu Roma, care oficial nu exista, era urmărită de Direcția I a Securității, care în anul 1989 deținea 263 de informatori în rândul clerului greco-catolic, care se cifra la 586 de persoane (episcopi, preoți și călugări).[94]

Lichidarea instituțiilor culturale

Ceaușescu și Iliescu, jucându-se cu cercurile, 1976

În ceea ce privește istoriografia propriu-zisă, transferarea sediului ei la Academia Ștefan Gheorghiu și la Institutul de Istorie al Partidului a lichidat-o practic ca știință. Academia Română a fost lichidată ca instituție de cercetare, toate instituțiile i-au fost luate, noii membri au fost aleși aproape exclusiv din rândul activiștilor culturali de partid, în frunte cu soția președintelui. Foarte prestigiosul Institut de Matematică a fost desființat în 1975, Institutul de Pedagogie a avut aceeași soartă în 1982. Au fost de asemenea desființate numeroase institute tehnice.[95]
Perioada autoritară și cultul personalității
Afiș propagandistic pe Calea Moșilor (București, 1986)
Ceaușescu în vizită la Sibiu, iunie 1967
Adunare Piața Palatului August 1968
Ștefan Voitec înmânându-i lui Nicolae Ceaușescu sceptrul prezidențial în 1974 [96]
Articol principal: Cultul personalității lui Nicolae Ceaușescu.

Pentru a defini ceea ce înseamnă cultul personalității trebuie să avem în vedere doua aspecte. Un prim aspect este legat de partea publică, și anume campania propagandistică care a fost în totalitate controlată și dirijată, această campanie de propagandă are în centru un singur individ, în cazul de față pe Nicolae Ceaușescu. Mass-media, televiziunea, radoul, cărțile precum și manifestațiile publice joacă un rol important în această privință, ele transmițând informații care au scopul  să-l ridice în slăvi pe conducător și să ii arate caracterul său extraordinar.

În al doilea rând, pe lângă această campanie propagandistică se constituie și o structură politică în care sunt captați doar “oameni de încredere “,( crearea unei baze personale de putere) de altfel baza politică constituie în fond fundația propagandei. De altfel, cultul personalității reflectă  situația politică existent în stat, ci anume faptul că întreaga putere este concentrate în mâinile  unui singur individ, acesta fiind conducătorul statului sau al partidului.

Același structură și atmosferă  care a predominat în timpul lui Gheorghe-Gheorghiu-Dej a fost adoptată și de către Nicolae Ceaușescu. Unitatea  conducerii PRM s-a datorat în cea mai mare măsură loialității personale a membrilor față de lider, această loialitate se bazează pe faptul că aceștia împărtășeau opțiuni politice comune. Pe de altă parte, unitatea partidului și a conducerii în jurul liderului a constituit o modalitate de protective  împotriva vreunui posibil amestec sovietic.

.[97]

Începând cu anii ’70, Ceaușescu devine obiectul unui cult al personalității tot mai pronunțat, nemaiîntâlnit în Europa de la moartea lui Stalin.[84] În acest context, poeții proletcultiști joacă un rol important. Titulatura completă, sub care era adresat de presa vremii includea funcțiile sale politice și statale: „Nicolae Ceaușescu, secretar general al Partidului Comunist Român, președintele Republicii Socialiste România, comandant suprem al forțelor armate”. Deseori se adăugau și apelative precum „genialul cârmaci”, „cel mai iubit fiu al poporului român”, „patriot înflăcărat” „personalitate excepțională a lumii contemporane”, „luptător pentru cauza dreptății și păcii, și socialismului”, „geniul Carpaților”, „marele conducător”. Primul volum omagial i-a fost dedicat în 1973. Fostul ucenic muncitor nu mai era așezat doar în rândul „eroilor clasei muncitoare”, ci el începe să fie văzut la capătul unui șir lung de principi, regi, voievozi, de unde i se putea revendica legitimitatea. Activiștii culturali au mers până într-acolo încât descoperă în apropierea Scorniceștilor, satul natal, rămășițele unui prim homo sapiens european, pompos intitulat Australanthropus Olteniensis.[60] Cultul personalității i-a dat liderului comunist ambiții nebănuite, inclusiv aceea de a scrie un nou imn pentru RSR,[27], el modificând, se pare, o parte din bine-cunoscutul Tricolor, pentru a introduce versuri ca: „Azi partidul ne unește/Și pe plaiul românesc/Socialismul se clădește/Prin elan muncitoresc”.

Soția sa, Elena, cu o pregătire școlară elementară,[98][99][100][101] era „savant de renume mondial” și „mamă iubitoare” a poporului. Cu toate acestea, ea avea dreptul de a semna cu dr.h.c.mult. Elena Ceaușescu, deoarece primise mai multe titluri dr.h.c. de la diverse universități din lume. Deoarece acest titlu se poate acorda pentru merite politice, titlul său dr.h.c.mult. nu era o înșelătorie: prin acordarea acestui titlu se recunoșteau merite politice ale soțului ei și se urmăreau avantaje politice și comerciale reale. Astfel, acordarea acestor titluri era o monedă de schimb pentru autoritățile anumitor țări, dar titlurile erau cât se poate de reale. Dr.h.c.mult. Nicolae Ceaușescu a primit un doctorat de onoare de la Universitatea din Nisa, pe care îl deține și în prezent.[102][103]

Cultul personalității lui Ceaușescu se asemăna cu cel comunist practicat în China și Coreea de Nord de unde poate a fost copiat după vizite efectuate în respectivele țări. El este particularizat și de un complex cultural, care face din familia conducătoare nu numai depozitara înțelepciunii politice, dar și a valorilor culturale și științifice ale umanității. Președintele „scrie” cărți de filosofie, economie politică, istorie, este proclamat drept „mare gânditor al contemporaneității”. Soția sa a devenit membră a Academiei RSR și a multor altor academii, doctor în științe chimice, „savant de renume mondial”, autoare de cărți publicate în toate limbile pământului.[104] Cultul personalității nu a fost practicat de niciun domnitor, rege sau conducător român din istorie cu excepția legionarilor.[105] La o ședință de deschidere a Marii Adunări Naționale, Ceaușescu a apărut purtând sceptrul prezidențial, similar cu cele folosite de monarhi. Astfel de excese îl determină pe pictorul Salvador Dali să-i trimită dictatorului o telegramă de „felicitare”. Cotidianul central al partidului - Scînteia - nesesizând tonul ei vădit ironic, publică textul integral al telegramei[106].[nefuncțională]

Pentru a evita noi situații de „gen Pacepa”, Ceaușescu numește membri ai propriei familii, în frunte cu Elena, în funcții cheie de conducere.
Statura politică a lui Ceaușescu

Pe parcursul „Epocii Ceaușescu”, România devine al patrulea mare exportator european de armament[necesită citare]. În pofida acestui fapt, se pare că fostul șef de stat se visa laureat al Premiului Nobel pentru Pace. În acest sens, Ceaușescu face mari eforturi pentru a obține statutul de mediator în conflictul israeliano-palestinian (România fiind singura țară în contact oficial cu ambii beligeranți). Mai mult, în anul 1986, el a organizat un referendum pentru aprobarea reducerii cheltuielilor și personalului Armatei Române cu 5%. Acestea nu îl împiedică să oblige liceenii la pregătire militară, sub forma detașamentelor premilitare P.T.A.P., să oblige studentele să facă pregătire premilitară, o zi pe săptămână, în primii 3 ani de facultate și să organizeze pregătirea militară a tuturor oamenilor muncii, sub forma Gărzilor Patriotice. În aceeași perioadă, la inițiativa șefului de partid și de stat, erau convocate frecvent mari „adunări populare” pentru susținerea păcii mondiale, la care oamenii erau obligați să participe.

Principiul „neamestecului în treburile interne” este intens promovat de către Ceaușescu care dorea ca nimeni din exterior să nu-l acuze pentru dezastrul în care se afundă țara. Pe măsură ce își consolidează puterea, șeful de stat român devine megaloman, amăgit se pare de propaganda propriului partid: aparatul de propagandă partinic îl prezintă ca măreț personaj istoric, pe linia lui Burebista, a lui Decebal și a marilor domnitori medievali. Deseori, oameni de cultură, obligați de susținătorii regimului, îl proslăvesc pe „Marele Cârmaci”. Ajutat de istorici obedienți, „Mult iubitul și stimatul” își permite să modifice istoria: Mircea cel Bătrân devine „cel Mare”, iar Ioan Vodă cel Cumplit devine „cel Viteaz”. „Președintele însuși a scris în repetate rânduri despre trecut, publicând chiar și un volum intitulat «Pagini din istoria poporului român»(1983). Numeroși activiști culturali, între ei și unul din frații președintelui (generalul Ilie Ceaușescu), au devenit peste noapte istorici oficiali, preocupați în egală măsură de istoria antică, contemporană, medievală. Obsesia istorică reflectă pe de-o parte criza de legitimitate a regimului; pe de altă parte, ea are și menirea unei diversiuni, căutând să pună în interesul partidului firescul sentiment național. Modul însă foarte elementar în care se pune în practică acest naționalism istoric, caracterul său aniversativ, patriotard, fals euforic sunt de natură de a avea mai degrabă rezultate inverse”.[107]

Ceaușescu patronează un sistem politic de tip comunist, cu partid unic și alegeri de fațadă căci pe buletinele de vot nu existau mai multe partide astfel că P.C.R. câștiga cu 99,7%. Oamenii se prezintă la alegeri în procent de 99,9% de frică, pentru a nu intra în vizorul Securității. Este clamată o „democrație socialistă” pe care oamenii trebuie să o accepte și să o laude în public.
Îngrădirea libertății de exprimare

În martie 1983 Consiliul de Stat a hotărât înregistrarea mașinilor de scris și multiplicat. Posesia și folosirea lor au fost strict reglementate, pentru a preveni utilizarea lor de către persoane care „reprezintă un pericol pentru ordinea publică ori securitatea statului”, cu alte cuvinte de către cei care ar fi îndrăznit confecționarea de manifeste. O lege similară existase între 1948-1964, dar după aceea stăpânirea și folosirea mașinilor de scris de către particulari fusese liberă. Conform noului decret, aprobările de folosire a mașinilor de scris vor fi date de către Ministerul de Interne care poate „efectua și controlul asupra modului cum acestea sunt folosite”; o fișă cu literele, cifrele și semnele ortografice ale fiecărei mașini urmează a fi depusă la miliție. Astfel se putea identifica locul unde ar fi fost create manifestele. Decretul prevedea, de asemenea, că „închirierea mașinilor de scris ... precum și împrumutarea acestora în afara domiciliului deținătorului sunt interzise.”[108]

În același an, pe motiv că a criticat într-o predică faptul că ziua de Crăciun era zi obișnuită de lucru în România comunistă, preotul Géza Pálfi din Odorheiu Secuiesc a fost arestat și omorât în bătaie de organele de Securitate.

După o vizită în China și Coreea de Nord în anul 1971, la o ședință a Comitetului Executiv al C.C. al P.C.R. din 6 iulie 1971, Ceaușescu a prezentat propunerile sale pentru „îmbunătățirea activității politico-ideologice, de educare marxist-leninistă a membrilor de partid a tuturor oamenilor muncii.”[109] Cele 17 propuneri sau „teze” au fost considerate o „minirevoluție culturală” de către majoritatea observatorilor. Propunerile chemau la „creșterea continuă a rolului conducător al partidului în toate domeniile activității politico-educative”, cereau sublinierea „marilor realizări ale poporului român - constructor al socialismului”, „un control mai riguros... pentru a evita publicarea operelor literare care nu sunt la nivelul cerințelor activității politico-ideologice a partidului, a cărților care promovează idei și concepții dăunătoare intereselor construcției socialiste.” În repertoriul teatrelor, operelor și teatrelor de varietăți trebuia să se pună accentul „pe promovarea producțiilor naționale cu un caracter militant revoluționar.” După 1981 n-au mai fost permise conferințele naționale ale Uniunii Scriitorilor. Ședințele secțiilor de proză și poezie ale Uniunii Scriitorilor au fost interzise. În aceste condiții de limitare a libertății de exprimare a fost promovat protocronismul, ca ideologie culturală care se baza pe o perspectivă naționalistă asupra trecutului și pe negarea influențelor externe în cultura românească.(Mihai Bărbulescu ș.a, 2002, op. cit.)
Monitorizarea discuțiilor cu străinii

Legi și decrete speciale au fost adoptate pentru a îngrădi și controla contactele cetățenilor români cu străinii; astfel s-a decretat obligativitatea raportării oricărei convorbiri cu un cetățean străin, iar în 1982 a fost limitat numărul convorbirilor telefonice pe care abonații le puteau avea cu străinătatea. Toate aceste măsuri au îngreunat sensibil contactele cu lumea din afară, ușurând în același timp reprimarea acțiunilor de disidență.[108]
Proteste în perioada regimului Ceaușescu

În primăvara anului 1977 s-a înregistrat mișcarea inițiată de scriitorul Paul Goma. În vara anului 1977 a avut loc greva minerilor de pe Valea Jiului. În anul 1984 a eșuat o tentativă de lovitură de stat pusă la cale de trei generali, între care și Nicolae Militaru.[27] La sfârșitul anului 1987 a avut loc un nou protest, de data aceasta al muncitorilor de la uzine brașovene: 61 dintre ei vor fi condamnați la închisoare, iar 67 vor fi arestați la domiciliu.

Gabriel Andreescu, Dorin Tudoran, Dan Petrescu sau Radu Filipescu au protestat și ei în anii '80 față de abuzurile regimului totalitar.

În martie 1989, șase membri marcanți ai Partidului Comunist: Gheorghe Apostol, Alexandru Bârlădeanu, Silviu Brucan, Corneliu Mănescu, Constantin Pârvulescu și Grigore Răceanu i-au trimis lui Ceaușescu o scrisoare, cunoscută apoi ca „scrisoarea celor șase”, în care îi imputau faptul că exercita o dominație absolută asupra partidului.
Sfârșitul regimului lui Ceaușescu
Revoluția din decembrie 1989
Articole principale: Revoluția română din 1989 și Cronologia ultimelor 80 zile ale regimului Ceaușescu.

Evenimentele sângeroase de la Timișoara și București din decembrie 1989 au culminat cu căderea lui Ceaușescu și a regimului comunist.

Spre exasperarea majorității covârșitoare a românilor, Ceaușescu este confirmat în fruntea PCR pentru un nou termen de cinci ani, la Congresul al XIV-lea al PCR din noiembrie 1989. La acest congres Ceaușescu denunță Pactul Molotov-Ribbentrop și cere anularea consecințelor acestuia.

Prima tentativă de organizare a unor proteste ar fi trebuit să se materializeze la Iași, în 14 decembrie 1989, dar manifestația, ce ar fi urmat să se desfășoare în Piața Unirii, este dejucată de autoritățile comuniste.[110] O tentativă a regimului de a-l evacua pe pastorul reformat maghiar László Tőkés din locuința parohială pe care o ocupa de drept la Timișoara, pe motiv că acesta ar fi fost mutat la o altă parohie, întâmpină rezistență din partea enoriașilor, care înconjoară casa parohială într-o demonstrație de sprijin. Acestora li se alătură și români, iar demonstrația capătă în scurtă vreme un caracter mai larg, de protest împotriva regimului comunist. Trupe ale armatei, miliției și Securității apar la fața locului la 17 decembrie 1989 și deschid focul asupra manifestanților.

La 18 decembrie 1989, Ceaușescu pleacă într-o vizită oficială în Iran, lăsându-i soției sale, Elena, și altor colaboratori apropiați, misiunea de a înăbuși revolta de la Timișoara. Revolta continuă să ia amploare. După revenirea sa în țară, la 20 decembrie 1989, Ceaușescu ține o cuvântare televizată dintr-un studio de televiziune amenajat în incinta clădirii CC al PCR, în care califică evenimentele de la Timișoara drept o încercare din afară de imixtiune în afacerile interne și de subminare a suveranității României. Până la cuvântarea lui Ceaușescu, mediile oficiale de informare evită cu strictețe orice referință la evenimentele care se derulau în Timișoara, singurele surse de informare fiind posturile de radio din afara granițelor țării, precum Radio Europa Liberă și Vocea Americii. O „adunare populară” în sprijinul regimului este organizată pentru ziua următoare, 21 decembrie, în fața sediului CC al PCR, într-un loc care, în urma evenimentelor acelei zile, poartă azi numele de Piața Revoluției.[111] Demonstrația degenerează în mișcare de răsturnare a regimului. Soții Ceaușescu, surprinși de această turnură a lucrurilor, se dovedesc incapabili de a păstra controlul asupra maselor. Populația capitalei se adună în Piața Revoluției, unde se confruntă cu unități ale miliției și armatei. Din păcate, raportul de forțe înclină în favoarea forțelor de represiune, bine reprezentate numeric și bine înarmate, care până la miezul nopții reușesc să degajeze piața, omorând zeci și arestând sute de protestatari.

Cu toată întreruperea transmisiunii televizate a demonstrației din 21 decembrie, reacția ineptă și neajutorată a lui Ceaușescu nu scapă neobservată de telespectatorii din întreaga țară. Până în dimineața zilei de 22 decembrie 1989, protestele se răspândiseră deja în toate marile orașe ale României. Moartea în condiții suspecte a ministrului apărării, generalul Vasile Milea, este anunțată în 22 decembrie de către posturile naționale de radio și televiziune. Imediat după acest anunț, o ședință extraordinară a comitetului politic executiv al PCR are loc, sub conducerea lui Ceaușescu, care cu acest prilej anunță că preia comanda armatei. Ceaușescu mai face o încercare disperată de a se adresa mulțimii adunate în fața sediului CC, dar fără succes. Protestatarii forțează ușile și pătrund în sediul CC, iar soților Ceaușescu nu le rămâne decât opțiunea de a fugi cu un elicopter care îi aștepta pe acoperișul clădirii CC.
Procesul și execuția
Articol principal: Procesul și execuția soților Ceaușescu.

Soții Ceaușescu au fost condamnați printr-un proces-spectacol ținut în pur stil stalinist[112] cu verdict trasat dinainte de Victor Atanasie Stănculescu[112][113] și sacii de învelit cadavre aduși dinainte[112] la pedeapsa capitală și confiscarea totală a averii pentru săvârșirea următoarelor infracțiuni:

- Genocid, prevăzut de articolul 357, aliniat 1, literele a-c, Cod Penal;

- Subminarea puterii de stat, prevăzut de articolul 162, aliniat 1, Cod Penal;

- Acte de diversiune, prevăzut de articolul 163 Cod Penal;

- Subminarea economiei naționale, prevăzut de articolul 165, aliniat 2, Cod Penal, toate cu aplicarea articolelor 33-34 și 41, aliniat 2, Cod Penal.[114]
Deshumarea

Nicolae Ceaușescu și soția sa, Elena Ceaușescu, au fost deshumați pe 21 iulie 2010 pentru prelevarea de probe ADN, după 21 de ani, la cererea fiului lor Valentin Ceaușescu și a ginerelui Mircea Oprean (soțul Zoiei Ceaușescu), pentru a stabili dacă ei au fost sau nu înmormântați acolo.[115][116][117] Probele ADN au demonstrat că, într-adevăr, soții Ceaușescu au fost înmormântați la Cimitirul Ghencea din București.[118]
Ceaușescu în conștiința populară
Ceaușescu vânător, 1976

Potrivit unui sondaj CURS realizat în 2009, 31% dintre cei chestionați sunt de părere că în manualul de istorie Nicolae Ceaușescu ar trebui prezentat ca un om care a făcut României mai mult bine, 13% că a făcut mai mult rău, iar 52% ca un om care a făcut bine și rău în mod egal. Cei mai mulți care consideră că Ceaușescu a făcut mai mult bine sunt persoane de peste 56 de ani.[119] În emisiunea „Tănase și Dinescu”, Stelian Tănase arătă că, întrebați de ce regretă epoca Ceaușescu, nostalgicii lui Ceaușescu de vârstă înaintată invocă în primul rând faptul că erau tineri. Adrian Cioroianu a afirmat și el același lucru pe 7 august 2011 la postul Realitatea TV: oamenii care au nostalgia lui Ceaușescu au, de fapt, nostalgia propriei tinereți. Tiberiu Conțiu Șoitu, conf. dr. la catedra de Asistență Socială, sociologul constănțean Ionel Alexe din Constanța, istoricul clujean Vasile Lechințan, sociologul bucureștean Lazăr Vlăsceanu exprimă și ei aceeași părere.[120] Alte categorii care regretă epoca Ceaușescu sunt unii favorizați ai regimului de atunci (aceia al căror nivel de trai a scăzut comparativ cu cel din vremea aceea) și unii din cei care au în prezent o situație economică precară sau disperată, arată sociologul constănțean Ionel Alexe din Constanța și sociologul Marius Matichescu. Ultimul arată că nostalgia nu va fi întâlnită niciodată la „un capitalist, un patron de firmă, la cineva care nu are probleme și poate să-i ofere copilului un apartament sau chiar un loc de muncă“.[120] Printre locuitorii din mediul rural, doar 9% consideră că Ceaușescu ar fi făcut României mai mult rău decât bine.[119] Un studiu al opiniei publice executat de Marsh Copsey and Associates și Biroul de Cercetari Sociale arată că majoritatea românilor spun că regretă epoca Ceaușescu și nu sunt de acord cu faptul că soții Ceaușescu au fost executați. Totuși răsturnarea vechiului regim este considerată a fi fost în folosul țării de 40,3%, față de 35,7% care consideră că a fost în dauna țării și de 24% care au spus că nu știu. Mai mult, 60,2% nu ar prefera ca România să revină la rânduielile din vremea lui Ceaușescu față de 22,3% care ar prefera acest lucru, 17,5% spunând că nu știu sau nu răspund.[121] Sondajele s-au făcut numai pe românii aflați pe teritoriul României, deci fără cele 2,1 milioane de români care muncesc în străinătate.[122]
Neexistența de „conturi secrete” ale lui Ceaușescu

În primele zile ale revoluției din decembrie 1989 s-a vorbit mult despre conturile secrete ale lui Nicolae Ceaușescu. La procesul din 25 decembrie 1989, membrii Tribunalului Militar Excepțional au pus întrebări legate de acești bani, dar ambii soți Ceaușescu au declarat că nu au nici un dolar pe conturi în bănci străine. Deși acuzația de delapidare a banilor statului român nu a fost inclusă între capetele de acuzare (care erau 4 la număr),[123] totuși, în comunicatul care a fost difuzat de televiziune și radio, și a doua zi de presa scrisă, s-a adăugat un al cincilea punct cu următorul conținut: „Încercarea de a fugi din țară pe baza unor fonduri de peste un miliard de dolari, depuse în bănci străine”.[124]

În 1990 un grup de experți canadieni angajați de Guvernul României pentru a da de urma banilor lui Ceaușescu, a propus arestarea lui Dan Voiculescu, dar investigațiile lor au fost oprite în mod nejustificat.[125][126][127]

Parlamentul însă a adoptat, în data de 14 octombrie 2008, raportul Comisiei parlamentare de anchetă pentru investigări și clarificări referitoare la conturile lui Nicolae Ceaușescu, concluzia finală fiind că fostul șef de stat nu a avut conturi sau averi depozitate în străinătate. „În doi ani de activitate, am invitat diferite persoane care au făcut parte din sistemul de stat de atunci, oameni din BCRE, jurnaliști care s-au ocupat de acest subiect. De altfel, tot raportul cuprinde mărturiile acestor persoane. Concluziile sunt bazate pe aceste mărturii. Concluzia comună a tuturor celor audiați a fost că Nicolae Ceaușescu nu a avut conturi în afara țării”, a declarat președintele comisiei de anchetă, senatorul Sabin Cutaș.[128]

Ipoteza existenței unor conturi secrete a fost infirmată inclusiv de gen. Silvu Predoiu, fost șef al Serviciului de Informații Externe care, într-un interviu pentru Europa Liberă, a declarat: "A fost o anchetă extinsă și a fost reflectată și în presă într-o perioadă. În principiu, eu nu sunt de acord neapărat cu ideea de „conturile lui Ceaușescu”.Sunt convins că nu avea o evidență „conturile lui”. Dacă erau ale lui, ar fi avut o evidență. Nu-mi aduc aminte să fi fost găsite în cabinetul lui... Unde putea să țină o evidență a conturilor Ceaușescu? Pentru că n-a apucat să-și adune nimic de acolo. Nu cred neapărat că avea conturi. Erau niște conturi, aflate la dispoziția unor unități operative, pentru o serie de activități. Să nu uităm că era perioada când s-au plătit datoriile externe și s-au făcut o serie de contracte spectaculoase la timpul respectiv. Nu știu nimic despre soarta lor. S-au făcut niște anchete în serviciu. Una foarte profundă, cred că la nivelul anilor 2000, care s-a terminat cu niște rapoarte trimise către Parchet la momentul respectiv.” Mitul conturilor lui Ceaușescu i-a fost atribuit, fără dovezi, lui Dan Voiculescu.[129]
Altele
Familia
Nicolae Ceaușescu cu soția și părinții (1968)
Valentin Ceaușescu, fiul soților Ceaușescu
Ceaușescu jucând biliard, 1976

Ceaușescu a avut 3 copii: un fiu, Valentin Ceaușescu (n. 1947), specialist în fizică și care nu a deținut funcții politice, o fiică, Zoia Ceaușescu, matematician (n. 1 martie 1949, d. 20 noiembrie 2006) și un fiu mai tânăr, Nicu Ceaușescu (n. 1 septembrie 1951, d. 25 septembrie 1996), care s-a implicat direct în politică. Însă singurul nepot de sânge al lui Ceaușescu avea să se afle abia după aproximativ 20 de ani, acesta fiind fiul lui Valentin Ceaușescu, născut în 1981.[130]
Venituri legale

Salariul oficial al lui Ceaușescu era de 18.000 lei (aproximativ 1.200 dolari la cursul oficial de schimb din 1989, având o medie de 14,92 lei, echivalent al salariului mediu din SUA în acea perioadă).[131] Au existat zvonuri că deținea conturi secrete în străinătate, dar urma acestora nu a putut fi descoperită.[132] Există în schimb dovezi că luxul în care trăia Ceaușescu era finanțat din bani publici.[133]
Garda personală

Garda personală a lui Ceaușescu consta din 40 de membri, responsabili pentru protecția întregii sale familii, precum și a locuințelor acestora[necesită citare]. Șeful gărzii, colonelul Dumitru Burlan, afirmă că întreaga gardă era dotată cu numai două arme automate (dotare insuficientă pentru o apărare serioasă). Colonelul Burlan susține că Ceaușescu se credea iubit de popor și nu simțea nevoia protecției. De fapt pe Ceaușescu îl apăra tot regimul său și întreaga Securitate și nu avea nevoie de o gardă de corp prea puternică. Departamentul Securității Statului a avut 8.474 de oameni, iar Trupele de Securitate, comandate de generalul Ghiță, erau de aproximativ 15.000.[134]
Preferințe

Într-un articol recent, se afirmă că Ceaușescu ar fi fost implicat în închisoare într-un caz de homosexualitate, care s-ar fi consumat între el și un alt deținut numit Marcovici. Cazul a fost prelucrat de Chivu Stoica, care a acționat la indicațiile lui Gheorghe Gheorghiu-Dej în sensul prevenirii unor întâmplări similare.[135]

Suzana Andreias, șefa personalului la reședința de la Snagov a familiei Ceaușescu timp de aproape trei decenii, a declarat: „Erau foarte apropiați, se țineau de mână. Ceaușescu nu ieșea din cuvântul ei, dar și tovarășa se interesa mult de el, dacă a mâncat, dacă are tot ce-i trebuie, dacă e mulțumit. Luau masa în curte și se simțeau bine împreună. Lui îi plăcea mult muzica Ioanei Radu și a Miei Braia și, după ce mâncau, el cânta, jucau table și ea îl mai fura. Zicea tovarășul: «Iar m-ai furat, nu mai joc.» «Hai, Nicule, că nu te mai fur...» Și uite-așa se distrau ei în familie” . Lui Ceaușescu îi plăceau șahul, biliardul și voleiul. După versurile pe care le recita pe la congrese, se pare că citea literatura română, și în primul rând poezia lui Eminescu. Nu era pretențios la mâncare și avea gusturi rustice. Filmele le-a descoperit pe la 35 de ani. Era mare fan Kojak și se uita cu plăcere la filme polițiste americane. Toate reședințele lui erau dotate cu o sală specială de proiecție. După 1955, s-a apucat de vânătoare, mai întâi invitat de șefii locali de partid, pe care îi controla la vremea aceea în calitatea lui de membru al Biroului Politic al CC. Din 1968, cuvântările sale au început să fie tipărite. S-a ajuns la Ceaușescu în 33 de volume. În ultimii 10 ani din viață, a suferit de diabet. Odată cu înaintarea în vârstă, a devenit tot mai fricos. Din 1972, nu mai purta niciun articol de îmbrăcăminte mai mult de o zi. Direcția a V-a a Securității a înființat ateliere de croitorie care produceau numai pentru el: îmbrăcăminte de birou, șepci Lenin, jachete Mao, paltoane de stofă englezească, hanorace vătuite, în stil sovietic, costume de vânătoare în stil german. Era pedant și obsedat de punctualitate. În fiecare dimineață, la 8 fix, coloana de mașini îl ducea la birou. Lua masa de prânz la ora 13 fix. Folosea gel de duș Badedas și se rădea cu Gillette. Îi plăceau Galbena de Odobești și șampania roze.[16]

    „„A fost vorba de dereglare psihică în cazul lui Nicolae Ceaușescu. Mulți întreabă dacă răposatul a fost paranoic și eu, de regulă, le răspund - și aceasta este opinia mea personală - că n-a fost paranoic, ci psihopat paranoic. Diferența este de grad, ambii au un sistem ideativ rigid, cred foarte tare că ceea ce este în capul lor este și adevărat, diferența între un paranoic și un psihopat paranoic este gradul de desprindere de realitate. De pildă, paranoicul o să îți spună că el comunică cu extratereștrii și că dușmanii pun otravă în lampa din plafon și îți dai seama repede că este prea de tot, în timp ce un psihopat paranoic te va convinge până la un anumit punct, pentru că el pare coerent. La o primă analiză, parcă nu este chiar nebun de tot. Paranoizii sunt printre noi și sunt în funcții foarte înalte, peste tot în lume. Paranoid au fost și Hitler, și Stalin”, a fost descrierea făcută de psihologul Holdevici Irina fostului dictator la emisiunea „Profesioniștii” de pe TVR.”
    —Cristian Andrei, Holdevici: „Am fost un amărât de agent. N-am fost niciodată împotriva unui regim”. Lista celor turnați: Ion Vulcănescu, Gregorian Bivolaru, Vladimir Gheorghiu, puterea.ro, 22 februarie 2011

'''
pairGenerator = PairGenerator(text, vocabulary=voc, window_size=5)

net = Word2Vec(len(voc))

net.train(pairGenerator, 10)

embeddings = net.reprs.weight.T

word1 = run_stemmer(['matematician'])[0]
word1 = voc.index(word1)

word2 = run_stemmer(['bani'])[0]
word2 = voc.index(word2)

word3 = run_stemmer(['politica'])[0]
word3 = voc.index(word3)

word4 = run_stemmer(['familiei'])[0]
word4 = voc.index(word4)

print( f'POLITICA - BANI: {(embeddings[word3] - embeddings[word2]).abs().sum()}' )
print( f'POLITICA - MATEMATICIAN: {(embeddings[word3] - embeddings[word1]).abs().sum()}' )
print(f'BANI - FAMILIE: {(embeddings[word2] - embeddings[word4]).abs().sum()}')
print(f'POLITICA - FAMILIE: {(embeddings[word3] - embeddings[word4]).abs().sum()}')
