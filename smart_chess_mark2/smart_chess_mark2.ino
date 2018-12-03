int outPins[8] = {2, 3, 4, 5, 6, 7, 8, 9};
int muxPins[3] = {12, 11, 10};

String board;// = "0010000001100000011000000110000011000000110000001100000011000000";


void set_mux(int i){
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
      return;
}

void setup() {
  // put your setup code here, to run once:
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
}
//00000011 00000011 00000011 00000111 00000011



void loop() {
  // put your main code here, to run repeatedly:

  
  if (Serial.available()) {

    board = Serial.readString();

    Serial.println(board);
    Serial.println(board.length());
    for(int i = 0; i<8; i++){
      set_mux(i);
      for(int j = 0; j<8; j++){
        Serial.println("at j  = ");
        Serial.println(board[j+(8*i)]);
        if(board[j+(8*i)] == '1'){
          Serial.println("in if");
          pinMode(outPins[j], LOW);
          pinMode(outPins[j], HIGH);
        }
        else{
          pinMode(outPins[j], HIGH);
        }
      }

      delay(1000);
      for(int i = 0; i < 8; i++){
        digitalWrite(outPins[i], HIGH);
      }
    }
  }
}