import re
from datetime import date

def calculeaza_varsta_luni(data_nasterii): 
    today = date.today()
    ani = today.year - data_nasterii.year
    luni = today.month - data_nasterii.month
    if today.day < data_nasterii.day:
        luni -= 1
    if luni < 0:
        ani -= 1
        luni += 12
    if ani == 0:
        return f"{luni} luni"
    return f"{ani} ani și {luni} luni"

def formateaza_mesaj(mesaj):
    mesaj = mesaj.replace('\n', ' ').replace('\r', '')
    mesaj = re.sub(' +', ' ', mesaj)
    def upper_repl(match):
        return match.group(1) + match.group(2).upper()
    
    mesaj = re.sub(r'([.?!…]+)(\s+[a-z])', upper_repl, mesaj)
    return mesaj.strip()