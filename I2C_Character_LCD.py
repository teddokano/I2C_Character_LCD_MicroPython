from machine	import	Pin, I2C



class I2C_Character_LCD:
	def __init__( self, i2c, address ):
		self.i2c			= i2c
		self.address		= address
		self.device_present	= True
		self.lines			= len( self.line_select )
		
	def send( self, data_flag, value ):
		if self.device_present:
			try:
				self.i2c.writeto( self.address, bytearray( [ self.data_byte if data_flag else self.command_byte, value ] ) )
			except Exception as e:
				self.device_present	= False

	def command( self, command ):
		self.send( False, command )
		utime.sleep_us( 27 )

	def data( self, data ):
		self.send( True, data )
		utime.sleep_ms( 1 )

	def clear( self ):
		self.command( 0x01 )

	def putc( self, char ):
		self.data( char )

	def puts( self, str, line_num = 0 ):
		line		= line_num % self.lines
	
		self.command( 0x80 | (self.line_select[ line ]) )
		
		for c in str:
			self.putc( ord( c ) )

	def print( self, string ):
		if isinstance( string, str ):
			splt	= []
			for i in range( 0, self.width * self.lines, self.width ):
				splt	+= [ string[ i : i + self.width ] ]
			
			self.print( splt )
			
		else:
			for i, s in enumerate( string ):
				if s is not None:
					blank	= "".join( [ " " for _ in range( self.width - len( s ) ) ] )
					self.puts( s + blank, i )


class AE_AQM0802( I2C_Character_LCD ):
	
	DEFAULT_ADDR		= (0x7C >> 1)
	
	def __init__( self, i2c ):
		self.command_byte	= 0x00
		self.data_byte		= 0x40
		self.width			= 8
		self.line_select	= ( 0x00, 0x40 )
		super().__init__( i2c, self.DEFAULT_ADDR )
		
#		init_commands		= [ [ 0x38, 0x39, 0x14, 0x7A, 0x54, 0x6C ], [0x38, 0x0C, 0x01 ] ]	# for 5.0V operation
		init_commands		= [ [ 0x38, 0x39, 0x14, 0x70, 0x56, 0x6C ], [0x38, 0x0C, 0x01 ] ]	# for 3.3V operation

		for seq in init_commands:
			for v in seq:
				self.command( v )
			
			utime.sleep_ms( 200 )
		
		utime.sleep_ms( 200 )

class AQM0802( AE_AQM0802 ):
	def __init__( self, i2c ):
		super().__init__( i2c )
		
class ACM2004D_FLW_FBW_IIC( I2C_Character_LCD ):
	DEFAULT_ADDR		= (0x7E >> 1)
	
	def __init__( self, i2c ):
		self.command_byte	= 0x00
		self.data_byte		= 0x40
		self.width			= 20
		self.line_select	= ( 0x00, 0x40, 0x14, 0x54 )
		super().__init__( i2c, self.DEFAULT_ADDR )
		
		init_commands		= [ 0x38, 0x01, 0x02, 0x0C ]
		for v in init_commands:
			self.command( v )
			utime.sleep_ms( 20 )
		
		utime.sleep_ms( 200 )

class ACM2004( ACM2004D_FLW_FBW_IIC ):
	def __init__( self, i2c ):
		super().__init__( i2c )
		
def test_AQM0802():
	i2c		= I2C( 0, freq = (100 * 1000) )
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (400_000) )
	#i2c	= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )

	lcd		= AQM0802( i2c )
	utime.sleep_ms( 200 )
	lcd.print( "192.168.100.222" )
	
	print( os.uname().machine + " is working!" )
	print( "available I2C target(s): ", end = "" )
	print( [ hex( i ) for i in i2c.scan() ] )

	while True:
		lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" )
		utime.sleep( 1 )
		
		lcd.print( "192.168.100.222" )
		utime.sleep( 1 )
		
		lcd.print( "10.0.1.2" )
		utime.sleep( 1 )

		lcd.print( [ "ABCDEFGH", "12345678" ] )
		utime.sleep( 1 )
		
		lcd.print( [ "abcdefgh", None ] )
		utime.sleep( 1 )
		
		lcd.clear()
		utime.sleep( 1 )

		lcd.print( [ "ABCD", "1234" ] )
		utime.sleep( 1 )
		
		lcd.print( [ "abc", "" ] )
		utime.sleep( 1 )

		lcd.print( [ "", "ABC" ] )
		utime.sleep( 1 )
		
		for i in range( 10000 ):
			lcd.print( f"n={i}" )

def test_ACM2004():
	i2c		= I2C( 0, freq = (100_000) )
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (400_000) )
	#i2c		= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )

	lcd		= ACM2004( i2c )
	utime.sleep_ms( 200 )
	lcd.print( "192.168.100.222" )
	
	print( os.uname().machine + " is working!" )
	print( "available I2C target(s): ", end = "" )
	print( [ hex( i ) for i in i2c.scan() ] )

	while True:
		lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890!@#$%^&" )
		utime.sleep( 1 )

		lcd.print( [ "ABCDEFGHIJKLMNOPQRST", "abcdefghijklmnopqrst", "01234567890123456789", "!@#$%^&*()!@#$%^&*()" ] )
		utime.sleep( 1 )
		
		lcd.print( [ "192.168.100.222", "255.255.255.0", "192.168.100.222", "0.0.0.0" ] )
		utime.sleep( 1 )
		
		lcd.clear()
		utime.sleep( 1 )

		lcd.print( [ "00000000000000000000", "11111111111111111111", "22222222222222222222", "33333333333333333333" ] )
		utime.sleep( 1 )
		
		lcd.print( [ "", None, None, None ] )
		utime.sleep( 1 )
		
		lcd.print( [ None, "", None, None ] )
		utime.sleep( 1 )
		
		lcd.print( [ None, None, "", None ] )
		utime.sleep( 1 )
				
		lcd.print( [ "ABCD", "1234", "abcd", "!@#$" ] )
		utime.sleep( 1 )
		
		for i in range( 10000 ):
			lcd.print( f"n={i}" )
		
def main():
	test_AQM0802()
#	test_ACM2004()
		
if __name__ == "__main__":
	import machine
	import	utime
	import	os
	
	main()
