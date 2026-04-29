int main (void) {
  init();
  pinMode(3, OUTPUT); // v outuput lo setto al pin 3
  pinMode(A0, INPUT); //v generata da arduino e misurata (prendo il pin 3 e lo porto in a0)
  pinMode(A4, INPUT); // v hall misurata in arrivo dalla sonda Misura di HAll
  Serial2.begin(9600); // pin 15 RX e 14 TX tra arduino  e adattatore seriale
  Serial.begin(9600); // tra arduino e computer 

  int f = 5; //numero di n misure in semiperiodo per b positivo e negativo
  int Nperiodi = 150;
  float V_ard_low[f], V_ard_high[f];
  float V_hall_high[f], V_hall_low[f];
  float dV_hall, dV_ard;
  float incremento_corrente = 0.1; // di quanto incremento B
  float I_max = 1.2;
  delay(3000);
  Serial2.println("OP1 1");
  delay(3000);
  Serial2.println("I1 0");
  delay(3000);
  Serial2.println("V1 30");
  delay(3000);// millisecondi

  // setto fondoscala lettura V hall in base alla sua tensione massima
  //analogReference(INTERNAL1V1);  //fondoscala lettura 1.1V
  //analogReference(INTERNAL2V56); //fondoscala lettura 2.56V
  analogReference(DEFAULT);      //fondoscala lettura 5V
  float fondoscalaV = 5.0;     // fondoscala in volt settato sopra

 // ho dodici incrementi di B, dentro 150 periodi, per ogni semi-periodo ho 5 misure
  
  for(float I=0; I <= I_max ; I+= incremento_corrente){
    Serial.println("CORRENTE");
    Serial.println(I);

    delay(500);
    String corrente = "I1 " + String(I); // manda al generatore delle bobine
    Serial2.println(corrente);
    
    for(int M = 0; M <= Nperiodi ; M += 1){ // M misure di un "periodo"
      for (int N = 0 ; N < f ; N += 1){ //N misure 5V
        digitalWrite(3, HIGH); // setto il pin 3 a 5V con High
        V_ard_high[N] = digitalRead(A0) ? 5.0 : 0.0; // if 3 veramente High -> 5.0V, if 3 veramente Low -> 0.0V
        
        delay(30);
        V_hall_high[N] = float(analogRead(A4))*fondoscalaV/1023; //float(map(analogRead(A4), 0, 1023, 0, 5000))/1000;
      }

      for(int K=0 ; K < f ; K += 1){ //N misure 0V
        digitalWrite(3, LOW);
        V_ard_low[K] = digitalRead(A0) ? 5.0 : 0.0; // if 3 veramente High -> 5.0V, if 3 veramente Low -> 0.0V

        delay(30);
        V_hall_low[K] = float(analogRead(A4))*fondoscalaV/1023; //float(map(analogRead(A4), 0, 1023, 0, 5000))/1000;
      }
// comunico con il computer e gli invio i dati che ho trovato 
      Serial.println("VARD"); // questo è um controllo in più
      for ( int T = 0 ; T < f ; T++){
        dV_ard = (V_ard_high[T]-V_ard_low[T]); // high-low
        String vard = String(dV_ard, 4) + " "; // converto in stringa
        Serial.print(vard);  // PRINTO N VALORI
      }
      Serial.println(" ");

      Serial.println("VHALL");
      for ( int T = 0 ; T < f ; T++){
        dV_hall = (V_hall_high[T]-V_hall_low[T]);
        String vhall = String(dV_hall, 4) + " ";
        Serial.print(vhall); //PRINTO N VALORI 
      }
      Serial.println(" ");
    }
    
    delay(100);
  }
  delay(100);
  Serial.println("BREAK");
  delay(100);
  
  return 0;
}
