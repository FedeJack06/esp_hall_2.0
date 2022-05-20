import string
from numpy import correlate
import uncertainties
from uncertainties import ufloat


"""
R_A  = ufloat( 217 , 6  )
R_B1 = ufloat( 2150 , 26 ) 
R_B2 = ufloat( 2160 , 26 ) 
R_C1 = ufloat( 558 , 10 ) 
R_C2 = ufloat( 557 , 10 ) 
R_D1 = ufloat( 5470 , 59 ) 
R_D2 = ufloat( 5480 , 59 ) 


G_diff = 0.5*((1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)+(R_D2)/(R_C2))*(1+2*(R_B1)/(R_A))


G_modo = (1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)-(R_D2)/(R_C2)

gdiff = G_diff.n
egdiff = G_diff.s

print("guadagno differenziale: " + str(G_diff))

print("guadagno di modo comune: " + str(G_modo))


"""

R_1  = ufloat( 559 , 10 )
R_2 = ufloat( 558 , 10 ) 
R_3 = ufloat( 557 , 10 ) 
R_4 = ufloat( 558 ,  10 ) 
R_5 = ufloat( 458 ,  9) 

corrente = ((R_2)/(R_1))*(5/(R_5))

print("corrente: " + str(corrente))
