 // inputs
#define DOOR_SENSOR_PIN 2
#define MICRO_SENSOR_PIN 3
#define IR_SENSOR_PIN 4
#define PROX_SENSOR_PIN 5

// outputs
#define PRIVACYFILM_PIN 6
#define LIGHT_PIN 9
#define OCCUPIED_PIN 10

#define MAX_LIGHT 255
#define MIN_LIGHT 0
#define DIM_LIGHT 1

#define MAX_OCCUPIED 255

int state = 0;
int loopCounter = 0;
bool triggerPulse = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(PRIVACYFILM_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(OCCUPIED_PIN, OUTPUT);

  pinMode(DOOR_SENSOR_PIN, INPUT_PULLUP);
  pinMode(MICRO_SENSOR_PIN, INPUT);
  pinMode(IR_SENSOR_PIN, INPUT_PULLUP);
  pinMode(PROX_SENSOR_PIN, INPUT);

  Serial.begin(115200);


  //digitalWrite(LIGHT_PIN, HIGH);
  //digitalWrite(PRIVACYFILM_PIN, HIGH);

  test_beat();
    analogWrite(LIGHT_PIN, 1);
}

void loop() {
  // put your main code here, to run repeatedly:

  //test_light();
/*
  digitalWrite(LIGHT_PIN, HIGH);
  digitalWrite(PRIVACYFILM_PIN, HIGH);


  delay(2000);

  
  for (int i = MAX_LIGHT; i >= DIM_LIGHT; i-=3)
  {
    analogWrite(LIGHT_PIN, i);
    delay(20);
  }
  digitalWrite(PRIVACYFILM_PIN, LOW);

  delay(1000);

  test_occupied();
  delay(50);
  test_occupied();
  delay(50);
  test_occupied();
  delay(50);

*/


  /*
    Serial.print("DOOR_SENSOR_PIN:");
    Serial.println(digitalRead(DOOR_SENSOR_PIN));
    Serial.print("MICRO_SENSOR_PIN:");
    Serial.println(digitalRead(MICRO_SENSOR_PIN));
    Serial.print("IR_SENSOR_PIN:");
    Serial.println(digitalRead(IR_SENSOR_PIN));
    Serial.print("PROX_SENSOR_PIN:");
    Serial.println(digitalRead(PROX_SENSOR_PIN));
  `  Serial.println("");

    delay(100);
    */
  

  //digitalWrite(LIGHT_PIN, !digitalRead(IR_SENSOR_PIN)  );

  //digitalWrite(OCCUPIED_PIN, digitalRead(PROX_SENSOR_PIN));
  

  //update_light();
  


}

void test_beat()
{
  static uint16_t last = millis();

  if (millis() - last >= 5000);
  {
    triggerPulse = true;
    last = millis();
  }

  update_light();
}

void update_light()
{
  // now handle state machine for pulsing the light
  if (state == 0)
  {
    if (triggerPulse)   // trigger heart beat pulse
    {
      triggerPulse = false;
      loopCounter = 5;
      state = 1;
    }
  } else if (state == 1)
  {
    int b = 100 + (20 * (5 - loopCounter));
    analogWrite(LIGHT_PIN, b);
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 2;
      loopCounter  = 10;
    }
  } else if (state == 2)
  {
    int b = 100 + (10 * loopCounter);
    analogWrite(LIGHT_PIN, b);
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 3;
      loopCounter  = 5;
    }
  } else if (state == 3)
  {
    int b = 100 + (20 * (5 - loopCounter));
    analogWrite(LIGHT_PIN, b);
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 4;
      loopCounter  = 10;
    }
  } else if (state == 4)
  {
    int b = 100 + (10 * loopCounter);
    analogWrite(LIGHT_PIN, b);
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 0;
    }
  }
}


void test_pf()
{
  digitalWrite(PRIVACYFILM_PIN, HIGH);
  delay(1000);
  digitalWrite(PRIVACYFILM_PIN, LOW);
  delay(1000);
}

void test_light()
{

  for (int i = 0; i <= MAX_LIGHT; i++)
  {
    analogWrite(LIGHT_PIN, i);
    //Serial.println(i);
    delay(15);
  }

  for (int i = MAX_LIGHT; i >= 0 ; i--)
  {
    analogWrite(LIGHT_PIN, i);
    //Serial.println(i);
    delay(15);
  }
}

void test_occupied()
{

  for (int i = 0; i <= MAX_OCCUPIED; i++)
  {
    analogWrite(OCCUPIED_PIN, i);
    //Serial.println(i);
    delay(5);
  }

  for (int i = MAX_OCCUPIED; i >= 0 ; i--)
  {
    analogWrite(OCCUPIED_PIN, i);
    //Serial.println(i);
    delay(5);
  }
}
