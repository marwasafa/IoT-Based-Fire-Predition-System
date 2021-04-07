import http.client
import urllib.request, urllib.parse, urllib.error
import time
import smbus
import time
from datetime import datetime
import pandas as pd
import numpy as np
from pandas.core import algorithms
from scipy.spatial import distance
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

key = "LP1T78H3I4WXETW4"  # Put your API Key here

def detector():
    
    fire = 0
    fireStatus = "Green"
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        #temp = 395 #int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        #humidity = 45
        # Get I2C bus
        bus = smbus.SMBus(1)

        # BME280 address, 0x76(118)
        # Read data back from 0x88(136), 24 bytes
        b1 = bus.read_i2c_block_data(0x76, 0x88, 24)

        # Convert the data
        # Temp coefficients
        dig_T1 = b1[1] * 256 + b1[0]
        dig_T2 = b1[3] * 256 + b1[2]
        if dig_T2 > 32767 :
            dig_T2 -= 65536
        dig_T3 = b1[5] * 256 + b1[4]
        if dig_T3 > 32767 :
            dig_T3 -= 65536

        # Pressure coefficients
        dig_P1 = b1[7] * 256 + b1[6]
        dig_P2 = b1[9] * 256 + b1[8]
        if dig_P2 > 32767 :
            dig_P2 -= 65536
        dig_P3 = b1[11] * 256 + b1[10]
        if dig_P3 > 32767 :
            dig_P3 -= 65536
        dig_P4 = b1[13] * 256 + b1[12]
        if dig_P4 > 32767 :
            dig_P4 -= 65536
        dig_P5 = b1[15] * 256 + b1[14]
        if dig_P5 > 32767 :
            dig_P5 -= 65536
        dig_P6 = b1[17] * 256 + b1[16]
        if dig_P6 > 32767 :
            dig_P6 -= 65536
        dig_P7 = b1[19] * 256 + b1[18]
        if dig_P7 > 32767 :
            dig_P7 -= 65536
        dig_P8 = b1[21] * 256 + b1[20]
        if dig_P8 > 32767 :
            dig_P8 -= 65536
        dig_P9 = b1[23] * 256 + b1[22]
        if dig_P9 > 32767 :
            dig_P9 -= 65536

        # BME280 address, 0x76(118)
        # Read data back from 0xA1(161), 1 byte
        dig_H1 = bus.read_byte_data(0x76, 0xA1)

        # BME280 address, 0x76(118)
        # Read data back from 0xE1(225), 7 bytes
        b1 = bus.read_i2c_block_data(0x76, 0xE1, 7)

        # Convert the data
        # Humidity coefficients
        dig_H2 = b1[1] * 256 + b1[0]
        if dig_H2 > 32767 :
            dig_H2 -= 65536
        dig_H3 = (b1[2] &  0xFF)
        dig_H4 = (b1[3] * 16) + (b1[4] & 0xF)
        if dig_H4 > 32767 :
            dig_H4 -= 65536
        dig_H5 = (b1[4] / 16) + (b1[5] * 16)
        if dig_H5 > 32767 :
            dig_H5 -= 65536
        dig_H6 = b1[6]
        if dig_H6 > 127 :
            dig_H6 -= 256

        # BME280 address, 0x76(118)
        # Select control humidity register, 0xF2(242)
        #		0x01(01)	Humidity Oversampling = 1
        bus.write_byte_data(0x76, 0xF2, 0x01)
        # BME280 address, 0x76(118)
        # Select Control measurement register, 0xF4(244)
        #		0x27(39)	Pressure and Temperature Oversampling rate = 1
        #					Normal mode
        bus.write_byte_data(0x76, 0xF4, 0x27)
        # BME280 address, 0x76(118)
        # Select Configuration register, 0xF5(245)
        #		0xA0(00)	Stand_by time = 1000 ms
        bus.write_byte_data(0x76, 0xF5, 0xA0)

        time.sleep(0.5)

        # BME280 address, 0x76(118)
        # Read data back from 0xF7(247), 8 bytes
        # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
        # Temperature xLSB, Humidity MSB, Humidity LSB
        data = bus.read_i2c_block_data(0x76, 0xF7, 8)

        # Convert pressure and temperature data to 19-bits
        adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
        adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16

        # Convert the humidity data
        adc_h = data[6] * 256 + data[7]

        # Temperature offset calculations
        var1 = ((adc_t) / 16384.0 - (dig_T1) / 1024.0) * (dig_T2)
        var2 = (((adc_t) / 131072.0 - (dig_T1) / 8192.0) * ((adc_t)/131072.0 - (dig_T1)/8192.0)) * (dig_T3)
        t_fine = (var1 + var2)
        cTemp = (var1 + var2) / 5120.0
        fTemp = cTemp * 1.8 + 32

        # Pressure offset calculations
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (dig_P6) / 32768.0
        var2 = var2 + var1 * (dig_P5) * 2.0
        var2 = (var2 / 4.0) + ((dig_P4) * 65536.0)
        var1 = ((dig_P3) * var1 * var1 / 524288.0 + ( dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (dig_P1)
        p = 1048576.0 - adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (dig_P9) * p * p / 2147483648.0
        var2 = p * (dig_P8) / 32768.0
        pressure = (p + (var1 + var2 + (dig_P7)) / 16.0) / 100

        # Humidity offset calculations
        var_H = ((t_fine) - 76800.0)
        var_H = (adc_h - (dig_H4 * 64.0 + dig_H5 / 16384.0 * var_H)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * var_H * (1.0 + dig_H3 / 67108864.0 * var_H)))
        humidity = var_H * (1.0 -  dig_H1 * var_H / 524288.0)
        if humidity > 100.0 :
            humidity = 100.0
        elif humidity < 0.0 :
            humidity = 0.0

        #time of day
        now = datetime.now()

        c_time = now.strftime("%H:%M")
        current_time = float(c_time.replace(":","."))
        # with open('forestfires_dataset.csv') as readfile:
        #     fire_listings = pd.read_csv(readfile.read())
        #     #df = pd.read_csv(readfile.read())

        fire_listings = pd.read_csv('forestfires_dataset.csv')

        #randomizing the rows
        fire_listings = fire_listings.sample(frac=1,random_state=0)
        #split into training and test data sets
        train_df = fire_listings.copy().iloc[0:76]
        test_df = fire_listings.copy().iloc[76:]
        train_features = train_df[['temp', 'humidity', 'time_of_day']]
        train_target = train_df[['fire_prob']]
        test_features = test_df[['temp', 'humidity', 'time_of_day']]
        test_target = test_df[['fire_prob']]

        #instantiating an empty knn model
        knn = KNeighborsRegressor(algorithm='brute')
        knn.fit(train_features, train_target) #fitting the model to the data
        #making predictions about the test data colums
        predictions = knn.predict(test_features)
        # print(predictions)
        #calculating the mse using scikit-learn
        mse = mean_squared_error(test_target, predictions)
        rmse = mse ** (1/2)
        #print(rmse)

        firePredictionArray = knn.predict([[cTemp, humidity, current_time]])
        fire = round(firePredictionArray[0][0], 2)
        #print("Current Time = ", current_time)

        # preferred relative humidity for burning varies from 30 to 55 percent
        #ignition temperature is 300 degree Celsius
        if fire < 0.25:
            fireStatus = "Green"
        elif fire > 0.25 and fire < 0.75: 
            fireStatus = "Orange"
        else :
            fireStatus = "Red"

        params = urllib.parse.urlencode({'field1': cTemp, 'field2': humidity, 'field3': current_time, 'field4': fire, 'key':key }) # channel field info for thingspeak
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80") # defining thingspeak connection

        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse() 
            
            # Output data to screen
            print("Temperature in Celsius : %.2f C" %cTemp)
            print("Temperature in Fahrenheit : %.2f F" %fTemp)
            print("Pressure : %.2f hPa " %pressure)
            print("Current Time : %.2f" %current_time)
            print("Fire Probability is: ", fire)
            print("Fire Status: ", fireStatus)
            print("Response Status: ", response.status, response.reason)
            data = response.read()
            conn.close()
            
        except:
            print("connection failed") 
        break
if __name__ == "__main__":
        while True:
                detector()
                time.sleep(5) # loops every 5 secs

