
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
  
  /*  
  digitalWrite(muxPins[0], LOW);
  digitalWrite(muxPins[1], LOW);
  digitalWrite(muxPins[2], LOW);
  delay(1000);
  Serial.println("col 1");


  digitalWrite(muxPins[0], HIGH);
  digitalWrite(muxPins[1], LOW);
  digitalWrite(muxPins[2], LOW);
  Serial.println("col 2");

  delay(1000);

  digitalWrite(muxPins[0], LOW);
  digitalWrite(muxPins[1], HIGH);
  digitalWrite(muxPins[2], LOW);
  Serial.println("col 3");
  delay(1000);

  digitalWrite(muxPins[0], HIGH);
  digitalWrite(muxPins[1], HIGH);
  digitalWrite(muxPins[2], LOW);
  Serial.println("col 4");
  delay(1000);
  */

  if (i == 0) {
        //case 0: // S = 000
          digitalWrite(muxPins[0], LOW);
          digitalWrite(muxPins[1], LOW);
          digitalWrite(muxPins[2], LOW);
          Serial.println("col 1");
      }
      else if (i == 1) {//  case 1: // S = 001
          digitalWrite(muxPins[0], HIGH);
          digitalWrite(muxPins[1], LOW);
          digitalWrite(muxPins[2], LOW);
          Serial.println("col 2");
      }
      else if (i == 2) {//  case 2: // S = 010
          digitalWrite(muxPins[0], LOW);
          digitalWrite(muxPins[1], HIGH);
          digitalWrite(muxPins[2], LOW);
          Serial.println("col 3");
      }
      else if (i == 3) {//  case 3: // S = 011
          digitalWrite(muxPins[0], HIGH);
          digitalWrite(muxPins[1], HIGH);
          digitalWrite(muxPins[2], LOW);
          Serial.println("col 4");
      }
      else if (i == 4) {//  case 4: // S = 100
          digitalWrite(muxPins[0], LOW);
          digitalWrite(muxPins[1], LOW);
          digitalWrite(muxPins[2], HIGH);
          Serial.println("col 5");
      }
      else if (i == 5) {//  case 5: // S = 101
          digitalWrite(muxPins[0], HIGH);
          digitalWrite(muxPins[1], LOW);
          digitalWrite(muxPins[2], HIGH);
          Serial.println("col 6");
      }
      else if (i == 6) {//  case 6: // S = 110
          digitalWrite(muxPins[0], LOW);
          digitalWrite(muxPins[1], HIGH);
          digitalWrite(muxPins[2], HIGH);
          Serial.println("col 7");
      }
      else if (i == 7) {//  case 7: // S = 111
          digitalWrite(muxPins[0], HIGH);
          digitalWrite(muxPins[1], HIGH);
          digitalWrite(muxPins[2], HIGH);
          Serial.println("col 8");
      }
      else {//  default:
          digitalWrite(muxPins[0], LOW);
          digitalWrite(muxPins[1], LOW);
          digitalWrite(muxPins[2], LOW);
          Serial.println("default");
      }

      delay(1000);

  
  }
}

void loop() {
  // put your main code here, to run repeatedly:



}
