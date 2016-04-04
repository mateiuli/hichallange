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
- webserver -> folosind flask se creaza un server web ce asculta pe portul 5000
si asteapta cereri care contin un query string de forma:
<i>http://localhost:5000/?day=april%204&year=1964&category=events</i>

Poate sa lipseasca oricare dintre variabilele: day, year, category, cautarea
facandu-se astfel doar dupa valorile specificate.

Am avut in vedere si cautarea dupa un keyword din cadrul titlului, astfel cautarea
se poate face astfel:
<i>http://localhost:5000/?category=events&keyword=germany&year=1945</i>

Cele patru variabile: day, category, year si keyword pot fi combinate in orice mod.