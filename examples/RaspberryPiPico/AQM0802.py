from machine	import	I2C, Pin
from time		import	sleep
from I2C_Character_LCD	import	AQM0802

i2c	= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )
lcd	= AQM0802( i2c )

while True:
	lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" )
	sleep( 1 )
	
	lcd.print( [ "ABCDEFGH", "12345678" ] )
	sleep( 1 )
	
	lcd.print( [ "abcdefgh", None ] )
	sleep( 1 )
	
	lcd.print( [ None, "OPQRSTUV" ] )
	sleep( 1 )
	
	lcd.clear()
	sleep( 1 )

	lcd.print( [ "ABCD", "1234" ] )
	sleep( 1 )
	
