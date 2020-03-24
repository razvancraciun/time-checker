from nltk import word_tokenize
from ml.bayes import BayesClassifier


text = '''Mihail Kogălniceanu (n. 6 septembrie 1817, Iași, Moldova – d. 1 iulie 1891, Paris, Republica Franceză) a fost un om politic de orientare liberală, avocat, istoric și publicist român originar din Moldova, care a devenit prim-ministru al României la 11 octombrie 1863, după Unirea din 1859 a Principatelor Dunărene în timpul domniei lui Alexandru Ioan Cuza, și mai târziu a servit ca ministru al Afacerilor Externe sub domnia lui Carol I. A fost de mai multe ori ministru de interne în timpul domniilor lui Cuza și Carol. A fost unul dintre cei mai influenți intelectuali români ai generației sale (situându-se pe curentul moderat al liberalismului). Fiind un liberal moderat, și-a început cariera politică în calitate de colaborator al prințului Mihail Sturdza, în același timp ocupând funcția de director al Teatrului Național din Iași și a publicat multe opere împreună cu poetul Vasile Alecsandri și activistul Ion Ghica.

A fost redactor șef al revistei Dacia Literară și profesor al Academiei Mihăileane. Kogălniceanu a intrat în conflict cu autoritățile din cauza discursului inaugural cu tentă romantic-naționalistă susținut în anul 1843. A fost unul dintre ideologii Revoluției de la 1848 în Moldova, fiind autorul petiției Dorințele partidei naționale din Moldova.

După Războiul Crimeii, prințul Grigore Alexandru Ghica l-a însărcinat cu elaborarea unui pachet de legi pentru abolirea robiei romilor. Împreună cu Alecsandri, a editat revista unionistă Steaua Dunării, a jucat un rol important în timpul alegerilor pentru Divanurile ad-hoc, și l-a promovat cu succes pe Cuza, prietenul său pe tot parcursul vieții, la tron.

Kogălniceanu a susținut prin propuneri legislative eliminarea rangurilor boierești și secularizarea averilor mănăstirești. Eforturile sale pentru reforma agrară au dus la o moțiune de cenzură, care a declanșat o criză politică care a culminat cu lovitura de stat din mai 1864, provocată de Alexandru Ioan Cuza pentru implementarea reformei. Cu toate acestea, Kogălniceanu a demisionat în 1865, în urma conflictelor cu domnitorul. După un deceniu, a pus bazele Partidului Național Liberal, dar mai înainte de asta, a jucat un rol important în decizia României de a participa la Războiul Ruso-Turc din 1877-1878, război care a dus la recunoașterea independenței țării. În ultimii ani de viață a fost o figură politică proeminentă, președinte al Academiei Române și reprezentant al României în relațiile cu Franța. '''

text = word_tokenize(text)
bc = BayesClassifier()

print('Unbiased run...')
result = bc.run(text)
print(result)

print('---------------------------')

print('Biased run...')
result_biased = bc.run_biased(text)
print(result_biased)