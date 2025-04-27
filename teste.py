import requests
from bs4 import BeautifulSoup

# Fazendo a requisição para a página de produtos
url = 'https://lista.mercadolivre.com.br/pcs#D[A:pcs]'
response = requests.get(url)
html = response.text

# Criando o objeto Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Buscando todos os elementos que contêm os preços dos produtos
precos = soup.find_all('span', class_='andes-money-amount__fraction')

# Extraindo e imprimindo os preços
for preco in precos:
    print(preco.text.strip())