# FlexSEA_Demo_PositionControl
#=-=-=-=-=-=-=-=-=-=-=-=
# Motor will attempt to hold the starting position.
# Major sensors will be displayed on the terminal.
# Hit Ctrl+C to exit
# 2018/01/10, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched

# User setup:
COM = comPortFromFile()
refreshRate = 0.005   # seconds, communication & FSM
displayDiv = 5       # We refresh the display every 50th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep)

# position controller gains:
pos_KP = 50 # proportional gain
pos_KI = 3 # integral gain

# This is called by the timer:
def timerEvent():
	# Read data & display it:
	i = readActPack(0, 2, displayDiv)
	if i == 0:
		print('\nFSM State =', state)
	# Call state machine:
	stateMachineDemo1()
	flexSEAScheduler.enter(refreshRate, 1, timerEvent) # adds itself back onto schedule

# State machine
state = 'init'
holdPosition = 0
fsmLoopCounter = 0

def stateMachineDemo1():

	global state
	global holdPosition
	global fsmLoopCounter
	
	if state == 'init':
		
		#Skip a few cycles to make sure we are receiving replies
	
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > 2):
			fsmLoopCounter = 0
			state = 'setController'

	elif state == "setController":
		
		# Set Control mode to Position
		print('Setting controller to Position...')
		setControlMode(CTRL_POSITION)
		setZGains(pos_KP, pos_KI, 0, 0)
		holdPosition = myRigid.ex.enc_ang[0]
		setPosition(holdPosition) # Start where we are
		
		# Transition:
		state = 'hold'

	elif state == 'hold':
		# Equilibrium position
		setPosition(holdPosition)

	else:
		# Invalid state - stay here and complain
		print('Invalid FSM state!')
		state = 'Invalid'

# Housekeeping before we quit:
def beforeExiting():
	print('closing com')
	setControlMode(0)
	sleep(0.5)
	hser.close()
	sleep(0.5)
	print('\nDone.\n')

# "Main":
print('\nDemo code - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

# Open serial port:
hser = serial.Serial(COM)
print('Opened', hser.portstr)

# pyFlexSEA:
print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass com handle to pyFlexSEA
sleep(0.1)

# Background: read Rigid and call FSM at 100Hz:
print('Starting the background comm...')


# Main while() loop:
#===================
try:
	while True:
		flexSEAScheduler.enter(refreshRate, 1, timerEvent)
		flexSEAScheduler.run()
		sleep(60*60*24) # arbitrary sleep time
except (KeyboardInterrupt, SystemExit):
	beforeExiting()
	sys.exit()
	

