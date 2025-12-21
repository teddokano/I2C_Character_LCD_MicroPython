from machine	import	I2C
from time		import	sleep
from I2C_Character_LCD	import	ACM1602

i2c	= I2C( 0, freq = (70_000) )
lcd	= ACM1602( i2c )

while True:
	lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$" )
	sleep( 1 )

	lcd.print( [ "ABCDEFGHIJKLMNOP", "0123456789012345" ] )
	sleep( 1 )

	lcd.clear()
	sleep( 1 )

	lcd.print( [ "0000000000000000", "1111111111111111" ] )
	sleep( 1 )
	
	lcd.print( [ "", None ] )
	sleep( 1 )
	
	lcd.print( [ None, "" ] )
	sleep( 1 )
