from machine	import	I2C
import	time

class I2C_Character_LCD:
	"""
	An abstraction class to make user interface for the character LCDs.
	"""

	def __init__( self, i2c, address ):
		"""
		Parameters
		----------
		i2c		: I2C instance
		address	: int
		"""
		self.i2c			= i2c
		self.address		= address
		self.device_present	= True
		self.lines			= len( self.line_select )
		self.command_byte	= 0x00
		self.data_byte		= 0x40
		
	def send( self, data_flag, value ):
		"""
		Parameters
		----------
		data_flag	: flag to distinguish command or data
		value		: int
		"""
		if self.device_present:
			try:
				self.i2c.writeto( self.address, bytearray( [ self.data_byte if data_flag else self.command_byte, value ] ) )
			except Exception as e:
				self.device_present	= False

	def command( self, command ):
		"""
		Parameters
		----------
		command		: int
		"""
		self.send( False, command )
		time.sleep_us( 27 )
		time.sleep_ms( 1 )

	def data( self, data ):
		"""
		Parameters
		----------
		data		: int
		"""
		self.send( True, data )
		time.sleep_ms( 1 )

	def clear( self ):
		self.command( 0x01 )

	def putc( self, char ):
		self.data( char )

	def puts( self, str, line_num = 0 ):
		"""
		Parameters
		----------
		str			: string to put on LCD
		line_num	: int, option. line number
		"""
		line		= line_num % self.lines
	
		self.command( 0x80 | (self.line_select[ line ]) )
		
		for c in str:
			self.putc( ord( c ) )

	def print( self, string ):
		"""
		Parameters
		----------
		string		: a string or list of string
		"""
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
	"""
	AE_AQM0802: 8 characters x 2 lines LCD
	https://akizukidenshi.com/catalog/g/g106795/
	
	pins	name
	1		VDD(3.3V)
	2		nRESET
	3		I2C_SCL
	4		I2C_SDA
	5		GND
	"""
	DEFAULT_ADDR		= (0x7C >> 1)
	
	def __init__( self, i2c ):
		"""
		Parameters
		----------
		i2c		: I2C instance
		"""
		self.width			= 8
		self.line_select	= ( 0x00, 0x40 )
		super().__init__( i2c, self.DEFAULT_ADDR )
		
#		init_commands		= [ [ 0x38, 0x39, 0x14, 0x7A, 0x54, 0x6C ], [0x38, 0x0C, 0x01 ] ]	# for 5.0V operation
		init_commands		= [ [ 0x38, 0x39, 0x14, 0x70, 0x56, 0x6C ], [0x38, 0x0C, 0x01 ] ]	# for 3.3V operation

		for seq in init_commands:
			for v in seq:
				self.command( v )
			
			time.sleep_ms( 200 )
		
		time.sleep_ms( 200 )

class ACM2004D_FLW_FBW_IIC( I2C_Character_LCD ):
	"""
	ACM2004D_FLW_FBW_IIC: 20 characters x 4 lines LCD
	https://akizukidenshi.com/catalog/g/g117381/

	pins	name
	1		VSS(GND)
	2		VDD(5V)
	3		V0(NC)
	4		I2C_SDA
	5		I2C_SCL
	6		Backlight+(5V)
	7		Backlight-(0V)
	"""
	DEFAULT_ADDR		= (0x7E >> 1)
	
	def __init__( self, i2c ):
		"""
		Parameters
		----------
		i2c		: I2C instance
		"""
		self.width			= 20
		self.line_select	= ( 0x00, 0x40, 0x14, 0x54 )
		super().__init__( i2c, self.DEFAULT_ADDR )
		
		init_commands		= [ 0x38, 0x01, 0x02, 0x0C ]
		for v in init_commands:
			self.command( v )
			time.sleep_ms( 20 )
		
		time.sleep_ms( 200 )

class ACM1602NI_FLW_FBW( I2C_Character_LCD ):
	"""
	ACM1602NI_FLW_FBW: 16 characters x 2 lines LCD
	https://akizukidenshi.com/catalog/g/g105693/
	
	pins	name
	1		VSS(GND)
	2		VDD(3.3V)
	3		V0(contrast adj)
	4		I2C_SCL
	5		I2C_SDA
	6		Backlight+(3.3V)
	7		Backlight-(0V)
	"""
	DEFAULT_ADDR		= (0xA0 >> 1)
	
	def __init__( self, i2c ):
		"""
		Parameters
		----------
		i2c		: I2C instance
		"""
		self.width			= 16
		self.line_select	= ( 0x00, 0xC0 )
		super().__init__( i2c, self.DEFAULT_ADDR )

		self.data_byte		= 0x80

		init_commands		= [ 0x01, 0x38, 0x0F, 0x06 ]
		for v in init_commands:
			self.command( v )
			time.sleep_ms( 1 )
				
class AQM0802( AE_AQM0802 ):
	def __init__( self, i2c ):
		super().__init__( i2c )
		
class ACM2004( ACM2004D_FLW_FBW_IIC ):
	def __init__( self, i2c ):
		super().__init__( i2c )
		
class ACM1602( ACM1602NI_FLW_FBW ):
	def __init__( self, i2c ):
		super().__init__( i2c )
		
def test_AQM0802():
	#i2c	= I2C( 0, freq = (100 * 1000) )									# for MIMXRT10xx
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (400_000) )
	i2c		= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )		# for Raspberry Pi Pico

	lcd		= AQM0802( i2c )
	time.sleep_ms( 200 )
	lcd.print( "192.168.100.222" )
	
	print( os.uname().machine + " is working!" )
	print( "available I2C target(s): ", end = "" )
	print( [ hex( i ) for i in i2c.scan() ] )

	while True:
		lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" )
		time.sleep( 1 )
		
		lcd.print( "192.168.100.222" )
		time.sleep( 1 )
		
		lcd.print( "10.0.1.2" )
		time.sleep( 1 )

		lcd.print( [ "ABCDEFGH", "12345678" ] )
		time.sleep( 1 )
		
		lcd.print( [ "abcdefgh", None ] )
		time.sleep( 1 )
		
		lcd.clear()
		time.sleep( 1 )

		lcd.print( [ "ABCD", "1234" ] )
		time.sleep( 1 )
		
		lcd.print( [ "abc", "" ] )
		time.sleep( 1 )

		lcd.print( [ "", "ABC" ] )
		time.sleep( 1 )
		
		for i in range( 10000 ):
			lcd.print( f"n={i}" )

def test_ACM2004():
	#i2c	= I2C( 0, freq = (100_000) )									# for MIMXRT10xx
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (400_000) )
	i2c		= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 400_000 )		# for Raspberry Pi Pico

	lcd		= ACM2004( i2c )
	time.sleep_ms( 200 )
	lcd.print( "192.168.100.222" )
	
	print( os.uname().machine + " is working!" )
	print( "available I2C target(s): ", end = "" )
	print( [ hex( i ) for i in i2c.scan() ] )

	while True:
		lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890!@#$%^&" )
		time.sleep( 1 )

		lcd.print( [ "ABCDEFGHIJKLMNOPQRST", "abcdefghijklmnopqrst", "01234567890123456789", "!@#$%^&*()!@#$%^&*()" ] )
		time.sleep( 1 )
		
		lcd.print( [ "192.168.100.222", "255.255.255.0", "192.168.100.1", "0.0.0.0" ] )
		time.sleep( 1 )
		
		lcd.clear()
		time.sleep( 1 )

		lcd.print( [ "00000000000000000000", "11111111111111111111", "22222222222222222222", "33333333333333333333" ] )
		time.sleep( 1 )
		
		lcd.print( [ "", None, None, None ] )
		time.sleep( 1 )
		
		lcd.print( [ None, "", None, None ] )
		time.sleep( 1 )
		
		lcd.print( [ None, None, "", None ] )
		time.sleep( 1 )
				
		lcd.print( [ "ABCD", "1234", "abcd", "!@#$" ] )
		time.sleep( 1 )
		
		for i in range( 10000 ):
			lcd.print( f"n={i}" )
		
def test_ACM1602():

	###
	### USE lower I2C-SCL frequency due to the LCD module's I2C signal imcompatibility
	###
	
	#i2c	= I2C( 0, freq = (70_000) )											# for MIMXRT10xx
	#i2c	= machine.SoftI2C( sda = "D14", scl = "D15", freq = (70_000) )
	i2c		= I2C( 0, sda = Pin( 0 ), scl = Pin( 1 ), freq = 50_000 )			# for Raspberry Pi Pico

	time.sleep_ms( 200 )

	lcd		= ACM1602( i2c )
	time.sleep_ms( 200 )
	lcd.print( "192.168.100.222" )
	
	print( os.uname().machine + " is working!" )
	print( "available I2C target(s): ", end = "" )
	print( [ hex( i ) for i in i2c.scan() ] )

	while True:
		lcd.print( "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$" )
		time.sleep( 1 )

		lcd.print( [ "ABCDEFGHIJKLMNOP", "0123456789012345" ] )
		time.sleep( 1 )
		
		lcd.print( [ "192.168.100.222", "255.255.255.0" ] )
		time.sleep( 1 )
		
		lcd.clear()
		time.sleep( 1 )

		lcd.print( [ "0000000000000000", "1111111111111111" ] )
		time.sleep( 1 )
		
		lcd.print( [ "", None ] )
		time.sleep( 1 )
		
		lcd.print( [ None, "" ] )
		time.sleep( 1 )
		
		lcd.print( [ "ABCD", "1234", "abcd", "!@#$" ] )
		time.sleep( 1 )
		
		for i in range( 10000 ):
			lcd.print( f"n={i}" )
		
def main():
	test_AQM0802()
#	test_ACM2004()
#	test_ACM1602()
		
if __name__ == "__main__":
	from machine import	Pin
	import 	machine
	import	os
	
	main()
