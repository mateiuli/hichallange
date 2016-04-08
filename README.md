# Hichallange

Pentru rezolvarea problemei am folosit Python 2.7.10. Pachetele aditionale
folosite sunt disponibile in fisierul requirements.txt. 

Ca baza de date am folosit MongoDB, dupa cum se cerea si in enunt.

Exista doua scripturi, unul care parcurge toate zilele unui an, parseaza
continutul paginilor preluat cu ajutorul pachetului 'wikipedia' si le salveaza
in baza de date.

Am avut in vedere si posibilitatea cautarii dupa un keyword din 'title', din 
acest motiv se creaza si un index de tip text peste acest camp.
Din cauza faptului ca anumiti ani sunt sub forma 'year BC', am retinut data
sub forma unui string nu sub forma unui obiect corespunzator. Un alt motiv
pentru care am ales aceasta solutie este faptul ca nu se fac interogari de
selectie a unui interval dat de doua date.

Deoarece nu se fac inserari/modificari in continuu asupra bazei de date, ci
doar cautari, am ales sa creez un index pentru campurile: category, day, year.

Cele doua scripturi sunt: 
- WebServer.py
- FetchWiki.py

<h2>WebServer.py</h2>
Folosind flask se creaza un server web ce asculta pe portul 5000 si asteapta cereri care contin un query string de forma: <br />
<i>http://localhost:5000/?day=april 4&year=1964&category=events</i>

Poate sa lipseasca oricare dintre variabilele: day, year, category, cautarea
facandu-se astfel doar dupa valorile specificate.

Am avut in vedere si cautarea dupa un keyword din cadrul titlului, astfel cautarea
se poate face astfel: <br />
<i>http://localhost:5000/?category=events&keyword=germany&year=1945</i>

Cele patru variabile: day, category, year si keyword pot fi combinate in orice mod.

<h2>FetchWiki.py</h2>
Folosind pachetul 'wikipedia' extrag din fiecare pagina cu titlu de forma 'month_day' continutul acesteia sub forma plain text si cu ajutorul expresiilor regulate, extrag linie cu linie informatiile si le salvez in baza de date.

Parser-ul efectiv l-am implementat separat: PageParser.py.

<h1>Cum se ruleaza</h1>
Scripturile pot fi rulate atat pe localhost cat si in containere docker diferite,
serverul cu baza de date intr-un container, iar celelalte doua scripturi in alt
container.

Legatura dintre cele doua containere (adresa serverului cu baza de date) se face automat prin variabila de mediu: DB_PORT_27017_TCP_ADDR. By default, adresa
serverului DB este luata din aceasta variabila de mediu. Ea poate fi suprascrisa in cazul in care se doreste rularea pe localhost.

<h2>Rulare local (fara docker)</h2>
Mai intai trebuie parsate paginile de pe wikipedia pentru popularea bazei de date. Acest lucru se poate face astfel: <br />
<b>python -u FetchWiki.py --dbserver &lt;mongo_db_server_address&gt;</b>
<i> exemplu: python -u FetchWiki.py --dbserver localhost</i>

Apoi se poate porni serverul web astfel: <br />
<b>python -u WebServer.py --dbserver &lt;mongo_db_server_address&gt;</b>
<i>exemplu: python -u WebServer.py --dbserver localhost</i>

<h2>Rulare in containere docker (docker-compose)</h2>

<b>docker-compose build</b>

<b>docker-compose up</b>

Intr-un container ruleaza serverul cu baza de date, iar in celalalt este rulat scriptul 'run_all.sh' care mai intai executa 'FetchWiki.py' iar apoi porneste serverul web 'WebServer.py'.

Nu exista posibilitatea de a se face refresh la date intr-un interval de doua ore. De fiecare data se parseaza si se salveaza informatiile in db. 