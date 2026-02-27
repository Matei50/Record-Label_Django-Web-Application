from django.contrib import admin
from .models import Artist, Album, Piesa, GenMuzical, CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = "Administrare CasaDeDiscuri"
admin.site.site_title = "Admin pgLang"
admin.site.index_title = "Bun venit in panoul de administrare"

class PiesaInline(admin.TabularInline):
    model = Piesa
    extra = 1 

class GenMuzicalAdmin(admin.ModelAdmin):
    list_display = ('nume', 'slug', 'culoare')
    search_fields = ('nume',)

class ArtistAdmin(admin.ModelAdmin): 
    list_display = ('nume', 'gen_muzical')
    search_fields = ('nume', 'gen_muzical__nume') 
    list_filter = ('gen_muzical',) 
    

    fieldsets = (
        ('Informatii Principale', {
            'fields': ('nume', 'gen_muzical', 'imagine')
        }),
        ('Detalii Suplimentare (Colapsabil)', { 
            'classes': ('collapse',),
            'fields': ('bio',),
        }),
    )


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titlu', 'artist', 'data_lansarii') 
    list_filter = ('artist', 'data_lansarii')
    search_fields = ('titlu', 'artist__nume')
    inlines = [PiesaInline] 
    list_select_related = ('artist',)

class PiesaAdmin(admin.ModelAdmin):
    list_display = ('titlu', 'album', 'numar_piesa', 'durata_formatata')
    list_filter = ('album__artist',)
    search_fields = ('titlu', 'album__titlu')
    list_per_page = 5 

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Date Suplimentare Profil', {
            'fields': ('data_nasterii', 'telefon', 'adresa', 'oras', 'judet', 'cod_postal'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('data_nasterii', 'telefon', 'adresa', 'oras', 'judet', 'cod_postal'),
        }),
    )

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Piesa, PiesaAdmin)
admin.site.register(GenMuzical, GenMuzicalAdmin)
admin.site.register(CustomUser, CustomUserAdmin)