import re
from datetime import date
from django.core.exceptions import ValidationError

def validate_varsta_majora(data_nasterii):#l5 2
    today = date.today()
    varsta = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
    if varsta < 18:
        raise ValidationError("Trebuie să aveți peste 18 ani pentru a trimite un mesaj.")

def validate_mesaj_complex(valoare):
    cuvinte = [c for c in re.split(r'\W+', valoare) if c]
    
    if not (5 <= len(cuvinte) <= 100):
        raise ValidationError(f"Mesajul trebuie să conțină între 5 și 100 de cuvinte. (Curent: {len(cuvinte)})")
    
    for cuvant in cuvinte:
        if len(cuvant) > 15:
            raise ValidationError(f"Cuvântul '{cuvant}' este prea lung (maxim 15 caractere).")

def validate_fara_link(valoare):
    if 'http://' in valoare.lower() or 'https://' in valoare.lower():
        raise ValidationError("Nu sunt permise link-uri (http:// sau https://) in acest camp.")

def validate_tip_mesaj_selectat(valoare):
    if valoare == 'neselectat':
        raise ValidationError("Vă rugăm să selectați un tip de mesaj valid.")

def validate_cnp(valoare):
    if not valoare.isdigit():
        raise ValidationError("CNP-ul trebuie să conțină doar cifre.")
    
    if len(valoare) != 13:
        raise ValidationError("CNP-ul trebuie să aibă exact 13 cifre.")

    if valoare[0] not in ['1', '2', '5', '6']:
        raise ValidationError("Conform cerințelor, CNP-ul trebuie să înceapă cu 1 sau 2, respectiv 5 sau 6.")
    
    if valoare[0] == 1 or valoare[0] == 2:
        an = int("19" + valoare[1:3])
        luna = int(valoare[3:5])
        zi = int(valoare[5:7])
    else:
        an = int("20" + valoare[1:3])
        luna = int(valoare[3:5])
        zi = int(valoare[5:7])
    
    try:
        date(an, luna, zi)
    except ValueError:
        raise ValidationError("Cifrele din CNP nu formează o dată validă.")

def validate_email_temporar(valoare):
    domenii_interzise = ['guerillamail.com', 'yopmail.com']
    parti_email = valoare.split('@')
    if len(parti_email) > 1:
        domeniu = parti_email[-1].lower()
        if domeniu in domenii_interzise:    
            raise ValidationError(f"Domeniul '{domeniu}' nu este permis (email temporar).")

def validate_format_text(valoare):
    if not re.match(r'^[A-Z][a-zA-Z\s-]*$', valoare):
        raise ValidationError("Textul trebuie să înceapă cu literă mare și să conțină doar litere, spații sau cratimă.")

def validate_majuscula_dupa_separator(valoare):
    if re.search(r'(?<=[\s-])[a-z]', valoare):
        raise ValidationError("Fiecare nume trebuie să înceapă cu literă mare (chiar și după cratimă sau spațiu).")
    
def validate_fara_simboluri(valoare):
    if re.search(r'[!@#$%^&*(){}\[\]]', valoare):
        raise ValidationError("Titlul nu poate conține caractere speciale (!@#$%...).")