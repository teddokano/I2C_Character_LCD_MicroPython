# I2C_Character_LCD

## What is this?
I²C character LCD class drivers for [AE-AQM0802](https://akizukidenshi.com/catalog/g/g106795/), [ACM2004D-FLW-FBW-IIC](https://akizukidenshi.com/catalog/g/g117381/) and [ACM1602NI-FLW-FBW-M01](https://akizukidenshi.com/catalog/g/g105693/)   

The code runs on [MicroPython](https://micropython.org), operation is checked on [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), [MIMXRT1050-EVKB](https://www.nxp.com/design/design-center/development-boards-and-designs/MIMXRT1050-EVK) and [MIMXRT1010-EVK](https://www.nxp.com/design/design-center/development-boards-and-designs/i-mx-evaluation-and-development-boards/i-mx-rt1010-evaluation-kit:MIMXRT1010-EVK).  

A [video](https://youtube.com/shorts/FqGNWmqnXug) is available to show how are those can be looked like.   
[![](https://github.com/teddokano/additional_files/blob/main/I2C_Character_LCD/video.png)](https://youtube.com/shorts/FqGNWmqnXug)


## How can it be used?

Refer to sample code. Sample code available for each MCUs and LCDs.  
Before trying the example code, upload `I2C_Character_LCD.py` into flash storage area of target microcontroller board. 
![](https://github.com/teddokano/I2C_Character_LCD_MicroPython/blob/main/examples/RaspberryPiPico/README_before_trying_sample_code.png)

Next code shows a sample of using ACM2004: 20 characters x 4 lines LCD.  
The sample is available as `example/RaspberryPiPico/ACM2004.py`.  

```python
from machine	import	I2C, Pin
from time		import	sleep
from I2C_Character_LCD	import	ACM2004

i2c	= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )
lcd	= ACM2004( i2c )

while True:
	lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890!@#$%^&" )
	sleep( 1 )

	lcd.print( [ "ABCDEFGHIJKLMNOPQRST", "abcdefghijklmnopqrst", "01234567890123456789", "!@#$%^&*()!@#$%^&*()" ] )
	sleep( 1 )
	
	lcd.clear()
	sleep( 1 )
```

### functions
##### `print()`
`print()` function is available to print the characters.   
The `print()` can take two types of argument.  
* If an string is given as the argument, the text wraps and is displayed on the next line.   
* If a list of strings is given, each strings will be shown in lines. If the item in the list is `None`, the line will be kept as it is.   

##### `clear()`
Another function: `clear()` is available to clear the screen.  





## Connecting hardware

### MCU  
Signal|Raspberry Pi Pico|MIMXRT1050|MIMXRT1010
---|---|---|---
SDA|Pin1(GP0)|A4/ADC4/SDA|D14/I2C_SDA
SCL|Pin2(GP1)|A5/ADC5/SCL|D15/I2C_SCL

### LCD
AE-AQM0802
Pin#|Name
---|---
1|		VDD(3.3V)
2|		nRESET
3|		I2C_SCL
4|		I2C_SDA
5|		GND

ACM2004D-FLW-FBW-IIC
Pin#|Name
---|---
1|		VSS(GND)
2|		VDD(5V)
3|		V0(NC)
4|		I2C_SDA
5|		I2C_SCL
6|		Backlight+(5V)
7|		Backlight-(0V)
	
ACM1602NI-FLW-FBW-M01
Pin#|Name
---|---
1|		VSS(GND)
2|		VDD(3.3V)
3|		V0(contrast adj)
4|		I2C_SCL
5|		I2C_SDA
6|		Backlight+(3.3V)
7|		Backlight-(0V)

## scenes
![](https://github.com/teddokano/additional_files/blob/main/I2C_Character_LCD/AE-AQM0802.JPG)
AE-AQM0802

![](https://github.com/teddokano/additional_files/blob/main/I2C_Character_LCD/ACM2004D-FLW-FBW-IIC.JPG)
ACM2004D-FLW-FBW-IIC

![](https://github.com/teddokano/additional_files/blob/main/I2C_Character_LCD/ACM1602NI-FLW-FBW-M01.JPG)
ACM1602NI-FLW-FBW-M01
