# I2C_Character_LCD

## What is this?
I²C character LCD class drivers for [AE-AQM0802](https://akizukidenshi.com/catalog/g/g106795/), [ACM2004D-FLW-FBW-IIC](https://akizukidenshi.com/catalog/g/g117381/) and [ACM1602NI-FLW-FBW-M01](https://akizukidenshi.com/catalog/g/g105693/)   

The code runs on [MicroPython](https://micropython.org), operation is checked on [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), [MIMXRT1050-EVKB](https://www.nxp.com/design/design-center/development-boards-and-designs/MIMXRT1050-EVK) and [MIMXRT1010-EVK](https://www.nxp.com/design/design-center/development-boards-and-designs/i-mx-evaluation-and-development-boards/i-mx-rt1010-evaluation-kit:MIMXRT1010-EVK).  

## How can it be used?

### Select test function for target LCD

In bottom of the `I2C_Character_LCD.py` file, there is a `main()` function. In this function, enable one of test function calls.  

```python
def main():
	test_AQM0802()
#	test_ACM2004()
#	test_ACM1602()
		
if __name__ == "__main__":
	import machine
	import	utime
	import	os
	
	main()
```

### Select I2C constructing method for host MCU board

In each test functions, it has I2C constructor calls. enable one of three types of call.   

```python
def test_AQM0802():
	#i2c	= I2C( 0, freq = (100 * 1000) )									# for MIMXRT10xx
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (400_000) )
	i2c		= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )		# for Raspberry Pi Pico
```

### Connect hardware

#### MCU  
Signal|Raspberry Pi Pico|MIMXRT1050|MIMXRT1010
---|---|---|---
SDA|Pin1(GP0)|A4/ADC4/SDA|D14/I2C_SDA
SCL|Pin2(GP1)|A5/ADC5/SCL|D15/I2C_SCL

#### LCD
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
