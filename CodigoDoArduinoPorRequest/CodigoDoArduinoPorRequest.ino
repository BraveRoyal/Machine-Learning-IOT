#include <SoftwareSerial.h>

 
#define DEBUG true
 
 
//Cria o objeto para usar a biblioteca Sotfware Serial
//RX do arduino é o pino 2
//TX do arduino é o pino 3
//O TX do esp8266 deve ser ligado no pino 2 do arduino
//O RX do esp8266 deve ser ligado no pino 3 do arduino
 
SoftwareSerial esp8266(2,3);

//declara os pinos do led rgb 
int luz =13;
 


 

 
void setup()
{
  //um pequeno delay no arduino
  //para evitar que envie comandos antes do esp8266 dar o start
  delay(500);
  //Seta ambas seriais para a velocidade de 9600
  Serial.begin(9600);
  //(em alguns casos a velocidade do seu esp8266 pode estar diferente desta)
  esp8266.begin(9600);
  
  //declara os pinos como saida
  pinMode(luz,OUTPUT);
  digitalWrite(luz,LOW);
   delay(2000);
   //liga o led azul para informar o inicio dos comandos AT
  
 
  
 
 
 
  //Envia o comandos AT
 
  // reseta o modulo
  sendData("AT+RST\r\n",2000,DEBUG);
  // configure as access point e estação (ambos)
  sendData("AT+CWMODE=3\r\n",1000,DEBUG);
  //conecta ao roteador com a senha  
  //(esta configuração deve ser feita, pois o seu roteador tem nome diferente do meu e senha)
  sendData("AT+CWJAP=\"ROTEADOR\",\"SENHA\"r\n",10000,DEBUG);
  //Retorna o IP ao qual está conectado e o IP de Station
  sendData("AT+CIFSR\r\n",1000,DEBUG);
  //Habilita multiplas conexões
  sendData("AT+CIPMUX=1\r\n",1000,DEBUG);
  //Habilita ao servidor a porta 80
  sendData("AT+CIPSERVER=1,80\r\n",1000,DEBUG);
}
 
void loop()
{
 
 

 
  //verifica se o esp8266 esta enviando mensagem e esta disponivel
  if(esp8266.available())
  {
 
   
    if(esp8266.find("+IPD,"))
    {
      
  
 
     delay(1000); 
     //recupera apenas comando ASCII
     int connectionId = esp8266.read()-48; 
          
     //avança o cursor até a palavra  "pin="    
     esp8266.find("pin="); 
     
     //armazena o primeiro numero.. Ex: Se for pino 13 armazenara 1 e logo em seguida multiplica por 10 para o calculo do pino   
     int pinNumber = (esp8266.read()-48)*10; 
     //armazena o segundo numero e soma com o primeiro...  Ex : Se o numero for 13 a soma sera 10 + 3 que resultara no pino ao qual foi enviado pela pagina Web
     pinNumber += (esp8266.read()-48); 
     //armazena o terceiro dado que correponde ao status do led '1' para ligado e '0' para desligado
     int statusLed =(esp8266.read()-48);
     
     //Escreve o satus com o metodo digital Write
     //Ex se recebeu 131
     //o pino 13 sera ligado
     //digitalWrite(13, 1);
     digitalWrite(pinNumber, statusLed);
  
     // finaliza o comando no esp8266
     String closeCommand = "AT+CIPCLOSE="; 
     closeCommand+=connectionId; 
     closeCommand+="\r\n";
     
     //Encerra a conexao
     sendData(closeCommand,1000,DEBUG); 
     
     
    
    }

    
  }
}
 
 
 //Metodo que envia os comandos para o esp8266
String sendData(String command, const int timeout, boolean debug)
{
    //variavel de resposta do esp8266
    String response = "";
   
    // send a leitura dos caracteres para o esp8266
    esp8266.println(command);
   
    long int time = millis();
   
    while( (time+timeout) > millis())
    {
      while(esp8266.available())
      {
       
 
        //Concatena caracter por caractere recebido do modulo esp8266
        char c = esp8266.read();
        response+=c;
      }  
    }
   
    //debug de resposta do esp8266
    if(debug)
    {
      //Imprime o que o esp8266 enviou para o arduino
      Serial.println("Arduino : " + response);
    }
   
    return response;
}
