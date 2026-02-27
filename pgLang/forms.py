# pgLang/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import GenMuzical, Artist, Album, CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from .validators import (
    validate_varsta_majora, validate_mesaj_complex, validate_fara_link,
    validate_tip_mesaj_selectat, validate_cnp, validate_email_temporar,
    validate_format_text, validate_majuscula_dupa_separator, validate_fara_simboluri
)
    
class CustomUserCreationForm(UserCreationForm):
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if telefon and not telefon.isdigit():
            raise forms.ValidationError("Numărul de telefon trebuie să conțină doar cifre.")
        if telefon and len(telefon) < 10:
            raise forms.ValidationError("Numărul de telefon trebuie să aibă minim 10 cifre.")
        return telefon
        
    def clean_data_nasterii(self):
        data_nasterii = self.cleaned_data.get('data_nasterii')
        if data_nasterii:
            validate_varsta_majora(data_nasterii) 
        return data_nasterii
        
    def clean_oras(self):
        oras = self.cleaned_data.get('oras')
        if oras and len(oras) < 3:
            raise forms.ValidationError("Numele orașului trebuie să aibă minim 3 caractere.")
        return oras

    class Meta(UserCreationForm.Meta):
        model = CustomUser 
        fields = UserCreationForm.Meta.fields + (
            'email', 
            'first_name', 
            'last_name',  
            'data_nasterii', 
            'telefon', 
            'adresa', 
            'oras', 
            'judet', 
            'cod_postal'
        )
        
        labels = {
            'username': 'Nume utilizator',
            'email': 'Adresă email',
            'first_name': 'Prenume',
            'last_name': 'Nume de familie',
            'data_nasterii': 'Data nașterii',
            'telefon': 'Telefon',
            'adresa': 'Adresă',
            'oras': 'Oraș',
            'judet': 'Județ',
            'cod_postal': 'Cod poștal',
        }

class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Rămâneți logat'
    )
        

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['nume', 'bio', 'imagine', 'gen_muzical'] 
        labels = {
            'nume': 'Numele Artistului',
            'bio': 'Biografie',
            'imagine': 'Poza Artist',
            'gen_muzical': 'Gen Muzical'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_nume(self):
        nume = self.cleaned_data.get('nume')
        if len(nume) < 3:
            raise forms.ValidationError("Numele trebuie sa contina cel putin 3 caractere.")
        return nume

class ArtistFilterForm(forms.Form):
    nume = forms.CharField(label="Nume artist", required=False, 
                           widget=forms.TextInput(attrs={'placeholder': 'Cauta dupa nume...'}))
    
    gen_muzical = forms.ModelChoiceField(
        queryset=GenMuzical.objects.all(),
        required=False,
        empty_label="Toate genurile",
        label="Gen Muzical"
    )
    
    an_formare_min = forms.IntegerField(label="An formare (Min)", required=False)
    an_formare_max = forms.IntegerField(label="An formare (Max)", required=False)
    
    per_page = forms.ChoiceField(
        choices=[(5, '5 pe pagina'), (10, '10 pe pagina'), (20, '20 pe pagina')],
        required=False,
        label="Afisare",
        initial=5
    )

    def clean_an_formare_min(self):
        an_min = self.cleaned_data.get('an_formare_min')
        if an_min and an_min < 1800:
            raise forms.ValidationError("Anul nu poate fi mai mic de 1800.")
        return an_min

    def clean_an_formare_max(self):
        an_max = self.cleaned_data.get('an_formare_max')
        current_year = timezone.now().year
        if an_max and an_max > current_year:
            raise forms.ValidationError(f"Anul nu poate fi in viitor (mai mare de {current_year}).")
        return an_max

    def clean(self):
        cleaned_data = super().clean()
        an_min = cleaned_data.get('an_formare_min')
        an_max = cleaned_data.get('an_formare_max')

        if an_min and an_max and an_min > an_max:
            raise forms.ValidationError("Anul minim nu poate fi mai mare decat anul maxim.")

class ContactForm(forms.Form): #l5 1
    TIP_MESAJ_CHOICES = [
        ('neselectat', '--- Alegeti o optiune ---'),
        ('reclamatie', 'Reclamatie'),
        ('intrebare', 'Intrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare'),
    ]

    nume = forms.CharField(
        max_length=10, 
        required=True,
        validators=[validate_format_text, validate_majuscula_dupa_separator]
    )
    
    prenume = forms.CharField(
        max_length=10, 
        required=False,
        validators=[validate_format_text, validate_majuscula_dupa_separator]
    )
    
    cnp = forms.CharField(
        max_length=13, 
        min_length=13, 
        required=False, 
        label="CNP",
        validators=[validate_cnp] 
    )
    
    data_nasterii = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_varsta_majora] 
    )
    
    email = forms.EmailField(
        required=True,
        validators=[validate_email_temporar] 
    )
    
    confirmare_email = forms.EmailField(
        required=True, 
        label="Confirmare E-mail"
    )
    
    tip_mesaj = forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES, 
        required=True, 
        initial='neselectat',
        label="Tipul mesajului",
        validators=[validate_tip_mesaj_selectat]
    )
    
    subiect = forms.CharField(
        max_length=100, 
        required=True,
        validators=[validate_format_text, validate_fara_link]
    )
    
    minim_zile_asteptare = forms.IntegerField(
        required=True, 
        min_value=0,
        max_value=30,
        label="Minim zile asteptare",
        help_text="Pentru review-uri/cereri minimul de zile de asteptare trebuie setat de la 4 incolo iar pentru cereri/intrebari de la 2 incolo. Maximul e 30."
    )
    
    mesaj = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'rows': 5}),
        label="Mesaj (Va rugam sa va si semnati la final)",
        validators=[validate_mesaj_complex, validate_fara_link]
    )

    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirmare_email')
        if email and confirm_email and email != confirm_email:
             self.add_error('confirmare_email', "Adresele de email nu coincid.")

        tip_mesaj = cleaned_data.get('tip_mesaj')
        zile_asteptare = cleaned_data.get('minim_zile_asteptare')
        if tip_mesaj and zile_asteptare is not None: 
             if tip_mesaj in ['review', 'cerere'] and zile_asteptare < 4:
                self.add_error('minim_zile_asteptare', "Pentru 'Review' sau 'Cerere', minimul este de 4 zile.")
             if tip_mesaj in ['programare', 'intrebare'] and zile_asteptare < 2:
                self.add_error('minim_zile_asteptare', "Pentru 'Programare' sau 'Intrebare', minimul este de 2 zile.")

        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')
        if cnp and data_nasterii and len(cnp) == 13:
             an_cnp = int("19" + cnp[1:3])
             luna_cnp = int(cnp[3:5])
             zi_cnp = int(cnp[5:7])
             if data_nasterii.year != an_cnp or data_nasterii.month != luna_cnp or data_nasterii.day != zi_cnp:
                 self.add_error('cnp', "Data de naștere din CNP nu corespunde cu data nașterii introdusă.")

        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')
        if mesaj and nume:
             mesaj_curat = mesaj.strip().lower()
             nume_curat = nume.lower()
             if not mesaj_curat.endswith(nume_curat):
                 self.add_error('mesaj', f"Mesajul trebuie să se încheie cu semnătura dumneavoastră ({nume}).")

        return cleaned_data

class AlbumForm(forms.ModelForm):
    cost_productie = forms.DecimalField(
        label="Cost Producție (RON)",
        min_value=0,
        required=True,
        help_text="Introduceți costul total de producție al albumului."
    )
    marja_profit = forms.IntegerField(
        label="Marjă Profit (%)",
        min_value=0,
        max_value=1000,
        required=True,
        initial=20, 
        help_text="Procentul de profit dorit (între 0% și 1000%)."
    )

    class Meta:
        model = Album
        fields = ['titlu', 'artist', 'data_lansarii', 'gen', 'coperta']
        
        labels = {
            'titlu': 'Titlul Oficial al Albumului',
            'data_lansarii': 'Data Lansării pe Piață',
            'artist': 'Artistul Principal'
        }
        
        widgets = {
            'data_lansarii': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titlu'].validators.extend([validate_format_text, validate_fara_simboluri])

    def clean_cost_productie(self):
        cost = self.cleaned_data.get('cost_productie')
        if cost and cost > 10000:
            raise ValidationError("Costul de producție pare prea mare. Verificați suma.")
        return cost

    def clean_data_lansarii(self):
        data = self.cleaned_data.get('data_lansarii')
        if data and data.year < 2000:
            raise ValidationError("Nu acceptăm albume lansate înainte de anul 2000.")
        return data

    def clean_marja_profit(self):
        marja = self.cleaned_data.get('marja_profit')
        if marja and marja % 5 != 0:
             raise ValidationError("Marja de profit trebuie să fie un multiplu de 5 (ex: 15%, 20%).")
        return marja

    def clean(self):
        cleaned_data = super().clean()
        cost = cleaned_data.get('cost_productie')
        marja = cleaned_data.get('marja_profit')

        if cost and marja and cost > 5000 and marja > 100:
            raise ValidationError("Pentru costuri de producție mari (>5000 RON), marja de profit nu poate depăși 100%.")
        
        return cleaned_data