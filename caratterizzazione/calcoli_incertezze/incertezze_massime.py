import uncertainties
from uncertainties import ufloat



R_A  = ufloat( 217 , 6  )
R_B1 = ufloat( 2150 , 26 ) 
R_B2 = ufloat( 2160 , 26 ) 
R_C1 = ufloat( 558 , 10 ) 
R_C2 = ufloat( 557 , 10 ) 
R_D1 = ufloat( 5470 , 59 ) 
R_D2 = ufloat( 5480 , 59 ) 


G_diff = 0.5*((1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)+(R_D2)/(R_C2))*(1+2*(R_B1)/(R_A))


G_modo = (1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)-(R_D2)/(R_C2)



print("guadagno differenziale: " + G_diff)

print("guadagno di modo comune: " + G_modo)