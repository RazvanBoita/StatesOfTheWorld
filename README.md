Se va crea un crawler ce va intra pe pagina de Wikipedia cu țările lumii și va reține într-o
bază de date informații precum: nume, nume capitala, populatie, densitate, suprafață,
vecini, limba vorbită, fusul orar, tip de regim politic (democratic, monarhie, etc)


De asemenea, se va construi un API peste baza de date, care va avea multiple rute,
apelate cu metoda GET. Aceste apeluri vor returna topul primelor 10 țări cu : cea mai
mare populație, cea mai mare densitate.
Ex. Vreau topul primelor 10 țări după populație - apelez GET pe ruta
/top-10-tari-populație și voi primi un răspuns, pe care îl voi afișa pe ecran, lista aferentă
Deasemenea, ar trebui sa se poată cere și alte informații (de genu - toate țările de pe
GMT+2, sau toate țările în care se vorbește ENGLEZA, sau toate țările care se bazează
pe un anumit tip de regim politic), la fel sub forma de rute.
INPUT: wikipedia_api.py
Client.py (care sa apeleze API-ul)
OUTPUT: r = requests.get(api_url + route)

print(r.text)
``` topul țărilor cu cea mai mare densitate```