#Backend do site do arduino
#Nota: O codigo funciona apenas quando tem pelomenos 2 linha de dados,
#-> caso n tenha adicione ligando e desligando e em seguida reinicie o codigo

#Bibliotecas:
#baixar bibliotecas:
#pip install -Iv Flask==1.1.2
#pip install -Iv pandas==1.0.1
#pip install -Iv scikit-learn==0.24.1
#pip install -Iv requests==2.25.1

#Flask: Usado para a interação do site html com o python
from flask import Flask, render_template, redirect

#Time: Usado para pausar o servidor por um tempo
import time

#Requests: mandar requisições para um ip/site
import requests

#pandas: Usado para ler e escrever em Excel
import pandas as pd

#datetime: Usado para pegar a hora atual do servidor
import datetime as dt

#sklearn: Usado para fazer a predição da luz
from sklearn import tree


#nessa linha é instanciado um objeto da classe Flask,
#->é ele que vamos utilizar para configurar a nossa aplicação e para executa-la
#->com o servidor de testes do próprio Flask.
app = Flask(__name__)

#Função para pegar a data, e as horas e minutos em segundos;
def tempo():
    data_atual = dt.datetime.now()
    minutos = data_atual.hour*60
    segundos = (minutos+data_atual.minute)*60
    temp = segundos + data_atual.second
    return data_atual,temp

#Função que vai fazer a predição e mandar mensagem pro arduino
def ML():
    global clf
    try:
        print(clf)
        clf.predict([[1,1,1,1]])
    except:
        print('ML n funcionando, Reinicie caso tenha dados suficientes')
        global teste
        teste = False
    #Começar um loop fazendo a Machine learning ficar ativada ate dar ordem de desativar
    while teste:
        data,temp = tempo()
        valor = clf.predict([[data.day,data.month,temp,data.year]])
        time.sleep(0.1)
        if valor[0] == 1:
            requests.get('http://ip-Do-ESP-Do-Arduino?pin=131')
        else:
            requests.get('http://ip-Do-ESP-Do-Arduino?pin=130')
        time.sleep(1)


#@app.route('/') é um decorator responsável por interpretar a rota que acessamos,
#-> então, assim que é acessada a url / como é configurado na linha acima,
#-> a função que está abaixo é responsável por enviar uma rota ao navegador.

#Função da pagina Home: Escolher as opções
@app.route('/')
def index():
    return render_template('index.html')

#Função da pagina Start: Começar o loop da Machine
@app.route('/start')
def start():
    #global: define que a variavel global sera usada
    global teste
    teste = True
    ML()
    return redirect('/')

#Função da pagina Stop: Parar o loop da Machine
@app.route('/stop')
def stop():
    global teste
    teste = False
    ML()
    return redirect('/')

#Função da pagina Ligar: Ligar a luz manualmente e adicionar nos dados da Machine e Excel
@app.route('/ligar')
def ligar():
    requests.get('http://ip-Do-ESP-Do-Arduino?pin=131')
    global df1
    global clf
    data,temp = tempo()
    #df2: variavel que recebe o formato de dados do pandas
    df2 = pd.DataFrame([[data.day, data.month, temp, 1, data.year]],columns=list('ABCDE'))
    #append: juntando as variaveis
    df1= df1.append(df2, ignore_index=True)
    #to_excel: salvando o formato da variavel no excel
    df1.to_excel("dados.xlsx", index=False)
    #separando os valores de dias e horas com o valor "Ligado" e "Desligado"
    x = df1.drop("D", axis=1).values
    y = df1["D"].values
    try:
        clf = clf.fit(x,y)
    except:
        print('ML n funcionando, Reinicie caso tenha dados suficientes')
    print(df1)
    return redirect('/')

#Função da pagina Desligar: Desligar a luz manualmente e adicionar nos dados da Machine e Excel
@app.route('/desligar')
def desligar():
    requests.get('http://ip-Do-ESP-Do-Arduino?pin=130')
    global df1
    global clf
    data,temp = tempo()
    df2 = pd.DataFrame([[data.day, data.month, temp, 0, data.year]],columns=list('ABCDE'))
    df1= df1.append(df2, ignore_index=True)
    df1.to_excel("dados.xlsx", index=False)
    x = df1.drop("D", axis=1).values
    y = df1["D"].values
    try:
        clf = clf.fit(x,y)
    except:
        print('ML n funcionando, Reinicie caso tenha dados suficientes')
    print(df1)
    return redirect('/')
#Começo do script:
teste = False
#read_excel: ler o arquivo Excel
try:
    df1 = pd.read_excel("dados.xlsx")
except:
    df1 = pd.DataFrame(columns=list('ABCDE'))
    df1.to_excel("dados.xlsx", index=False)
x = df1.drop("D", axis=1).values
y = df1["D"].values
clf = tree.DecisionTreeClassifier()
try:
    clf = clf.fit(x,y)
except:
    print('Sem dados para Machine learning')
print(df1)

#Só queremos que nossa função app.run() seja executada se o módulo for o principal.
#-> Caso ele tenha sido importado, a aplicação só deverá ser executada se app.run()
#-> for chamado explicitamente.
if __name__ == "__main__":
    #app.run()
    #-> essas instruções definem que quando o "run.py" for executado via linha de
    #-> comando. O Flask deverá iniciar o seu servidor interno para executar a
    #-> aplicação, como no construtor foi passado o valor "True" para a chave
    #-> "debug", o servidor será iniciado no modo debug; assim, quando forem
    #-> feitas modificações no código e elas forem salvas o servidor irá
    #-> reiniciar automaticamente para que você possa testar o novo código.
    app.run()
