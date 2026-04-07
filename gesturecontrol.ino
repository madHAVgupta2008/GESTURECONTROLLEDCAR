char command;

int ENA = 5;
int ENB = 6;

int IN1 = 8;
int IN2 = 9;
int IN3 = 10;
int IN4 = 11;

int LED = 7;

int speedValue = 150;

void setup() {
  Serial.begin(9600);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  pinMode(LED, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();

    // SPEED
    if (command == '1') speedValue = 100;
    if (command == '2') speedValue = 180;
    if (command == '3') speedValue = 255;

    analogWrite(ENA, speedValue);
    analogWrite(ENB, speedValue);

    // MOVEMENT
    if (command == 'F') {
      digitalWrite(LED, LOW);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    }

    else if (command == 'S') {
      digitalWrite(LED, HIGH);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }

    else if (command == 'L') {
      digitalWrite(LED, LOW);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    }

    else if (command == 'R') {
      digitalWrite(LED, LOW);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
    }
  }
}