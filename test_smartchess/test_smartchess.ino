
int outPins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
int muxPins[3] = {12, 11, 10};
void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  for (int i = 0; i < 8; i++) {
    pinMode(outPins[i], OUTPUT);
  }
  pinMode(muxPins[0], OUTPUT);
  pinMode(muxPins[1], OUTPUT);
  pinMode(muxPins[2], OUTPUT);


  digitalWrite(muxPins[0], LOW);
  digitalWrite(muxPins[1], LOW);
  digitalWrite(muxPins[2], LOW);

  for(int i = 0; i < 8; i++){
    digitalWrite(outPins[i], HIGH);
  }
  //digitalWrite(outPins[4], LOW);
  //digitalWrite(outPins[1], LOW);
  digitalWrite(outPins[2], LOW);
  //digitalWrite(outPins[7], LOW);


  for(int i = 0; i<8; i++){
  
    
  digitalWrite(muxPins[0], LOW);
  digitalWrite(muxPins[1], LOW);
  digitalWrite(muxPins[2], LOW);
  delay(1000);

  digitalWrite(muxPins[0], HIGH);
  digitalWrite(muxPins[1], LOW);
  digitalWrite(muxPins[2], LOW);

  delay(1000);

  digitalWrite(muxPins[0], LOW);
  digitalWrite(muxPins[1], HIGH);
  digitalWrite(muxPins[2], LOW);
  delay(1000);

  digitalWrite(muxPins[0], HIGH);
  digitalWrite(muxPins[1], HIGH);
  digitalWrite(muxPins[2], LOW);
  delay(1000);
  }
}

void loop() {
  // put your main code here, to run repeatedly:



}
