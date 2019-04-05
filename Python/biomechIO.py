import os, sys
from biomechIOlib import config as cfg
from biomechIOlib.networkserver import NetworkServerWrapper
import struct

thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)
from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from flexseapython.fxUtil import *
from flexseapython.flexsea_demo.streamManager import StreamManager


FLEXSEA_DEVICES = 1


labels = ["genVar[0]", "genVar[1]", "genVar[2]", \
		"genVar[3]", "genVar[4]", "genVar[5]", \
		"genVar[6]", "genVar[7]", "genVar[8]", \
		"genVar[9]"]

varsToStream = [FX_GEN_VAR_0, FX_GEN_VAR_1, FX_GEN_VAR_2, \
			    FX_GEN_VAR_3, FX_GEN_VAR_4, FX_GEN_VAR_5, \
			    FX_GEN_VAR_6, FX_GEN_VAR_7, FX_GEN_VAR_8, \
			    FX_GEN_VAR_9]

def biomechRead(devId, stream):
	#reading
	preamble = ""
	stream()
	readUser(devId)
	preamble = "The current read vals are" + str(getUserRead())
	print(preamble)
	sleep(0.005)
	return

def biomechWrite(devId, stream, ch, value):
	#writing
	# stream()
	writeUser(devId,ch,value) # idx --> 0,1,2,3, val -->value
	# sleep(0.002)
	sleep(0.002)

	return


def fxUserRW(devId, time = 2, time_step = 0.1,  resolution = 100):
	rt_config_name = 'rt1'
	rt_config_path = thisdir +'/biomechIOlib/rt_config.yaml'
	rt_cfg = cfg.load_config(rt_config_path, rt_config_name)
	ROBOT_IP = ''
	ROBOT_PORT = 1

	if 'robot_ip' in rt_cfg:
	    ROBOT_IP = rt_cfg.get('robot_ip')
	    ROBOT_PORT = rt_cfg.get('robot_port')
	#
	s_server = NetworkServerWrapper(ROBOT_IP, ROBOT_PORT)

	s_server.wait_socket()
	#
	print("Server Opened")
	# result = True
	stream = StreamManager(devId,printingRate = 2, labels=labels,varsToStream = varsToStream)
	sleep(0.4)
	stream()
	biomechWrite(devId, stream, ch = 7, value = 0) # Pos Control Mode
	# biomechWrite(devId, stream, ch = 7, value = 1) # Imp Pos Control Mode

	# try:
	# 	input = raw_input
	# except NameError:
	# 	pass
	state = 0
	inev_act = 0
	pfdf_act = 0
	motion_scale = 1800 #/ for hugh
	# motion_scale = 1000  for hugh

	while True:
		buf = s_server.fsm_recv_socket(8)

		biomechWrite(devId, stream, ch = 9, value = int(inev_act)) # INEV

		if len(buf) !=8:
			s_server.close_socket()
			break

		data = struct.unpack('ff',buf)

		# pfdf_act = 0
		# inev_act = 0
		inev_act = data[0]*(motion_scale)

		# inev_act = data[0]*(-motion_scale)
		pfdf_act = data[1]*motion_scale

		# biomechRead(devId, stream)
		# val = 0
		print("PFDF {:.4f}, INEV {:.4f}".format(pfdf_act,inev_act))
		biomechWrite(devId, stream, ch = 8, value = int(pfdf_act)) # PFDF

		# if state ==0:
		# 	state+=1
		# else:
		# 	state = 0

		# preamble = ""
		# stream()
		# command = input("""\'q\': quit the program \n\'w idx val\': writes val to the nth user write value\n\'r\': reads the user values: """)
		# commands = command.split(' ')
		# num_args = len(commands)
		# if num_args == 1 and commands[0] == 'q':
		# 	break
		# elif num_args == 1 and commands[0] == 'r':
		# 	readUser(devId)
		# elif num_args == 3 and commands[0] == 'w':
		# 	try:
		# 		idx = int(commands[1])
		#
		# 		val = int(commands[2])
		# 		if idx > 3 or idx < 0:
		# 			raise Exception("Invalid index recieved, expecting a val between 3 and 0")
		# 	except:
		# 		# Add better exception handling?
		# 		pass
		# 	writeUser(devId,idx,val)
		# else:
		# 	print("Invalid input")
		#
		# sleep(time_step)
		# #stream(nt* getUserWrite())
		# preamble = "The current read vals are" + str(getUserRead())
		# print(preamble)
		#stream.printData(message=preamble)
	del stream
	return result

if __name__ == '__main__':
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	devIds = loadAndGetDevice(fpath, FLEXSEA_DEVICES)

	print('Got devices: ' + str(devIds))
	sleep(0.5)
	print("Start Interface")

	try:
		fxUserRW(devIds[0])
	except Exception as e:
		print("broke: " + str(e))
		pass
