from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

def procurar_licitacoes():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False) #inicia nosso navegador , nesse caso o crhome
        pagina = navegador.new_page() #abre uma nova aba no nosso navegador
        pagina.goto("http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro.asp") #vai ate nossa pagina de licitacoes

        pagina.fill('input[name="dt_publ_ini"]', '01/04/2025') #preenche o camppo de data inicial
        pagina.fill('input[name="dt_publ_fim"]', '14/04/2025') #preenche o camppo de data fim
        pagina.click('input[name="ok"]')  # vai clickar no botao de ok para os filtros

        #marca todas os filtros das licitacoes
        pagina.click('//*[@id="frmLicitacao"]/table/tbody/tr[2]/td/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[7]/td/input')
        pagina.click('input[name="ok"]')  # vai clickar no botao de ok para os filtros
        pagina.click('input[name="itens"]') #vai clickar na aba de inten e downloads

        # Espera por algum seletor específico (por segurança) , para garantir que toda a pagina carregou
        pagina.wait_for_timeout(3000)
        html = pagina.content()
        soup = BeautifulSoup(html, 'html.parser')

        #encontra e printa o elemento p do html
        for p in soup.find_all('p'):
            print(p.text)
        #encontra e printa o elemento b do html
        for b in soup.find_all('b'):
            if b.get_text().strip() == "Objeto:":
                texto_completo = b.next_sibling
                if texto_completo:
                    texto_final = texto_completo.replace('\xa0', ' ').strip()
                    print(texto_final)
        # encontra e printa o elemento span do html
        for span in soup.find_all('span'):
            print(span.text)
        # encontra e printa o elemento td do html
        for td in soup.find_all('td'):
            print(td.text)
        time.sleep(15) #vai esperar 5 segundo ate fechar meu navegador

if __name__ == "__main__":
    procurar_licitacoes()