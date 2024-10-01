from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256



def home(request):
     return render(request, 'home copy.html')


def login(request):
    if request.session.get('usuario'):
        return redirect('/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()
    usuario = Usuario.objects.filter(nome=nome).filter(senha=senha)
    senha = Usuario.objects.filter(senha=senha)

    # Nome de usuario não cadastrado
    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')

    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect('/home/')
    
  

    return HttpResponse(f"{nome} e {senha}")


def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email=email)
    nome_de_usuario = Usuario.objects.filter(nome=nome)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/cadastro/?status=1')

    if len(senha.strip()) < 8:
        return redirect('/cadastro/?status=2')

    if len(usuario) > 0:
        return redirect('/cadastro/?status=3')

    if len(nome_de_usuario) > 0:
        return redirect('/cadastro/?status=4')

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome, email=email, senha=senha)
        usuario.save()

        return redirect('/cadastro/?status=0')

    except:
        return redirect('/cadastro/?status=5')


def sair(request):
    request.session.flush()
    return redirect('/auth/login/')


def Sigfis(request):
    status = None  # Inicialize a variável status
    if request.method == "POST":
        status = 'iniciado'  # Define o status como 'iniciado' ao clicar no botão
        try:
            Automate_sigfis()  # Aqui está a função de automação
            status = '0'  # Define o status como '0' em caso de sucesso
        except Exception as e:
            status = '1'  # Define o status como '1' em caso de erro
            print(f"Erro ao iniciar a automação: {e}")

    return render(request, 'sigfis.html', {'status': status})








def Automate_sigfis():
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    from datetime import datetime
    import locale
    import calendar

    import os.path
    import pandas as pd
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    # Define o escopo para acessar Google Sheets e Google Drive
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"]

    # ID da planilha Google Sheets
    # Substitua pelo ID da sua planilha
    SPREADSHEET_ID = "1h9DNMSjTPI3pyTn4XxBfODXCqsguXtAQdDXHuYKazgs"

    # Nome da aba que deseja acessar (neste caso, "Sigfis")
    RANGE_NAME = "Sigfis TAC"  # Nome da aba ou faixa de células




    def main():
        creds = None
        # Verifica se o arquivo token.json existe
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
        # Se não houver credenciais válidas, permite que o usuário faça login.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Salva as credenciais para a próxima execução
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            # Inicializa o serviço do Google Sheets API
            service = build("sheets", "v4", credentials=creds)

            # Chama a API do Google Sheets
            sheet = service.spreadsheets()

            # Lê a aba específica
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return None  # Retorna None se não encontrar dados

            # Cria um DataFrame a partir dos dados da aba
            df_TAC = pd.DataFrame(values[1:], columns=values[0])  # headers as columns
            return df_TAC  # Retorna o DataFrame

        except HttpError as err:
            print(err)
            return None  # Retorna None em caso de erro


    if __name__ == "__main__":
        df_TAC = main()  # Captura o retorno da função main
        if df_TAC is not None:
            print("O DataFrame foi criado com sucesso!")
            print(df_TAC.head())  # Exibe as primeiras linhas do DataFrame
        else:
            print("Não foi possível criar o DataFrame.")


    # LOCAL
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


    # Inicializa o serviço do WebDriver
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)

    # Acessa a página desejada
    navegador.get('https://www.tcerj.tc.br/etcerj/')

    # Preenche os campos de login
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/section/div/div[2]/form/div[1]/div/div/input').send_keys("17475054713")
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/section/div/div[2]/form/div[2]/div/div/input').send_keys('123456')

    # Clica no botão de login
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/section/div/div[2]/form/div[3]/div/div/button').click()

    # Clica no link para acessar a página desejada
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/aside/section/div/div/div[1]/div/form[2]/div[2]/div/a').click()

    # Espera um pouco para garantir que a página carregue completamente
    time.sleep(3)

    # Clica no elemento que abre a lista
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/aside/section/div/div/div[1]/div/div[2]/div/div/div/div[2]/select').click()

    # Espera um pouco para garantir que a lista seja exibida
    time.sleep(1)

    # Clica na segunda opção da lista
    segunda_opcao_xpath = '/html/body/div[2]/aside/section/div/div/div[1]/div/div[2]/div/div/div/div[2]/select/option[2]'
    navegador.find_element(By.XPATH, segunda_opcao_xpath).click()

    # Clica no botão para confirmar a seleção
    navegador.find_element(
        By.XPATH, '/html/body/div[2]/aside/section/div/div/div[1]/div/div[2]/div/div/div/div[3]/button').click()


    # Espera um pouco para garantir que a próxima página carregue
    time.sleep(3)


    # ITEM DE LUPA
    navegador.find_element(
        By.XPATH, '/html/body/app-root/app-site/div/div/div/app-home/div/div[3]/acesso-rapido[1]/div/div[2]/span[1]/a').click()


    time.sleep(1)


    for index, row in df_TAC.iterrows():

        # INCLUIR
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-consulta/app-ajuste-contas-consulta-base/div[1]/div/div/div[2]/button').click()

        # INFORMAÇÕES

        TAC = row['TAC']
        ano_TAC = row['Ano']

        NTAC = TAC + '/' + ano_TAC
        processo = row['Processo']
        valor = row['Valor']
        cnpj = row['CNPJ']
        empresa = row['Nome da empresa']
        objeto = row['Objeto']

        boletim = row['Boletim Oficial']
        lei = '14133/21'
        data_assinatura = row['Assinatura']
        data_publicacão = row['Publicação']

        secretaria = 'CÉLIA SERRANO DA SILVA'
        secretaria_CPF = '392.515.002-15'

        CPF = row['CPF']

        nome_socio_bruto = row['Nome sócio']
        nome_socio_tratado = nome_socio_bruto.split(" ", 1)

        nome_socio = nome_socio_tratado[1]

        periodo = row['Período']
        qtd_barras = periodo.count("/")

        if qtd_barras == 1:

            separação = periodo.split("/")
            mes = separação[0]
            ano = int(separação[1])

            # Obtém o mês como um número (1 para Janeiro, 2 para Fevereiro, etc.)
            mes_num = datetime.strptime(mes, "%B").month

            # Obtém o ano atual
            ano_atual = datetime.now().year

            # Cria a data inicial do mês
            data_inicial1 = datetime(ano, mes_num, 1)
            data_final1 = calendar.monthrange(ano, mes_num)[1]

            data_final2 = datetime(ano, mes_num, data_final1)

            data_inicial = data_inicial1.strftime("%d/%m/%Y")
            data_final = data_final2.strftime("%d/%m/%Y")

        elif qtd_barras == 2:
            data_inicial = periodo
            data_final = periodo

            print(data_inicial)
            print(data_final)

        elif qtd_barras == 4:

            sub = periodo.replace("a", "-")

            separação = sub.split(" - ")

            data_inicial = separação[0]

            data_final = separação[1]

            print(data_inicial)
            print(data_final)

        else:
            data_inicial = '01/01/2024'
            data_final = '31/01/2024'

        # NÚMERO DO TAC
        input_element = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[1]/div[2]/div/input-text/div/input'))
        )

        input_element.send_keys(NTAC)

        # Nº PROCESSO
        # Espera até que a caixa de texto esteja disponível e então escreve o texto nela
        input_element2 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[1]/div[3]/div/input-text/div/input'))
        )

        input_element2.send_keys(processo)

        # VALOR
        input_element3 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[1]/div[4]/div/div/input-currency/div/input'))
        )

        input_element3.send_keys(valor)

        # RAZÃO SOCIAL
        input_element5 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[2]/div[1]/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[2]/div/input-text/div/input'))
        )

        input_element5.send_keys(empresa)

        # CNPJ
        input_element4 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[2]/div[1]/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[1]/div/div/input'))
        )

        input_element4.send_keys(cnpj)

        # POSSUI CONTRATO

        # Clica na segunda opção da lista
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[2]/div[2]/div/input-select/select').click()

        time.sleep(1)

        # Clica na terceira opção da lista = 'Não'
        terceira_opcao_xpath = '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[2]/div[2]/div/input-select/select/option[3]'
        navegador.find_element(By.XPATH, terceira_opcao_xpath).click()

        # OBJETO
        input_element6 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[3]/div/div/input-textarea/textarea'))
        )

        input_element6.send_keys(objeto)

        # BOLETIM
        input_element7 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[4]/div[1]/div/input-text/div/input'))
        )

        input_element7.send_keys(boletim)

        # LEI AUTORIZATIVA
        input_element8 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[4]/div[3]/div/input-text/div/input')))

        input_element8.send_keys(lei)

        # DATA DE ASSINATURA
        input_element11 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[5]/div[1]/div/input-date/div/input'))
        )

        input_element11.send_keys(data_assinatura)

        # DATA INICIAL
        input_element9 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[5]/div[2]/div/input-date/div/input')))

        input_element9.send_keys(str(data_inicial))

        # DATA FINAL
        input_element10 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[5]/div[3]/div/input-date/div/input')))

        input_element10.send_keys(str(data_final))

        # DATA DE PUBLICAÇÃO
        input_element12 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[5]/div[4]/div/input-date/div/input'))
        )

        input_element12.send_keys(str(data_publicacão))

        # SALVAR
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[1]/div[6]/div/button').click()

        time.sleep(2)

        # OK
        navegador.find_element(
            By.XPATH, 'html/body/div/div/div[3]/button[1]').click()

        # ABA 2
        # navegador.find_element(By.XPATH,').click()

        time.sleep(1)

        # Usa JavaScript para scrollar até o botão
        navegador.execute_script("window.scrollTo(0, 0);")

        # Localiza o botão que você precisa clicar
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/ul/li[2]/a').click()

        # REPRESENTANTE DA ADMIISTRAÇÃO PÚBLICA

        # Incluir
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[2]/app-responsaveis-listagem/div/div/div[2]/button').click()

        time.sleep(1)

        # Abrir lista
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select').click()

        # Seleção
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select/option[2]').click()

        # NOME SECRETARIA
        input_element13 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[2]/div/input-text/div/input'))
        )
        input_element13.send_keys(str(secretaria))

        # SECRETARIA CPF
        input_element14 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[1]/div/div/input'))

        )

        input_element14.send_keys(str(secretaria_CPF))

        # SALVAR
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[3]/div/button').click()

        time.sleep(2)

        # OK
        navegador.find_element(
            By.XPATH, '/html/body/div/div/div[3]/button[1]').click()

        time.sleep(1)

        # ORDENADOR DE DESPESA

        # Incluir
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[2]/app-responsaveis-listagem/div/div/div[2]/button').click()

        time.sleep(1)

        # Abrir lista
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select').click()

        # Seleção
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select/option[4]').click()

        # NOME SECRETARIA
        input_element16 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[2]/div/input-text/div/input'))
        )
        input_element16.send_keys(str(secretaria))

        # SECRETARIA CPF
        input_element17 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[1]/div/div/input'))

        )

        input_element17.send_keys(str(secretaria_CPF))

        # SALVAR
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[3]/div/button').click()

        time.sleep(2)

        # OK
        navegador.find_element(
            By.XPATH, '/html/body/div/div/div[3]/button[1]').click()

        time.sleep(1)

        # REPRESENTANTE DA CONTRATADA

        # Incluir
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[4]/div/div/form/tabset/div/tab[2]/app-responsaveis-listagem/div/div/div[2]/button').click()

        time.sleep(1)

        # Abrir lista
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select').click()

        # Seleção
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[1]/div/div/input-select/select/option[3]').click()

        # NOME DO CONTRATADO
        input_element19 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[2]/div/input-text/div/input'))
        )
        input_element19.send_keys(str(nome_socio))

        # CPF DO CONTRATADO
        input_element20 = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[2]/div/form/div[2]/div/div/app-pessoa-pesquisa-cadastro/div/div/div/div[2]/div[1]/div/div/input'))

        )

        input_element20.send_keys(str(CPF))

        # SALVAR
        navegador.find_element(
            By.XPATH, '/html/body/modal-container/div/div/app-responsavel-modal-cadastro/div/div/app-modal/div[3]/div/button').click()

        time.sleep(2)

        # OK
        navegador.find_element(
            By.XPATH, '/html/body/div/div/div[3]/button[1]').click()

        time.sleep(1)

        # SALVAR
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[1]/div/div/div[2]/div[1]/button[2]').click()

        time.sleep(1)

        # OK
        navegador.find_element(
            By.XPATH, '/html/body/div/div/div[3]/button[1]').click()

        time.sleep(1)

        # CANCELAR
        navegador.find_element(
            By.XPATH, '/html/body/app-root/app-site/div/div/div/app-ajuste-contas-cadastro/app-cadastro-com-alteracao-status-base/div/div/div[1]/div/div/div[2]/div[1]/a[1]').click()

        # Você pode fechar o navegador se não precisar mais dele
        # navegador.quit()
