int[] outPins = {2, 3, 4, 5, 6, 7, 8, 9};
int[] muxPins = {10, 11, 12};
String board;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for (int i = 0; i < 8; i++) {
    pinMode(outPins[i], OUTPUT);
  }
  pinMode(muxPins[0], OUTPUT);
  pinMode(muxPins[1], OUTPUT);
  pinMode(muxPins[2], OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(Serial.available()) {
    board = Serial.readString();
    if (board.length() != 64)
      continue;
    int index = 0;
    for (int i = 0; i < 8; i++) {
      switch (i) {
        case 0: // S = 000
          digitalWrite(muxPin[0], LOW);
          digitalWrite(muxPin[1], LOW);
          digitalWrite(muxPin[2], LOW);
          break;
        case 1: // S = 001
          digitalWrite(muxPin[0], HIGH);
          digitalWrite(muxPin[1], LOW);
          digitalWrite(muxPin[2], LOW);
          break;
        case 2: // S = 010
          digitalWrite(muxPin[0], LOW);
          digitalWrite(muxPin[1], HIGH);
          digitalWrite(muxPin[2], LOW);
          break;
        case 3: // S = 011
          digitalWrite(muxPin[0], HIGH);
          digitalWrite(muxPin[1], HIGH);
          digitalWrite(muxPin[2], LOW);
          break;
        case 4: // S = 100
          digitalWrite(muxPin[0], LOW);
          digitalWrite(muxPin[1], LOW);
          digitalWrite(muxPin[2], HIGH);
          break;
        case 5: // S = 101
          digitalWrite(muxPin[0], HIGH);
          digitalWrite(muxPin[1], LOW);
          digitalWrite(muxPin[2], HIGH);
          break;
        case 6: // S = 110
          digitalWrite(muxPin[0], LOW);
          digitalWrite(muxPin[1], HIGH);
          digitalWrite(muxPin[2], HIGH);
          break;
        case 7: // S = 111
          digitalWrite(muxPin[0], HIGH);
          digitalWrite(muxPin[1], HIGH);
          digitalWrite(muxPin[2], HIGH);
          break;
        default:
          digitalWrite(muxPin[0], LOW);
          digitalWrite(muxPin[1], LOW);
          digitalWrite(muxPin[2], LOW);
          break;
      }

      for (int j = 0; j < 8; j++) {
        if (board.charAt(index + j*8) == '1') {
          digitalWrite(outPins[j], HIGH);
        }
      }

      delay(250);

      for (int j = 0; j < 8; j++) {
        if (board.charAt(index + j*8) == '1') {
          digitalWrite(outPins[j], LOW);
        }
      }

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