#include "FastLED.h"
#include "lib8tion.h"

#define NUM_LEDS 107
CRGBArray<NUM_LEDS> leds;

// inputs
#define DOOR_SENSOR_PIN 2
#define MICRO_SENSOR_PIN 3
#define IR_SENSOR_PIN 4
#define PROX_SENSOR_PIN 5

// outputs
#define LED_PIN 8
#define PRIVACYFILM_PIN 6
#define OCCUPIED_PIN 7



char dataString[50] = {0};
uint16_t oldtime = millis();
uint16_t ntime = 0;

volatile bool triggerDoor = false;
volatile bool triggerMicro = false;
volatile bool triggerIR = false;
volatile bool triggerProximity = false;
bool triggerPulse = false;

int doorCounter = 0;
int microCounter = 0;
int irCounter = 0;
int proximityCounter = 0;
int state = 0;
int loopCounter = 0;

bool door = false;
bool micro = false;
bool ir = false;
bool proximity = false;


#define LED_IDLE_LEVEL 150


#define STATE_1_TIME 5
#define STATE_2_TIME 10
#define STATE_3_TIME 5
#define STATE_4_TIME 10

// state machine for heart beat pulse
// 0 = idle
// 1 = first beat
// 2 = fade...
// 3 = second beat
// 4 = fade...

void setup()
{
  Serial.begin(115200);              //Starting serial communication

// booth is likely GRB order
  FastLED.addLeds<WS2813, LED_PIN, GRB>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(255);

  fill_solid(leds,leds.size(), CRGB(100,100,100)); // on by default -- default brightness is 100; pulse up to 200 for beat
  FastLED.show();

  pinMode(DOOR_SENSOR_PIN, INPUT);
  pinMode(MICRO_SENSOR_PIN, INPUT);
  pinMode(IR_SENSOR_PIN, INPUT);
  pinMode(PROX_SENSOR_PIN, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(DOOR_SENSOR_PIN), triggerDoorSensor, FALLING);
  attachInterrupt(digitalPinToInterrupt(MICRO_SENSOR_PIN), triggerMicroSensor, RISING);
  attachInterrupt(digitalPinToInterrupt(IR_SENSOR_PIN), triggerIrSensor, FALLING);
  attachInterrupt(digitalPinToInterrupt(PROX_SENSOR_PIN), triggerProxSensor, RISING);
}


void triggerDoorSensor() {
  if (doorCounter <= 0)
    triggerDoor = true;
}

void triggerMicroSensor() {
  if (microCounter <= 0)
    triggerMicro = true;
}

void triggerIrSensor() {
  if (irCounter <= 0)
    triggerIR = true;
}

void triggerProxSensor() {
  if (proximityCounter <= 0)
    triggerProximity = true;
}

void loop() {
  uint16_t t = millis();
  uint16_t dt = t - oldtime;
  oldtime = t;

  delay(20);

  // process all the cooldown timers
  // after cooldown time expires, use polling to check if active state has ended
  if (doorCounter > 0)
  {
    doorCounter -= dt;
  } else if (door && digitalRead(DOOR_SENSOR_PIN) == HIGH)   // this is no longer active
  {
    door = false;
    Serial.println("door_off");
  } 

  if (microCounter > 0)
  {
    microCounter -= dt;
  } else if (micro && digitalRead(MICRO_SENSOR_PIN) == LOW)
  {
    micro = false;
    Serial.println("micro_off");
  }
  
  if (irCounter > 0)
  {
    irCounter -= dt;
  } else if (ir && digitalRead(IR_SENSOR_PIN) == HIGH)
  {
    ir = false;
    Serial.println("ir_off");
  }
  
  if (proximityCounter > 0)
  {
    proximityCounter -= dt;
  } else if (proximity && digitalRead(PROX_SENSOR_PIN) == LOW)
  {
    proximity = false;
    Serial.println("proximity_off");
  }


  // process all interrupts to see if any of them have triggered
  // if one triggers, set up 5 second cool down time before it can trigger again
  if (triggerDoor)
  {
    triggerDoor = false;
    door = true;
    doorCounter = 5000;
    Serial.println("door_on");    
  }
  if (triggerMicro)
  {
    triggerMicro = false;
    micro = true;
    microCounter = 5000;
    Serial.println("micro_on");    
  }
  if (triggerIR)
  {
    triggerIR = false;
    ir = true;
    irCounter = 5000;
    Serial.println("ir_on");    
  }
  if (triggerProximity)
  {
    triggerProximity = false;
    proximity = true;
    proximityCounter = 5000;
    Serial.println("proximity_on");    
  }

  // now handle state machine for pulsing the light
  if (state == 0)
  {
    if (triggerPulse)   // trigger heart beat pulse
    {
      triggerPulse = false;
      loopCounter = STATE_1_TIME;
      state = 1;
    }
  } else if (state == 1)
  {
    int b = LED_IDLE_LEVEL + (20 * (5-loopCounter));
    fill_solid(leds,leds.size(), CRGB(b,b,b)); 
    FastLED.show();
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 2;
      loopCounter  = STATE_2_TIME;
    }
  } else if (state == 2)
  {
    int b = LED_IDLE_LEVEL + (10 * loopCounter);
    fill_solid(leds,leds.size(), CRGB(b,b,b)); 
    FastLED.show();
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 3;
      loopCounter  = STATE_3_TIME;
    }
  } else if (state == 3)
  {
    int b = LED_IDLE_LEVEL + (20 * (5-loopCounter));
    fill_solid(leds,leds.size(), CRGB(b,b,b)); 
    FastLED.show();
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 4;
      loopCounter  = STATE_4_TIME;
    }
  } else if (state == 4)
  {
    int b = LED_IDLE_LEVEL + (10 * loopCounter);
    fill_solid(leds,leds.size(), CRGB(b,b,b)); 
    FastLED.show();
    loopCounter--;
    if (loopCounter == 0)
    {
      state = 0;
    }
  }  
    
  // now handle incoming messages via serial 
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    if (data == "beat")
    {
      triggerPulse = true;
    }
  }
}
