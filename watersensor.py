from machine import ADC, Pin, I2C
import ssd1306
import time

# This is where I decleared the constants for the turbitity sensor
turbidity = ADC(26)  # ADC Pin for turbidity sensor
conversion_factor = 3.3 / 65535  # Conversion factor for 16-bit ADC
low_turbidity = 500     # Calibrated raw value for clean water
high_turbidity = 45000  # Calibrated raw value for highly turbid water

# Constants for TDS Sensor
tds = ADC(Pin(27)) 
VREF = 3.3       
SLOPE = 0.5     
INTERCEPT = 10  

# I2C setup for OLED
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)  # Clear the OLED screen
oled.show()

oled.text('Initializing...', 0, 0)
oled.show()
time.sleep(2)

# Function to calculate TDS value
# ChatGPT assisted with writing this section of the code
def calculate_tds(sensor_value):
    # Adjusted TDS calculation formula based on sensor value
    return max(0, SLOPE * sensor_value + INTERCEPT)  # Ensure TDS is not negative
# Function to calibrate and calculate turbidity percentage
def calculate_turbidity(raw_value):
    # Linearly map the raw value to a percentage (0 to 100)
    if raw_value < low_turbidity:
        return 0  # Return 0% for clean water
    elif raw_value > high_turbidity:
        return 100  # Return 100% for very turbid water
    else:
        # Map the raw value linearly to a percentage between 0 and 100
        return int(((raw_value - low_turbidity) * 100) / (high_turbidity - low_turbidity))

# Main loop
while True:
    # Read turbidity sensor
    raw_turbidity = turbidity.read_u16()
    volts_turbidity = raw_turbidity * conversion_factor
    percentage_turbidity = calculate_turbidity(raw_turbidity)

    # Read TDS sensor
    raw_tds = tds.read_u16()
    volts_tds = raw_tds * conversion_factor  # Convert to voltage
    tds_value = calculate_tds(raw_tds)  # Calculate TDS value in ppm

    # Display values on the OLED screen
    oled.fill(0)  # Clear the screen
    oled.text('Turbidity:', 0, 0)
    oled.text('Raw: {}'.format(raw_turbidity), 0, 10)
    oled.text('Voltage: {:.2f}V'.format(volts_turbidity), 0, 20)
    oled.text('Turbidity: {}%'.format(percentage_turbidity), 0, 30)

    oled.text('TDS Value: {:.0f} ppm'.format(tds_value), 0, 40)
    oled.text('TDS Voltage: {:.2f}V'.format(volts_tds), 0, 50)
    
    oled.show()  # Update the OLED display with the new data
    # Debugging output
    # ChatGPT Assisted with this section of the code
  print('Turbidity - Raw: {}, Voltage: {:.2f}V, Percentage: {}%'.format(
        raw_turbidity, volts_turbidity, percentage_turbidity))
  print('TDS - Raw: {}, Voltage: {:.2f}V, TDS Value: {:.0f} ppm'.format(
        raw_tds, volts_tds, tds_value))
    
    time.sleep(1)  # Wait for a second before the next reading
