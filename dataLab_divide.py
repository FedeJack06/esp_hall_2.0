from ast import While
import string
from tokenize import String
from matplotlib.pyplot import plot
import ROOT
import numpy as np
import uncertainties
from uncertainties import ufloat
import math
from ROOT import gStyle

#COSTANTI PER IL CALCOLO DI B
N = 1400    #numero di spire elettromagnete
mu = 1000
mu_0 = 4*math.pi*10**(-7)
l1 = ufloat(15e-2,1e-3)
l2 = ufloat(18e-2,1e-3)
l3 = ufloat(3e-2 , 1e-3)
l4 = ufloat(3e-2 , 1e-3)
l5 = ufloat(6e-2 , 1e-3)
l_t = ufloat(7e-3 , 5e-5)
l_m_calc = 2*l1 - 4*l4 + l2 - l_t
l_m_n = l_m_calc.n
l_m_s = l_m_calc.s
l_m = ufloat( l_m_n , l_m_s )

#APERTURA FILE 
plot_rough = open("output/VhvsB+.dat" , "w")   
#plot_rough = open("serial_output/VhvsB-.dat" , "w") #se B negativo

c = ROOT.TCanvas("c", "tensione di hall grezza",3840 , 2160)
c.Divide(3,4)
dd = 1 #count divide canvas

#GRAFICO B vs V_HALL PROGRESSIVO
gr2 = ROOT.TGraphErrors()
f2 = ROOT.TF1("f" ,"[0] + [1] * x + [2] * pow(x,2)")
c2 = ROOT.TCanvas("c1", "canvas", 1920, 1080)
gr2.SetTitle("B vs V hall")
gr2.GetXaxis().SetTitle("Campo magnetico [T]")
gr2.GetYaxis().SetTitle("V hall [V]")
nn = 0 #counter punti

#### INPUT DATI DA FILE
corr = ["0.00", "0.10", "0.20", "0.30", "0.40", "0.50", "0.60", "0.70", "0.80", "0.90", "1.00", "1.10"]
for I in corr:
	print("top")
	vHallFile = open("serial_output-_150/vHall{}.dat".format(I), "r")

	#data = vHallFile.readline().decode('utf-8').rstrip()
	#print (data)

	#B magnetico
	B_rough = ((N*float(I))*mu/(l_m+(mu/mu_0)*l_t))*2    
	B = B_rough.n
	eB = B_rough.s/np.sqrt(3)

	#RESET HISTO quando ricevo valore corrente
	
	h = ROOT.TH1D("Distribuzione V Hall", "V_H I_{}A".format(I) ,60 , 0, 0)
    
	#PASSO M VOLTE DA QUI --- LEGGO RIGA V ARDUINO
	for line in vHallFile:
		for word in line.split():
			#HISTOGRAMMI, ho M volte le medie di N valori nell'histogramma
			if float(word) > 0.3:
				h.Fill(float(word))
				#print(word)

	c.cd(dd)
	dd += 1

	gaus = ROOT.TF1("gausss", "gaus(0)+pol0(3)")
	gaus.SetParLimits(0, 20, 70)
	gaus.SetParLimits(1, 0.6, 0.9)
	gaus.SetParLimits(2, 0.003, 0.008)
	h.Fit("gausss")
	gaus.Print()
	
	gStyle.SetOptFit()
	h.DrawClone()

	V_hall_mean = gaus.GetParameter("Mean")
	V_hall_dev = gaus.GetParameter("Sigma")
	#V_hall_mean = h.GetMean()
	#V_hall_dev = h.GetStdDev()

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

#CHIUSURA FILE

plot_rough.close()

"""            
                 _   
 _ __ ___   ___ | |_ 
| '__/ _ \ / _ \| __|
| | | (_) | (_) | |_ 
|_|  \___/ \___/ \__|
      
"""
c.SaveAs("output/istoV_hall_{}.jpg".format(I))

gr2.Fit("f")
c2.Modified()
c2.Update()
c2.SaveAs("output/B_vs_Vhall.jpg")

while True:
	ccc = 0