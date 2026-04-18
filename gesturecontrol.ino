#include <SoftwareSerial.h>

SoftwareSerial BT(7, 8); // RX, TX

char command;

int ENA = 9;
int ENB = 10;

int IN1 = 3;
int IN2 = 2;
int IN3 = 4;
int IN4 = 5;

int LEDR = 12;
int LEDL = 13;
int buzzer = 11;

int speedValue = 150;

void setup() {
  Serial.begin(9600);
  BT.begin(9600);   // Bluetooth baud rate

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  pinMode(LEDL, OUTPUT);
  pinMode(LEDR,OUTPUT);
}

void loop() {
  if (BT.available()) {
    command = BT.read();

    // SPEED CONTROL
    if (command == '1') speedValue = 100;
    if (command == '2') speedValue = 180;
    if (command == '3') speedValue = 255;

    analogWrite(ENA, speedValue);
    analogWrite(ENB, speedValue);

    // BACKWARD
    if (command == 'B') {
      digitalWrite(LEDR, LOW);
      digitalWrite(LEDL,LOW);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      digitalWrite(buzzer,HIGH);
    }

    // STOP
    else if (command == 'S') {
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDL,HIGH);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }

    //FORWARD
    else if (command == 'F') {
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDL,HIGH);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
    }


    // LEFT
    else if (command == 'L') {
      digitalWrite(LEDR, HIGH);
      digitalWrite(LEDL,LOW);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      digitalWrite(buzzer,HIGH);
      delay(10);
      digitalWrite(buzzer,LOW);
    }

    // RIGHT
    else if (command == 'R') {
      digitalWrite(LEDL, HIGH);
      digitalWrite(LEDR,LOW);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      digitalWrite(buzzer,HIGH);
      delay(10);
      digitalWrite(buzzer,LOW);
    }
  }
}