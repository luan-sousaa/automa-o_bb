import requests
from bs4 import BeautifulSoup

#input do usuario para colocar o link da licitação
url = input("Link do site para encontrar licitacoes :  ")
#a variavel response guarda a request e pega a url
response = requests.get(url)
response.status_code