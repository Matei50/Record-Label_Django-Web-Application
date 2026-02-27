from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArtistForm, ArtistFilterForm, ContactForm, AlbumForm, CustomUserCreationForm, CustomAuthenticationForm
import re
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import json
from .models import Artist, Album, Piesa, GenMuzical, CustomUser
import time
from django.conf import settings
import os
from .utils import calculeaza_varsta_luni, formateaza_mesaj
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.shortcuts import render, get_object_or_404
try:
    from .forms import ArtistFilterForm
except Exception:
    from django import forms
    class ArtistFilterForm(forms.Form):
        nume = forms.CharField(required=False)
        gen_muzical = forms.IntegerField(required=False)
        an_formare_min = forms.IntegerField(required=False)
        an_formare_max = forms.IntegerField(required=False)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


ACC = []
def index(request):
    acces = Accesare(
        ip_client=request.META.get("REMOTE_ADDR"),
        url=request.build_absolute_uri(),
        data=datetime.now(),
    )
    ACC.append(acces)

    numar_artisti = Artist.objects.count()
    numar_albume = Album.objects.count()
    numar_piese = Piesa.objects.count()
    
    toate_genurile = GenMuzical.objects.all()

    context = {
        "titlu_pagina": "Bun venit pe platforma casei noastre de discuri",
        "descriere_proiect": "Acest proiect este o aplicație web pentru managementul unei case de discuri. "
                             "Platforma va permite vizitatorilor să exploreze artiștii noștri, să vadă discografia completă, "
                             "să răsfoiască albume și piese.",

        "numar_artisti": numar_artisti,
        "numar_albume": numar_albume,
        "numar_piese": numar_piese,
        "genuri": toate_genurile,
    }
    
    return render(request, 'pgLang/index.html', context)


zile = ['luni', 'marți', 'miercuri', 'joi', 'vineri', 'sâmbătă', 'duminică']
luni = ['ianuarie', 'februarie', 'martie', 'aprilie', 'mai', 'iunie',
        'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie']

def afis_data(format):
    acum = datetime.now()
    ziua_sapt = zile[acum.weekday()]
    luna = luni[acum.month - 1]

    if format == 'data':
        sir = f"{ziua_sapt}, {acum.day} {luna} {acum.year}"
    elif format == 'zi':
        sir = ziua_sapt
    elif format == 'timp':
        sir = f"{acum.hour}:{acum.minute}:{acum.second}"
    else:
        sir = "Format necunoscut"
    return sir


class Accesare:
    _id = 0
    def __init__(self, ip_client, url, data):
        Accesare._id += 1
        self.id = Accesare._id
        self.ip_client = ip_client
        self.url = url
        self.data = data
        
    def lista_parametrii(self):
        p = urlparse(self.url)
        parametri = parse_qs(p.query)
        lista = []
        for cheie in parametri:
            if parametri[cheie]:
                lista.append((cheie, parametri[cheie]))
            else:
                lista.append((cheie, None))
        
        return [("id", self.id), ("ip client", self.ip_client if self.ip_client else None), ("url", self.url if self.url else None), ("data", self.data.strftime("%A %d %B %Y") if self.data else None)]
    
    def dict(self):
        p = urlparse(self.url)
        parametri = parse_qs(p.query)
        lista = []
        for cheie in parametri:
            if parametri[cheie]:
                lista.append((cheie, parametri[cheie]))
            else:
                lista.append((cheie, None))
                
        return {"id": self.id, "ip client": self.ip_client if self.ip_client else None, "url": self.url if self.url else None, "data": self.data.strftime("%A %d %B %Y") if self.data else None, "parametri": lista}
        

    def url(self):
        return self.url
    def data(self, str="%A %d %B %Y"):
        return self.data.strftime("")
    def ora(self):
        return f"{self.data.hour}:{self.data.minute}:{self.data.second}"
    def pagina(self):
        nume = urlparse(self.url).path
        return nume

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

def info(request):
    parametrii = request.GET
    nr_parametrii = len(parametrii)
    nume_parametrii = list(parametrii.keys())
    acces = Accesare(
        ip_client=request.META.get("REMOTE_ADDR"),
        url=request.build_absolute_uri(),
        data=datetime.now(),
    )
    ACC.append(acces)
    
    path = request.path
    print(path)
        
    print(f"Accesarea salvata: {acces}")
    print(ACC[-len(ACC)])

    print("Parametri accesare:", acces.lista_parametrii())
    print("Pagina accesata:", acces.pagina())
    
    client_ip = request.META.get('REMOTE_ADDR')

    format = request.GET.get("format")
    rezultat = afis_data(format)

    d = {
        "rezultat": rezultat,
        "nume_parametrii": nume_parametrii,
        "numar_parametrii": nr_parametrii,
        
    }
    return render(request, 'pgLang/info.html', d)

    
def afis_template(request):
    return render(request,"pgLang/exemplu.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )

def lista_artisti(request):
    
    lista_de_baza = Artist.objects.select_related('gen_muzical') 
    form = ArtistFilterForm(request.GET or None)
    
    per_page = 5 
    warning_message = None
    
    if form.is_valid():
        nume = form.cleaned_data.get('nume')
        gen = form.cleaned_data.get('gen_muzical')
        an_min = form.cleaned_data.get('an_formare_min')
        an_max = form.cleaned_data.get('an_formare_max')
        
        per_page = form.cleaned_data.get('per_page') or 5

        if nume:
            lista_de_baza = lista_de_baza.filter(nume__icontains=nume)
        if gen:
            lista_de_baza = lista_de_baza.filter(gen_muzical=gen)
        if an_min:
            lista_de_baza = lista_de_baza.filter(an_formare__gte=an_min)
        if an_max:
            lista_de_baza = lista_de_baza.filter(an_formare__lte=an_max)
    
    else:
        try:
            per_page = int(request.GET.get('per_page', 5))
        except ValueError:
            per_page = 5

    if 'per_page' in request.GET:
        warning_message = "Atentie: Numarul de itemi pe pagina a fost schimbat."

    sort_param = request.GET.get('sort')
    if sort_param == 'd':
        lista_de_baza = lista_de_baza.order_by('-nume')
        sort_display = 'Z-A'
    else:
        lista_de_baza = lista_de_baza.order_by('nume')
        sort_display = 'A-Z'

    paginator = Paginator(lista_de_baza, per_page) 
    numar_pagina = request.GET.get('page')
    try:
        artistii_de_pe_pagina = paginator.page(numar_pagina)
    except PageNotAnInteger:
        artistii_de_pe_pagina = paginator.page(1)
    except EmptyPage:
        artistii_de_pe_pagina = paginator.page(paginator.num_pages)

    context = {
        'lista_artisti' : artistii_de_pe_pagina, 
        'form': form,
        'sort_display': sort_display,
        'sort_param': sort_param,
        'warning_message': warning_message, 
    }
    
    return render(request, 'pgLang/lista_artisti.html', context)

def detaliu_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    
    albumele_artistului = artist.albume.all()
    
    context = {
        'artist': artist,
        'albume': albumele_artistului
    }
    return render(request, 'pgLang/detaliu_artist.html', context)

@login_required
def adauga_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            form.save() 
            return redirect('lista-artisti') 
    else:
        form = ArtistForm()
        
    return render(request, 'pgLang/adauga_artist.html', {'form': form})

def detaliu_gen(request, gen_slug):
    gen = get_object_or_404(GenMuzical, slug=gen_slug)
    
    lista_de_baza = Artist.objects.filter(gen_muzical=gen).select_related('gen_muzical')
    
    form = ArtistFilterForm(request.GET or None, initial={'gen_muzical': gen.id})
    
    per_page = 5 
    warning_message = None 
    
    if form.is_valid():
        nume = form.cleaned_data.get('nume')
        an_min = form.cleaned_data.get('an_formare_min')
        an_max = form.cleaned_data.get('an_formare_max')
        per_page = form.cleaned_data.get('per_page') or 5
        gen_from_form = form.cleaned_data.get('gen_muzical')

        if gen_from_form != gen:
            form.add_error('gen_muzical', 'Eroare: Modificarea categoriei nu este permisa pe aceasta pagina.')
        else:
            if nume:
                lista_de_baza = lista_de_baza.filter(nume__icontains=nume)
            if an_min:
                lista_de_baza = lista_de_baza.filter(an_formare__gte=an_min)
            if an_max:
                lista_de_baza = lista_de_baza.filter(an_formare__lte=an_max)
    else:
        try:
            per_page = int(request.GET.get('per_page', 5))
        except ValueError:
            per_page = 5

    if 'per_page' in request.GET:
        warning_message = "Atentie: Numarul de itemi pe pagina a fost schimbat."

    sort_param = request.GET.get('sort')
    if sort_param == 'd':
        lista_de_baza = lista_de_baza.order_by('-nume')
        sort_display = 'Z-A'
    else:
        lista_de_baza = lista_de_baza.order_by('nume')
        sort_display = 'A-Z'

    paginator = Paginator(lista_de_baza, per_page)
    numar_pagina = request.GET.get('page')
    try:
        artisti_pe_pagina = paginator.page(numar_pagina)
    except PageNotAnInteger:
        artisti_pe_pagina = paginator.page(1)
    except EmptyPage:
        artisti_pe_pagina = paginator.page(paginator.num_pages)

    context = {
        'gen': gen,
        'artisti': artisti_pe_pagina, 
        'form': form,
        'sort_display': sort_display,
        'sort_param': sort_param,
        'warning_message': warning_message,
        'is_gen_page': True
    }
    return render(request, 'pgLang/detaliu_gen.html', context)

def register_view(request): # l7 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #l7 c2
            user.cod = uuid.uuid4().hex
            user.email_confirmat = False
            user.save()

            link = request.build_absolute_uri(
                f"/aplicatie/confirma_mail/{user.cod}/"
            )

            html_content = render_to_string(
                "pgLang/email_confirmare.html",
                {
                    "user": user,
                    "link_confirmare": link
                }
            )

            email = EmailMessage(
                subject="Confirmare cont",
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            email.send()

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'pgLang/register.html', {'form': form})

def pagina_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            varsta_str = calculeaza_varsta_luni(data['data_nasterii'])
            mesaj_formatat = formateaza_mesaj(data['mesaj'])
            
            tip = data['tip_mesaj']
            zile = data['minim_zile_asteptare']
            urgent = False #l6 t4
            if (tip in ['review', 'cerere'] and zile == 4) or \
               (tip in ['programare', 'intrebare'] and zile == 2):
                urgent = True

            date_de_salvat = {
                'nume': data['nume'],
                'prenume': data['prenume'],
                'cnp': data['cnp'],
                'varsta': varsta_str,   
                'email': data['email'],
        
                'tip_mesaj': data['tip_mesaj'],
                'subiect': data['subiect'],
                'minim_zile_asteptare': zile,
                'mesaj': mesaj_formatat,
                'urgent': urgent,       
                
                'meta_info': {
                    'ip_utilizator': request.META.get('REMOTE_ADDR'),
                    'data_ora_primire': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }

            folder_mesaje = os.path.join(settings.BASE_DIR, 'Mesaje') 
            if not os.path.exists(folder_mesaje):
                os.makedirs(folder_mesaje)

            timestamp = int(time.time())
            nume_fisier = f"mesaj_{timestamp}"
            if urgent:
                nume_fisier += "_urgent"
            nume_fisier += ".json"
            
            cale_completa = os.path.join(folder_mesaje, nume_fisier)

            with open(cale_completa, 'w', encoding='utf-8') as f:
                json.dump(date_de_salvat, f, indent=4, ensure_ascii=False)

            return redirect('index')
    else:
        form = ContactForm()
        
    return render(request, 'pgLang/contact.html', {'form': form})

def adauga_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album_nou = form.save(commit=False)
            
            cost = form.cleaned_data.get('cost_productie')
            marja = form.cleaned_data.get('marja_profit')

            album_nou.pret = cost + (cost * marja / 100)
            
            album_nou.save()
            
            return redirect('index') 
    else:
        form = AlbumForm()
        
    return render(request, 'pgLang/adauga_album.html', {'form': form})

def detaliu_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    context = {
        'album': album,
    }
    return render(request, 'pgLang/detaliu_album.html', context)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST) 
        
        if form.is_valid():
            user = form.get_user()
            
            login(request, user) 
            
            request.session['profil'] = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'data_nasterii': user.data_nasterii.strftime('%Y-%m-%d') if user.data_nasterii else '',
                'telefon': user.telefon,
                'adresa': user.adresa,
                'oras': user.oras,
                'judet': user.judet,
                'cod_postal': user.cod_postal,
            }

            if form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(24 * 60 * 60) 
            else:
                request.session.set_expiry(0) 
            
            return redirect('profil') 
    else:
        form = CustomAuthenticationForm() 
        
    return render(request, 'pgLang/login.html', {'form': form})

def logout_view(request):
    logout(request) 
    return redirect('index') 

from django.contrib.auth.decorators import login_required

@login_required #l6 c5
def profil(request):
    profil_data = request.session.get('profil')

    if not profil_data:
        u = request.user
        profil_data = {
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'data_nasterii': u.data_nasterii.strftime('%Y-%m-%d') if u.data_nasterii else '',
            'telefon': u.telefon,
            'adresa': u.adresa,
            'oras': u.oras,
            'judet': u.judet,
            'cod_postal': u.cod_postal,
        }
        request.session['profil'] = profil_data

    return render(request, 'pgLang/profil.html', {'profil': profil_data})

@login_required
def schimbare_parola(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profil')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'pgLang/schimbare_parola.html', {'form': form})


def confirma_mail(request, cod):
    user = get_object_or_404(CustomUser, cod=cod)

    user.email_confirmat = True
    user.cod = None
    user.save()

    return render(request, "pgLang/email_confirmat.html")