import numpy as np
import serial

##SPLIT READLINE IN WORD AND PUSH IN ARRAY
data = ser.readline().decode('utf-8').rstrip()

for word in data.split():
	vArdArray = np.append(vArdArray, float(word))
	mediaVarduino_suN = np.mean(vArdArray)
	devStdVard_suN = np.std(vArdArray)





##ROOT T GRAPH UPDATE
import ROOT
gr2 = 	ROOT.TGraphErrors()
c2 = ROOT.TCanvas("c1", "canvas",1920 , 1080)
f2 = ROOT.TF1("f" ,"[0] + [1] * x + [2] * pow(x,2)")

gr2.SetTitle("title")
gr2.GetXaxis().SetTitle("[]")
gr2.GetYaxis().SetTitle("[]")
nn = 0 #counter punti

for a in range[2,3]:
    gr2.SetPoint(nn, x, y)
    gr2.SetPointError(nn, ex, ey)
    if nn==0:
        c2.cd()
        gr2.Draw("AP")
    else:
        c2.Modified()
        c2.Update()
        #ROOT.gPad.Update()
        #gSystem.ProcessEvents()
    nn += 1

gr2.Fit("f")
c2.Modified()
c2.Update()
c2.SaveAs("serial_output/B_vs_Vhall.jpg")
