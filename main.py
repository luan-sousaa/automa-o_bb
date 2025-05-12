from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
import reportlab.lib.pagesizes as pagesizes
from reportlab.pdfgen import canvas
from textwrap import wrap
from reportlab.lib.pagesizes import A4
import re

def procurar_licitacoes():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False) #inicia nosso navegador , nesse caso o crhome
        pagina = navegador.new_page() #abre uma nova aba no nosso navegador
        pagina.goto("http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro.asp") #vai ate nossa pagina de licitacoes

        pagina.fill('input[name="dt_publ_ini"]', '21/04/2025') #preenche o camppo de data inicial
        pagina.fill('input[name="dt_publ_fim"]', '27/04/2025') #preenche o camppo de data fim
        pagina.click('input[name="ok"]')  # vai clickar no botao de ok para os filtros

        #marca todas os filtros das licitacoes
        pagina.click('//*[@id="frmLicitacao"]/table/tbody/tr[2]/td/table[2]/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[7]/td/input')
        pagina.click('input[name="ok"]')  # vai clickar no botao de ok para os filtros
        pagina.click('input[name="itens"]') #vai clickar na aba de item e downloads

        # Espera por algum seletor específico (por segurança) , para garantir que toda a pagina carregou
        pagina.wait_for_timeout(3000)
        html = pagina.content()
        soup = BeautifulSoup(html, 'html.parser')

        # variavel auxiliar que ira armazenar o conteudo dos for
        licitacoes = []
        #encontra e printa o elemento p do html
        for p in soup.find_all('p'):
            licitacoes.append(p.get_text())
        #encontra e printa o elemento b do html
        for b in soup.find_all('b'):
            if b.get_text().strip() == "Objeto:":
                texto_completo = b.next_sibling
                if texto_completo:
                    texto_final = texto_completo.replace('\xa0', ' ').strip()
                    licitacoes.append(texto_final)
        # encontra e printa o elemento span do html
        for span in soup.find_all('span'):
            licitacoes.append(span.get_text())
        # encontra e printa o elemento td do html
        for td in soup.find_all('td'):
            licitacoes.append(td.get_text())
        # vai esperar 15 segundo ate fechar meu navegador
        time.sleep(15)
        return licitacoes

#funcao que ira gerar um relatorio por uma IA
dados = procurar_licitacoes()
#api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyASo5XExbsu-UFgHmluhplhF98IOmOLSh0" )
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="Você é um analista de licitações experiente, com profundo conhecimento em editais públicos, concorrências, pregões eletrônicos e processos administrativos. Sua tarefa é analisar os dados a seguir e gerar um relatório profissional e detalhado. O relatório deve conter:Resumo da licitação: tipo, número, órgão responsável e objeto.Análise dos requisitos: principais exigências técnicas e jurídicas.Riscos e oportunidades: o que pode impactar negativamente ou positivamente a participação da empresa.Conclusão e recomendação: se é viável participar da licitação, com justificativa..Maximo de 550 caracteres"),
    contents=f"{dados}"
)


#função que retira os espacos em branco e simbolos do pdf
def limpar_markdown(texto):
    texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
    texto = re.sub(r'\*(.*?)\*', r'\1', texto)
    texto = re.sub(r'##+', '', texto)
    texto = texto.replace('■', '')
    return texto

# Criar um objeto PageSize
page_size = pagesizes.letter

# Criar um objeto Canvas
c = canvas.Canvas('relatorio.pdf',pagesize=A4)
largura, altura = A4
# definir o tamanho da página
c.setPageSize(page_size)

# adicionar texto à página
conteudo = response.text
conteudo_limpo = limpar_markdown(conteudo)


# Texto
c.setFont("Helvetica", 12)
y = altura - 90

# Quebra o texto em linhas com no máximo 200 caracteres
linhas = wrap(conteudo_limpo, width=100)

for linha in linhas:
    c.drawString(50, y, linha)
    y -= 20
    # Se chegar ao final da página, cria nova
    if y < 50:
        c.showPage()
        c.setFont("Helvetica", 12)
        y = altura - 50

# fechar o arquivo PDF
c.showPage()
c.save()

#loop que ira pegar multiplas licitaçoes