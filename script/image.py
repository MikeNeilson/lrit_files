#!/bin/env python
import sys
import struct


class primary_header():

	def __init__(self, data):
		"""	
			type = 0
			length = 16
			type code = varies
			total header length = varies (includes this header)
			data field length = size of user data in bits
		"""
		self.type,self.size = struct.unpack("!BH", buffer( data[0:3] ) )
		self.file_type,self.total_length,self.data_field_len = struct.unpack("!BIQ", buffer( data[3:16] ) )
		

	def __str__(self):
		res= "Primary Header\n"
		res+= " File Type: %d\n" % self.file_type
		res+= " Total Header Length: %d\n" % self.total_length
		res+= " Data Field Length: %d\n" % self.data_field_len
		return res

class image_structure_record():
	def __init__(self, data):
		"""
			type = 1
			length = 9
			bits per pixel = ( 1-255)
			colums  = 1-65535
			lines   = 1-65535
			compression = (0,1,2)
		"""
		self.type,self.size = struct.unpack( "!BH", buffer(data[0:3]) )
		self.bpp,self.columns,self.lines,self.compression = struct.unpack("!BHHB", buffer(data[3:self.size]) )
	
	def __str__(self):
		res = "Image Structure Record\n"
		res += " Bits Per Pixel: %d\n" % self.bpp
		res += " Columns: %d\n" % self.columns
		res += " Lines: %d\n" % self.lines
		res += " Compression: %d\n" % self.compression
		return res

class navigation_record():
	def __init__( self,data):
		"""
			type = 2
			length=51
			projection name (32 characters)
			column scaling factor (CFAC)
		"""
		self.type,self.size = struct.unpack("!BH", buffer( data[0:3] ) )
		self.projection =str( buffer(data[3:32+3] ) )
		self.cfac,self.lfac,self.coff,self.loff = struct.unpack( "!IIII", buffer( data[3+32:self.size] ) )
	
	def __str__(self):
		res =  "Navition Record\n"
		res += " Projection: " + self.projection + "\n"
		res += " CFAC: %d\n" % self.cfac
		res += " LFAC: %d\n" % self.lfac
		res += " COFF: %d\n" % self.coff
		res += " LOFF: %d\n" % self.loff
		return res

class data_function_record():
	def __init__( self, data ):
		"""
			type = 3
			length = up to 65532
			data (up to 65532 characters)
		"""
		self.type,self.size = struct.unpack("!BH", buffer( data[0:3] ) )
		self.data = str( buffer( data[3:self.size] ) )

	def __str__( self):
		res = "Data Function Record\n"
		res += "Data:\n"
		res += self.data
		res += "\n"
		return res

class annotation_record():
	def __init__(self, data):
		"""
			type = 4
			length = up to 64
			data 
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.text = str( buffer( data[3:self.size] ) )
	
	def __str__(self):
		res = "Annotation\n"
		res += self.text
		res +="\n"
		return res

class timestamp_record():
	def __init__( self, data ):
		"""
			type = 5
			length = 0
			CCSDS time
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.time = data[3:self.size]
	def __str__( self ):
		res = "TimeStamp Record\n"
		res += repr(self.time)
		res += "\n"
		return res
	
class text_record():
	def __init__( self, data ):
		"""
			type = 6
			length = up to 65532
			text
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.text = str( buffer( data[3:self.size] ) )
	
	def __str__(self):
		res = "Ancillary Text Record\n"
		res += self.text
		res += "\n"
		return res

# Mission Specific headers follow

class segment_id_record():
	def __init__( self, data ):
		"""
			type = 128
			length = 17
			image id = 0 to 65535
			segment sequence number = 0 to max seg - 1
			start column of segment = 0 to max column-1
			start of line segment = 0 to max row - 1
			max segment
			max column
			max row
			
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.image_id,self.segment_seq_number,self.start_column,self.start_line,self.max_segment,self.max_column,self.max_row = struct.unpack( "!HHHHHHH", buffer( data[3:self.size] ) )
		
	def __str__(self):
		res = "Segment ID Record\n"
		res += " Image ID: %d\n" % self.image_id
		res += " Sequence Number: %d\n" % self.segment_seq_number
		res += " Start Column: %d\n" % self.start_column
		res += " Start Line: %d\n" % self.start_line
		res += " Max Segement: %d\n" % self.max_segment
		res += " Max Column: %d\n" % self.max_column
		res += " Max Row: %d\n" % self.max_row
		return res

class noaa_lrit_header():
	def __init__( self, data ):
		"""
			type = 129
			length = 14
			agency sig = "NOAA"
			product id
			product subid
			parameter
			NOAA specific compression
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.sig = str( buffer( data[3:3+4] ) ) 
		self.product_id,self.product_subid,self.parameter,self.compression = struct.unpack( "!HHHB", buffer( data[3+4:self.size] ) )
	def __str__( self ):
		res = "NOAA Lrit File Header\n"
		res += " Signature: " + self.sig + "\n"
		res += " Product ID: %d\n" % self.product_id
		res += " Product Sub ID: %d\n" % self.product_subid
		res += " Parameter: %d\n" % self.parameter
		res += " NOAA compression: %d\n" % self.compression
		return res

class header_structure_record():
	def __init__( self, data ):
		"""
			type = 130
			length = variable
		"""
		pass

class rice_compression_header():
	def __init__( self, data ):
		"""
			type = 131
			length = 7
			flags
			pixelsPerBlock
			scanLinesPerPacket
		"""
		self.type,self.size = struct.unpack( "!BH", buffer( data[0:3] ) )
		self.flags,self.pixels_per_block,self.scan_lines_per_packet = struct.unpack( "!HBB", buffer( data[3:self.size] ) )
	def __str__(self):
		res = "RICE Compression Header\n"
		res += " Flags: %d\n" % self.flags
		res += " Pixels Per Block: %d\n" % self.pixels_per_block
		res += " Scan Lines Per Packet: %d\n" % self.scan_lines_per_packet
		return res

def get_next_header(data):
	# get the next header, return that header and the rest of the data
	type,size = struct.unpack("!BH", buffer(data[0:3]) )
	#print type
	#print size
	header = None
	if type == 0:
		header = primary_header( data[0:size] )
	elif type == 1:
		header = image_structure_record( data[0:size] ) 
	elif type == 2:
		header = navigation_record( data[0:size] ) 
	elif type == 3:
		header = data_function_record( data[0:size] ) 
	elif type == 4:
		header = annotation_record( data[0:size] ) 
	elif type == 5:
		header = timestamp_record( data[0:size] ) 
	elif type == 6:
		header = text_record( data[0:size] ) 
	elif type == 128:
		header = segment_id_record( data[0:size] )
	elif type == 129:
		header = noaa_lrit_header( data[0:size] )
	elif type == 131:
		header = rice_compression_header( data[0:size] )
	else:
		pass
		#print "Header type %d is not implemented" % type 
		


	return header, data[size:]	


if __name__ == "__main__":
	file = sys.argv[1]
	f = open(file,"rb")
	data = bytearray( f.read() )
	f.close()
	print repr( data[0:16])
	header,data = get_next_header( data )
	
	print header

	while len(data) > 0:
		header,data = get_next_header( data )
		print header
	