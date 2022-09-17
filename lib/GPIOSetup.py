from lib.setup import rooms, settings

if settings['Make'] == 'OrangePi':
	import OPi.GPIO as GPIO
else:
	import RPi.GPIO as GPIO

if settings['GPIOMode'] == 'BOARD':
	GPIO.setmode(GPIO.BOARD)
else:
	GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def initialState(active_value):
	if active_value == 0:
		return GPIO.HIGH
	else:
		return GPIO.LOW

for room in rooms:
	for Appliance in room['Appliances']:
		if Appliance['Type'] == 'GPIO':
			if 'ReadOnly' in Appliance:
				roFlag = Appliance['ReadOnly']
			else:
				roFlag = False
			if roFlag:
				if 'PullUpDown' in Appliance:
					if Appliance['PullUpDown'].lower() in ['up', 'pullup']:
						GPIO.setup(Appliance['Pin'], GPIO.IN, GPIO.PUD_UP)
					elif Appliance['PullUpDown'].lower() in ['down', 'pulldown']:
						GPIO.setup(Appliance['Pin'], GPIO.IN, GPIO.PUD_DOWN)
					else:
						GPIO.setup(Appliance['Pin'], GPIO.IN)
						print(F"For pin {Appliance['Pin']}, an invalid setting for PullUpDown was found {Appliance['PullUpDown']}.\nDisabling pullup/down by default.\nValid options for this setting are: up, down, None")
				else:
						GPIO.setup(Appliance['Pin'], GPIO.IN)
			else:
				initial_state = initialState(Appliance['ActiveState'])
				GPIO.setup(Appliance['Pin'], GPIO.OUT, initial=initial_state)
