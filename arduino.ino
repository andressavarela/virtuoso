int lamp = 12;
bool lampState;

void setup()
{
  pinMode(lamp, OUTPUT);
  digitalWrite(lamp, lampState);
  Serial.begin(9600);
}

void loop()
{
  char command = Serial.read();
  if (command == 'L' && lampState == HIGH)
  {
    digitalWrite(lamp, LOW);
    lampState = LOW;
  }
  else if (command == 'H' && lampState == LOW)
  {
    digitalWrite(lamp, HIGH);
    lampState = HIGH;
  }
}
