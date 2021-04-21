int leitura;

void setup() {
  Serial.begin(9600);
  pinMode(3, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    leitura = Serial.read();
     if(leitura == 49){
      digitalWrite(3, HIGH);
    }
    else if(leitura == 48){
      digitalWrite(3, LOW);
    }
    Serial.println(leitura);
    }
}
