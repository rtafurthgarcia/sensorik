from machine import UART
from ubinascii import b2a_base64

class TTLCamera:
	SERIALNUM = 0    # start with 0, each camera should have a unique ID.

	COMMANDSEND = 0x56
	COMMANDREPLY = 0x76
	COMMANDEND = 0x00

	CMD_GETVERSION = 0x11
	CMD_RESET = 0x26
	CMD_TAKEPHOTO = 0x36
	CMD_READBUFF = 0x32
	CMD_GETBUFFLEN = 0x34

	FBUF_CURRENTFRAME = 0x00
	FBUF_NEXTFRAME = 0x01

	FBUF_STOPCURRENTFRAME = 0x00

	getversioncommand = [COMMANDSEND, SERIALNUM, CMD_GETVERSION, COMMANDEND]
	resetcommand = [COMMANDSEND, SERIALNUM, CMD_RESET, COMMANDEND]
	takephotocommand = [COMMANDSEND, SERIALNUM, CMD_TAKEPHOTO, 0x01, FBUF_STOPCURRENTFRAME]
	getbufflencommand = [COMMANDSEND, SERIALNUM, CMD_GETBUFFLEN, 0x01, FBUF_CURRENTFRAME]
	readphotocommand = [COMMANDSEND, SERIALNUM, CMD_READBUFF, 0x0c, FBUF_CURRENTFRAME, 0x0a]

	def __init__(self, uart: UART):
		self.uart = uart

	def __checkreply(r, b) -> bool:
		r = map( ord, r )
		if(r[0] == TTLCamera.COMMANDREPLY and r[1] == TTLCamera.SERIALNUM and r[2] == b and r[3] == 0x00):
			return True
		return False

	def reset(self) -> bool:
		cmd = ''.join(map(chr, TTLCamera.resetcommand))
		self.uart.write(cmd)
		reply = self.uart.read(100)
		r = list(reply)
		if self.__checkreply(r, TTLCamera.CMD_RESET):
			return True
		return False

	def getversion(self) -> str:
		cmd = ''.join(map(chr, TTLCamera.getversioncommand))
		self.uart.write(cmd)
		reply = self.uart.read(16)
		if (reply is None):
			raise RuntimeError("Couldnt connect myself to the camera")	
		r = list(reply)
		# print r
		if self.__checkreply(r, TTLCamera.CMD_GETVERSION):
			return r
		raise RuntimeError("Couldnt connect myself to the camera")

	def takephoto(self):
		cmd = ''.join(map(chr, TTLCamera.takephotocommand))
		self.uart.write(cmd)
		reply = self.uart.read(5)
		r = list(reply)
		# print r
		if(self.__checkreply(r, TTLCamera.CMD_TAKEPHOTO) and r[3] == chr(0x0)):
			return True
		return False

	def __getbufferlength(self) -> int:
		cmd = ''.join(map(chr, TTLCamera.getbufflencommand ))
		self.uart.write(cmd)
		reply = self.uart.read(9)
		r = list(reply)
		if(self.__checkreply(r, TTLCamera.CMD_GETBUFFLEN) and r[4] == chr(0x4)):
			l = ord(r[5])
			l <<= 8
			l += ord(r[6])
			l <<= 8
			l += ord(r[7])
			l <<= 8
			l += ord(r[8])
			return l
		return 0

	def __readbuffer(self, bytes) -> str:
		addr = 0   # the initial offset into the frame buffer
		photo = []

		# bytes to read each time (must be a mutiple of 4)
		inc = 8192

		while(addr < bytes):
			# on the last read, we may need to read fewer byteself.uart.
			chunk = min(bytes-addr, inc)

			# append 4 bytes that specify the offset into the frame buffer
			command = self.readphotocommand + [(addr >> 24) & 0xff, (addr>>16) & 0xff, (addr>>8 ) & 0xff, addr & 0xff]

			# append 4 bytes that specify the data length to read
			command += [(chunk >> 24) & 0xff, (chunk>>16) & 0xff, (chunk>>8 ) & 0xff, chunk & 0xff]

			# append the delay
			command += [1,0]

			# print map(hex, command)
			print("Reading", chunk, "bytes at", addr)

			# make a string out of the command byteself.uart.
			cmd = ''.join(map(chr, command))
			self.uart.write(cmd)

			# the reply is a 5-byte header, followed by the image data
			#   followed by the 5-byte header again.
			reply = self.uart.read(5+chunk+5)

			# convert the tuple reply into a list
			r = list(reply)
			if(len(r) != 5+chunk+5):
				# retry the read if we didn't get enough bytes back.
				print("Read", len(r), "Retrying.")
				continue

			if(not self.__checkreply(r, TTLCamera.CMD_READBUFF)):
				raise RuntimeError("error reading photo")
			
			# append the data between the header data to photo
			photo += r[5:chunk+5]

			# advance the offset into the frame buffer
			addr += chunk

		print(addr, "Bytes written")
		return photo
	
	def savephototobase64(self) -> bytes:
		bytes = self.__getbufferlength()
		photo = self.__readbuffer(bytes)
		photodata = ''.join(photo)
		return b2a_base64(photodata)

	def stream(self, refreshrate: int) -> bytes:
		raise NotImplementedError()