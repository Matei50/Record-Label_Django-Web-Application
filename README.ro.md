English version: [link](README.md)

---

# Sistem de Management pentru Casa de Discuri

Acest proiect implementează o aplicație web dezvoltată în Django, care simulează și gestionează activitățile unei case de discuri, incluzând administrarea artiștilor, gestionarea albumelor, organizarea pieselor, autentificarea utilizatorilor și procesarea structurată a mesajelor.

Aplicația este dezvoltată în Python folosind framework-ul Django și urmărește demonstrarea unei arhitecturi clare, a validărilor complexe de formular, a relațiilor între modele și a procesării datelor la nivel de server.

---

## Funcționalități principale

Platforma permite utilizatorilor să:

- Vizualizeze și filtreze artiști
- Acceseze detalii despre albume și piese
- Sorteze și pagineze rezultatele
- Se înregistreze și autentifice
- Trimită mesaje validate prin formular
- Salveze mesaje structurate în format JSON
- Administreze conținutul prin panoul Django Admin

---

## Elemente tehnice importante

### Model utilizator personalizat
Extinde `AbstractUser` cu câmpuri suplimentare:
- Data nașterii
- Telefon
- Adresă
- Oraș
- Județ
- Cod poștal

### Validări complexe
Sunt implementate validări pentru:
- Vârstă minimă (18+)
- CNP
- Număr și lungime cuvinte
- Domenii de email interzise
- Format text
- Semnătura obligatorie în mesaj

### Relații între modele
Structura bazei de date include:
- Gen muzical
- Artist
- Album
- Piesă

Implementate folosind Django ORM și relații ForeignKey.

### Paginare și filtrare
Lista artiștilor permite:
- Filtrare după nume
- Filtrare după gen
- Filtrare după an formare
- Modificarea numărului de rezultate pe pagină
- Sortare alfabetică

### Middleware personalizat
Aplicația include middleware pentru procesarea cererilor și modificarea răspunsurilor.

### Procesare JSON
Mesajele de contact sunt:
- Preprocesate
- Validate
- Salvate în fișiere JSON
- Marcate ca urgente pe baza unor reguli
- Însoțite de metadate (IP, dată, oră)

---

## Tehnologii utilizate

- Python
- Django
- SQLite
- Django ORM
- Template-uri HTML
- Validatori personalizați
- Middleware personalizat

---

## Context academic

Proiect realizat în cadrul cursurilor din anul II – Informatică, Universitatea din București.

Demonstrează aplicarea practică a:
- Programării orientate pe obiect
- Dezvoltării aplicațiilor web
- Validării datelor
- Baze de date relaționale
- Sistemelor de autentificare
