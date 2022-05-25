import ROOT
import numpy as np
import uncertainties
from uncertainties import ufloat
from ROOT import gStyle

#begin serial
ser = serial.Serial('/dev/tty.usbmodem14201', 9600)
time.sleep(1)
ser.close()
time.sleep(1)
ser.open()

## PREOCESSING
I = 0
stato = 0

#MEDIA SU N MSIURE
mediaVarduino_suN = 0
mediaVhall_suN = 0
devStdVard_suN = 0
devStdVh_suN = 0
vArdArray = np.array([])
vHallArray = np.array([])

#MEDIA SU M MISURE DI N MISURE (PRENDIAMO I VALORI MEDI DI N MISURE E LI METTIAMO IN UN ISTOGRAMMA) SOLO PER V HALL
mediaVarduino_suM = 0
mediaVhall_suM = 0
devStdVard_suM = 0
devStdVh_suM = 0
vArdArray_M = np.array([])
vHallArray_M = np.array([])

#COSTANTI PER IL CALCOLO DI B
N = 1400    #numero di spire elettromagnete
mu = 1000
mu_0 = 4*math.pi*10**(-7)
l1 = ufloat(15e-2,1e-3)
l2 = ufloat(18e-2,1e-3)
l3 = ufloat(3e-2 , 1e-3)
l4 = ufloat(3e-2 , 1e-3)
l5 = ufloat(6e-2 , 1e-3)
l_t = ufloat(7e-2 , 5e-5)
l_m_calc = 2*l1 - 4*l4 + l2 - l_t
l_m_n = l_m_calc.n
l_m_s = l_m_calc.s
l_m = ufloat( l_m_n , l_m_s )

#APERTURA FILE 
plot_rough = open("serial_output/VhvsB+.dat" , "a")   
#plot_rough = open("serial_output/VhvsB-.dat" , "w") #se B negativo

#GRAFICO B vs V_HALL PROGRESSIVO
gr2 = 	ROOT.TGraphErrors()
f2 = ROOT.TF1("f" ,"[0] + [1] * x + [2] * pow(x,2)")
c2 = ROOT.TCanvas("c1", "canvas",1920 , 1080)
gr2.SetTitle("B vs V hall")
gr2.GetXaxis().SetTitle("Campo magnetico [T]")
gr2.GetYaxis().SetTitle("V hall [V]")
nn = 0 #counter punti

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

		#B magnetico

		ei = float(I)*0.3/100 + 0.003
		i = ufloat( float(I) , ei)
		B_rough = (N*i*mu/(l_m+(mu/mu_0)*l_t))
		B = B_rough.n
		eB = B_rough.s/np.sqrt(3)

		#RESET HISTO quando ricevo valore corrente
		c = ROOT.TCanvas("c", "tensione di hall grezza",1920 , 1080)
		h = ROOT.TH1D("isto", "up" ,100, 0, 1.1)
	
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
			for word in data.split():
				vArdArray = np.append(vArdArray, float(word)) #N v arduino in array
			
			##ALCOLO LA MEDIA SULLA TENSIONE DI ARDUINO DI N VALORI
			mediaVarduino_suN = np.mean(vArdArray)
			devStdVard_suN = np.std(vArdArray)

	if stato == 2:
		data = ser.readline().decode('utf-8').rstrip()
		print (data)

		if data == "CORRENTE":
			stato = 3

			#HISTOGRAMMI, ho M volte le medie di N valori nell'histogramma
			c.cd()
			h.Draw()
			name_isto = "istoV_hall{}.jpg".format(I)
			c.SaveAs("serial_output/" + name_isto)
			V_hall_mean = h.GetMean()
			V_hall_dev = h.GetStdDev()

			#SCRIVO Vhall vs B
			plot_rough.write(str(V_hall_mean) + " " + str(B) + " " + str(V_hall_dev) + " " + str(eB) +"\n")
			
			#inserisco punto in grafico Vhall vs B
			gr2.SetPoint(nn, B, V_hall_mean)
			gr2.SetPointError(nn, eB, V_hall_dev)
			if nn==0:
				c2.cd()
				gr2.Draw("AP")
			else:
				c2.Modified()
				c2.Update()
				#ROOT.gPad.Update()
				#gSystem.ProcessEvents()
			nn += 1

		elif data == "BREAK":
			#HISTOGRAMMI, ho M volte le medie di N valori nell'histogramma
			c.cd()
			h.Draw()
			name_isto = "istoV_hall{}.jpg".format(I)
			c.SaveAs("serial_output/" + name_isto)
			V_hall_mean = h.GetMean() 
			V_hall_dev = h.GetStdDev()

			#SCRIVO Vhall vs B
			plot_rough.write(str(V_hall_mean) + " " + str(B) + " " + str(V_hall_dev) + " " + str(eB) +"\n")
			
			#inserisco punto in grafico Vhall vs B
			gr2.SetPoint(nn, B, V_hall_mean)
			gr2.SetPointError(nn, eB, V_hall_dev)
			if nn==0:
				c2.cd()
				gr2.Draw("AP")
			else:
				c2.Modified()
				c2.Update()
				#ROOT.gPad.Update()
				#gSystem.ProcessEvents()
			nn += 1

			ser.close()
			break

		elif data == "VARD":
			stato = 1 #torno a leggere v Arduino
		
		else:     #PASSO M VOLTE DA QUI --- LEGGO RIGHA V HARD con n valori
			vHall.write(data + "\n")
			vHall.close()
			for word in data.split():
				vHallArray = np.append(vHallArray, float(word)) #array con N valori

			#CALCOLO LA MEDIA SU N VALORI MISURATI
			mediaVhall_suN = np.mean(vHallArray)
			devStdVh = np.std(vHallArray)

			#aggiungo a hist la MEDIA di N valori
			h.Fill(mediaVhall_suN)

#CHIUSURA FILE
vHall.close()
vArduino.close()
plot_rough.close()

"""            
                 _   
 _ __ ___   ___ | |_ 
| '__/ _ \ / _ \| __|
| | | (_) | (_) | |_ 
|_|  \___/ \___/ \__|
      
"""

gr2.Fit("f")
c2.Modified()
c2.Update()
c2.SaveAs("serial_output/B_vs_Vhall.jpg")

while True:
	cccc = 0
#programma rimane aperto, cosí rimangono aperti i grafici di root
#Ctrl + C per chiudere il programma