from ml.misc_utils import preprocess
from ml.bayes import BayesClassifier


text = '''Arjen Robben (Pronunție în olandeză: /ˈɑrjən ˈrɔbə(n)/; n. 23 ianuarie 1984) este un fost jucător de fotbal olandez care a evoluat ultima dată la clubul german Bayern München, fiind în același timp și component al echipei naționale de fotbal a Olandei, fiind și căpitanul acesteia. A participat la Campionatele Europene din 2004, 2008 și 2012 și la Campionatele Mondiale din 2006, 2010 și 2014. Joacă de regulă ca extremă, fiind rar folosit și ca atacant. Este cunoscut pentru driblinguri, viteză, forță de pătrundere și un bun stângaci, mai ales pentru șuturile precise de la distanță.

Robben a devenit cunoscut în lumea fotbalului la Groningen, fiind jucătorul anului al echipei în sezonul de Eredivisie 2000-2001. Peste doi ani a semnat cu PSV, unde a devenit Cel mai bun tânăr fotbalist olandez și cu care a câștigat primul titlu. Din acest motiv cluburile engleze au încercat să-l aducă, cu Chelsea având câștig de cauză în 2004.

Debutul lui Robben la Chelsea a fost întârziat de accidentări, dar după revenire a reușit să câștige cu Chelsea Premier League de două ori consecutiv, fiind și Jucătorul Lunii în Premier League în noiembrie 2005. În cel de-al treilea sezon jucat în Anglia Robben a fost măcinat de accidentări, astfel că Chelsea l-a vândut la clubul spaniol Real Madrid pentru 35 de milioane de euro.

În august 2009, Robben a fost cumpărat de Bayern München pentru 25 de milioane de euro, marcând două goluri la debut. În primul sezon jucat pentru echipa bavareză a reușit să câștige primul titlu în Germania, fiind al cincilea campionat câștigat de Robben în opt ani, el marcând în același sezon și golul câștigător al Finalei Ligii Campionilor 2013. Pentru performanțele reușite la Bayern în primul sezon, Robben a fost numit Fotbalistul Anului în Germania. În 2014, Robben a fost numit al patrulea cel mai bun fotbalist din lume de ziarul The Guardian.

La 4 iulie 2019, Arjen Robben a ales să se retragă din fotbalul profesionist la doar 35 de ani, el spunând că aceasta a fost o decizie dificilă. Ultimul său meci a fost în luna mai a anului 2019 după câteva luni în care a stat pe bancă din cauza unei accidentări. Meciul a fost câștigat cu 5-1 de Bayern împotriva echipei Eintracht Frankfurt.'))'''

text = preprocess(text)
bc = BayesClassifier()
result = bc.run(text)
print(result)