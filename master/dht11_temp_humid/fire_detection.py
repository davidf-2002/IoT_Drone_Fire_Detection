import time
import random

# Simulation parameters
SIMULATION_INTERVAL = 1  #Simulate reading every 1 second
TEMPERATURE_THRESHOLD = 45 #degree celcius
CO_THRESHOLD = 500 #ppm

#Simulate sensor data
def get_simulated_dht11_data():
       #Simulate normal conditions with some random variation
       base_temp = 25 + random.uniform(-2, 2)
       base_humidity = 55 + random.uniform(-5, 5)
     
       #Simulate potential fire scenerio 
       if random.random() < 0.05:  #5% chance of fire 
             temp = base_temp + random.uniform(15, 30)
             humidity = base_humidity - random.uniform (10, 20)  #Humidity might decrease
       else:
             temp = base_temp
             humidity = base_humidity
       return temp, humidity

def get_simulated_mq7_data():
       #Simulate normal CO Levels
       base_co = 50 + random.uniform(-10, 10)

       #Simulate potential fire 
       if random.random() < 0.03:  # 3% chance of smoke
             co = base_co + random.uniform(400, 1000)
       else:
             co = base_co
       return co
          
 # Decision fusion
def check_for_fire(temperature, humidity, co_level):
  fire_detected = False
  reason = ""
  
  if temperature > TEMPERATURE_THRESHOLD and co_level > CO_THRESHOLD:
     fire_detected = True
     reason = "High temperature and CO"  
  elif temperature > TEMPERATURE_THRESHOLD:
       reason += "High temperature"
  elif co_level > CO_THRESHOLD:
       reason += "High CO Level"   
       
  return fire_detected, reason
       
# Main Loop (Simulation)    
try:
    while True:
       simulated_temp, simulated_humidity = get_simulated_dht11_data()
       simulated_co = get_simulated_mq7_data()
       
       fire_status, reason = check_for_fire(simulated_temp, simulated_humidity, simulated_co)
       print(f"Simulated Temperature:{simulated_temp:.2f}, Humidity: {simulated_humidity:.2f}, CO level: {simulated_co:.2f}")
         
       if fire_status:
           print(f"Fire Detected! Reason: {reason}")
       else:
           print("No fire")
                
       time.sleep(SIMULATION_INTERVAL)  
          
except KeyboardInterrupt:
           print("Simulation stopped")
