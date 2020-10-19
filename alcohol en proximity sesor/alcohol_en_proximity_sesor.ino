#define LED 2
#define BUTTON 3
//pins for proximity sensor
#define TRIG 12
#define ECHO 13
//pin for alcohol sensor
#define ALC A1

unsigned long time;

int WARMUP = 900; //set warmup to 15 minutes for warming up of the alcohol sensor.
int buttonState = 0; // variable for reading the pushbutton status
int debug = 0; //set debug flag.
float alc_min = 0.0;
float alc_max = 0.0;
float alc_treshold = 0.0;

void setup() {
  //Assinging inputs and outputs
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(ALC, INPUT);
  Serial.begin(9600);
  if (debug == 1) {
    Serial.println("DEBUG MODE");
  }
}


void calibrate() {
  Serial.println("callibarating");
  //to calibreate the sensor
  digitalWrite(LED, HIGH);//tun on led to let user know it is calibrating
  Serial.println("Setteling for 5 seconds.");
  delay(5000);//let sensor settle before reading.
  Serial.println("Reading alc sensor...");
  alc_min = readAlcohol(); //read value of sensor to set the minimum
  Serial.println("Alcohol minimum:");
  Serial.print(alc_min);
  digitalWrite(LED, LOW);
  delay(200);
  //blink led 3 times to led user know to hold 90% alc in front of the sensor and push the button
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  delay(200);
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  delay(200);
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  delay(200);
  Serial.println("Waiting on button press...");
  int z = 0;
  while(z==0) { //wait until button is pressed.
    buttonState = digitalRead(BUTTON); //set button state to variable
     if (buttonState == LOW) {
      Serial.println("button pressed");   
      digitalWrite(LED, HIGH);//tun on led to let user know it is calibrating.
      delay(3000);
      alc_max = readAlcohol(); //set value to max_alc.
      Serial.println("alcmax:");
      Serial.print(alc_max);
      delay(200);
      digitalWrite(LED, LOW);
      z=1;
    }
  }
  Serial.println("tresh formule:");
  Serial.println("max - min");
  Serial.println(alc_max);
  Serial.println(alc_min);
  Serial.println(alc_max-alc_min);
  Serial.println("*10");
  Serial.println((alc_max-alc_min)*10);
  Serial.println("/33");
  Serial.println(((alc_max-alc_min)*10)/30);
  alc_treshold = ((((alc_max - alc_min) * 10) / 33)+alc_min);
  
  Serial.println("treshhold: ");
  Serial.print(alc_treshold);
  //Blink led 2 times to let user know calibrating is finshed.
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  delay(200);
  digitalWrite(LED, HIGH);
  delay(200);
  digitalWrite(LED, LOW);
  
}

int readAlcohol()
{
  int val = 0;
  int val1;
  int val2;
  int val3;
  int val4;
  int val5;
  val1 = analogRead(ALC);
  delay(10);
  val2 = analogRead(ALC);
  delay(10);
  val3 = analogRead(ALC);
  delay(10);
  val4 = analogRead(ALC);
  delay(10);
  val5 = analogRead(ALC);
  val = (val1 + val2 + val3 + val4 + val5) / 5;
  return val;
}

int readDistance(){
  //to read distance senor.
  long duration, distanceCm;
 
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO,HIGH);
 
  // convert the time into a distance
  distanceCm = duration / 29.1 / 2 ;
    if (distanceCm <= 0)
  {
    Serial.println("Out of range");
  }
 return distanceCm;
}



void loop() {
  delay(100);
  time = millis() / 1000;
  if (debug == 1) {
    delay(500);
    int WARMUP_DEBUG = 1;
    if (time < WARMUP_DEBUG){
      //flash led until warmup is finished. (15 minutes)
      digitalWrite(LED, HIGH);
      delay(200);
      digitalWrite(LED, LOW);
      delay(200);
      Serial.println("Warming up, Time:");
      Serial.println(time);
     }else if (time == WARMUP_DEBUG){
      //keep led on for 2 seconds to let user know warmup is finished.
      digitalWrite(LED, HIGH);
      delay(2000);
      digitalWrite(LED, LOW);
      delay(200);
    } else {
    Serial.println("distance: ");
    Serial.println(readDistance());
    Serial.println("alcohol: ");
    Serial.println(readAlcohol());
    }       
  }else{ 
    delay(300); 
    if (time < WARMUP) { //warming up the alcohol sensor.
      //flash led until warmup is finished. (15 minutes)
      digitalWrite(LED, HIGH);
      delay(200);
      digitalWrite(LED, LOW);
      delay(200);
      Serial.println("Warming up, Time:");
      Serial.println(time);
      
    } else if (time == WARMUP) {
      //keep led on for 2 seconds to let user know warmup is finished.
      digitalWrite(LED, HIGH);
      delay(2000);
      digitalWrite(LED, LOW);
      delay(200);
    } else {
      if (alc_max == 0.0) {
        calibrate();
      }
      buttonState = digitalRead(BUTTON); //set button state to variable.
      if (buttonState == LOW) { //check if button is pressed.
        calibrate();
      }
      //to read distance senor.
      int dis = readDistance(); 
      Serial.println("distance: ");
      Serial.print(dis); 
      if(dis <= 10){
        Serial.println("disatance below 5");
        Serial.println("treshhold: ");
        Serial.print(alc_treshold);
        Serial.println("alcohol: ");
        Serial.print(readAlcohol());
  
        if (readAlcohol()>= alc_treshold){
          Serial.println("alcohol above treshold");
          digitalWrite(LED, HIGH);//turn on led to inform the user they may enter.
          delay(5000);
          digitalWrite(LED, LOW);
          delay(200);
      }
     }
    }
  }
}
