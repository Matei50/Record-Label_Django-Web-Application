class GetIP:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        request.proprietate_noua=17       
        # se apelează (indirect) funcția de vizualizare (din views.py)
        response = self.get_response(request)      

        # putem adauga un header HTTP pentru toate răspunsurile
        response['header_nou'] = 'valoare'
        
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
          
            content = response.content.decode('utf-8')
           
        return response