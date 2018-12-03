int outPins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
int muxPins[3] = {12, 11, 10};
String board = "0110000001100000011000000110000011000000110000001000000010000000";//"1111111111111111111111111111111111111111111111111111111111111111";


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i < 8; i++) {
    pinMode(outPins[i], OUTPUT);
    digitalWrite(outPins[i], HIGH);
  }
  pinMode(muxPins[0], OUTPUT);
  pinMode(muxPins[1], OUTPUT);
  pinMode(muxPins[2], OUTPUT);
  pinMode(muxPins[0], LOW);
  pinMode(muxPins[1], LOW);
  pinMode(muxPins[2], LOW);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(1) {//Serial.available()) {
    //board = Serial.readString();
    Serial.println(board);
    Serial.println(board.length());
    if (board.length() != 64)
      continue;
    int index = 0;
    for (int i = 0; i < 8; i++) {

      for (int w = 0; w < 8; w++) {
        digitalWrite(outPins[w], HIGH);
      }
      for (int w = 0; w < 3; w++) {
        digitalWrite(muxPins[w], LOW);
      }

      
      Serial.print("i = ");
      Serial.println(i);
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
      

      for (int j = 0; j < 8; j++) {
        if (board.charAt(j + i*8) == '1') {
          digitalWrite(outPins[j], LOW);
          Serial.print("turning on pin ");
          Serial.print(j+1);
          Serial.print(", ");
          Serial.println(i+1);
          delay(500);
          digitalWrite(outPins[j], HIGH);
        }
      }

      //delay(500);

      //for (int j = 0; j < 8; j++) {
        //if (board.charAt(i + j*8) == '1') {
          //digitalWrite(outPins[j], HIGH);
        //}
      //}

      index++;
    }
  }

}


//if we want to acces via row, one pin at a time
/*if (board.charAt(index++) == '1') {
  digitalWrite(outPins[j], HIGH);
  delay(250);
  digitalWrite(outPins[j], LOW);
}*/
