from playwright.sync_api import sync_playwright
import time

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
        time.sleep(10) #vai esperar 5 segundo ate fechar meu navegador
        # Preenchimento de filtros

if __name__ == "__main__":
    procurar_licitacoes()