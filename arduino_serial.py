import serial
import time

#begin serial
ser = serial.Serial('/dev/tty.usbmodem14201', 9600)
time.sleep(1)
ser.close()
time.sleep(1)
ser.open()

## PREOCESSING
I = 0
stato = 0

#CICLO LETTURA E CALCOLI
while True:
	#### INPUT DATI DA ARDUINO
	if stato == 0:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)

	if data == "CORRENTE" or stato == 3:
		I = ser.readline().decode('utf-8').rstrip()
		print ("CORR " + I)

		#TORNA A LEGGERE SERIALE ALL'INIZIO
		stato = 0
	
	#OPEN FILE
	vArduino = open("serial_output/vArduino"+ str(I) +".dat", "a")
	vHall = open("serial_output/vHall" + str(I) + ".dat", "a")

	if data == "VARD":
		stato = 1

	if stato == 1:
		data = ser.readline().decode('utf-8').rstrip() #12.6
		print (data)

		if data == "VHALL":
			stato = 2
		else:                  #PASSO M VOLTE DA QUI --- LEGGO RIGA V ARDUINO
			vArduino.write(data + "\n")
			vArduino.close()

	if stato == 2:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)

		if data == "CORRENTE":
			stato = 3

		elif data == "BREAK":
			ser.close()
			break

		elif data == "VARD":
			stato = 1 #torno a leggere v Arduino
		
		else:     #PASSO M VOLTE DA QUI --- LEGGO RIGHA V HARD con n valori
			vHall.write(data + "\n")
			vHall.close()

#CHIUSURA FILE
vHall.close()
vArduino.close()