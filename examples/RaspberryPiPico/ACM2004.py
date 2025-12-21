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

	lcd.print( [ "00000000000000000000", "11111111111111111111", "22222222222222222222", "33333333333333333333" ] )
	sleep( 1 )
	
	lcd.print( [ "", None, None, None ] )
	sleep( 1 )
	
	lcd.print( [ None, "", None, None ] )
	sleep( 1 )
	
	lcd.print( [ None, None, "", None ] )
	sleep( 1 )
