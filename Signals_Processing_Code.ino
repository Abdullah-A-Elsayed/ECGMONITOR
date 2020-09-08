/*
  this code take two signals "ECG & PPG" from two different sensors "AD8232 & Pulse sensor "
  and do some processing on them to get Heart_Rate,Pulse transient time,SPO2 and from that
  use an equation to get Blood Presure ((a*PTT)+(b*HR)+c).


*/
#include <LiquidCrystal.h>
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
#include <Filters.h>

float Frequency_H = 2;
float Frequency_L = 50;
int filtered1 = 0;
int filtered2 = 0;

int i = 0 , j = 0, m = 1, h = 0;
int ecgvalue = 0 , peak1 = 0, ppgvalue = 0 , peak2 = 0;
long t = 0 , duration = 0, timeOf_peakecg1 = 0, timeOf_peakecg2 = 0 , timeOf_peakppg1 = 0, timeOf_peakppg2 = 0 ;
bool x = false, y = false;

float factor_ecg, factor_ppg;

float  a1 = 46.0010, b1 = 52.4258, c1 = 28.57625 , a2 = -11.5216, b2 = 16.8795, c2 = 59.8844 , bp_sys = 0, bp_dis = 0, bpm = 0, ptt = 0 ;
float avrag = 0, p1 = 0, p2 = 0, p3 = 0;

int ecgThreshold = 600;
int ppgThreshold = 450;

float R = 0.0;
int spo2 = 0;


FilterOnePole filterOneHighpass( HIGHPASS, Frequency_H );
FilterOnePole filterOneLowpass( LOWPASS, Frequency_L );

void setup() {
  Serial.begin(9600);
  pinMode(5, INPUT); // Setup for leads off detection LO +
  pinMode(6, INPUT); // Setup for leads off detection LO -
  lcd.begin(16, 2);

}
void loop() {
  if ((digitalRead(5) == 1) || (digitalRead(6) == 1)) {
    Serial.println('!');
  }
  else {

    ecgvalue = analogRead(A0);
    ppgvalue = analogRead(A5);
    filterOneHighpass.input(ecgvalue);
    filtered1 = filterOneHighpass.output();
    filterOneLowpass.input(filtered1);
    filtered2 = (((filterOneLowpass.output()) + 100)) * 4;
    // Serial.println(filtered2);

    //Start  code of the ECG signal
    if (filtered2 >= ecgThreshold) {
      peak1 = filtered2;
      for (;;) {
        ecgvalue = analogRead(A0);
        filterOneHighpass.input(ecgvalue);
        filtered1 = filterOneHighpass.output();
        filterOneLowpass.input(filtered1);
        filtered2 = (((filterOneLowpass.output()) + 100)) * 4;
        if (filtered2 >= peak1) {
          peak1 = filtered2;
          timeOf_peakecg1 = millis();
        }
        if (filtered2 < ecgThreshold) {
          x = true;
          factor_ecg = 60000 / (timeOf_peakecg1 - timeOf_peakecg2);
          timeOf_peakecg2 = timeOf_peakecg1;
          i++;
          break;
        }
      }
    }
    //End  code of the ECG signal

    //Start  code of the PPG signal

    if (ppgvalue >= ppgThreshold) {
      peak2 = ppgvalue;
      for (;;) {
        ppgvalue = analogRead(A5);
        if (ppgvalue >= peak2) {
          peak2 = ppgvalue;
          timeOf_peakppg1 = millis();
        }
        if (ppgvalue < ppgThreshold) {
          y = true;
          j++;
          factor_ppg = 60000 / (timeOf_peakppg1 - timeOf_peakppg2);
          timeOf_peakppg2 = timeOf_peakppg1;
          break;
        }
      }
    }
    //End  code of the PPG signal


    if (x && y) {
      ptt = timeOf_peakecg1 - timeOf_peakppg1 ;
      if (ptt < 0) {
        ptt = -ptt;
      }

      if (((factor_ecg - factor_ppg) >= 0 && (factor_ecg - factor_ppg) < 5) || ((factor_ppg - factor_ecg) >= 0 && (factor_ppg - factor_ecg) < 5)) {
        //      Serial.print(" the ptt is \t ");
        //      Serial.println(ptt);
        //      Serial.print("the heart rate is from ECG Signal \t ");
        //      Serial.println(factor_ecg);
        //      Serial.print("the heart rate is from PPG Signal \t ");
        //      Serial.println(factor_ppg);
        p1 = ptt / 1000.0;
        p2 = factor_ppg / 60.0;
        bp_sys = a1 * p1 + p2 * b1 + c1;
        bp_dis = a2 * p1 + p2 * b2 + c2;
        R = (750.0-peak2)/ 750.0;
        spo2 = 100.5 - (4.15 * R) - (17.69 * R * R);
        //      Serial.print("the Blood pressure is $$$$$$$$$$$$$$$$$$$$$$$$$$ \t ");
        //      Serial.print(bp_sys);
        //      Serial.print(" / ");
        //      Serial.println(bp_dis);
        if(bp_sys>90&&bp_dis<90&&bp_dis>50&&factor_ppg>45){
        String data = String(bp_sys) + "/" + String(bp_dis) + "," + String(int(factor_ppg)) + "," + String(spo2) + "%" + "," + String(ptt) + "ms";
        Serial.println(data);
        //lcd display code:
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("BP:");
        lcd.print(bp_sys);
        lcd.print(" / ");
        lcd.print(bp_dis);
        lcd.setCursor(0, 1);
        lcd.print("HR:");
        lcd.print(int(factor_ppg));
        lcd.print(" & ");
        lcd.print("SPO2:");
        lcd.print(spo2);
        lcd.print("%");
        }

      }
      x = false;
      y = false;
    }
  }

}
