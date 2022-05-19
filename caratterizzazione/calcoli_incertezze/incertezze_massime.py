import uncertanites 
from uncertainties import ufloat





R_A  = ufloat( 217 ,  )
R_B1 = ufloat( 2150 ,  ) 
R_B2 = ufloat( 2160 ,  ) 
R_C1 = ufloat( 558 ,  ) 
R_C2 = ufloat( 557 ,  ) 
R_D1 = ufloat( 5470 ,  ) 
R_D2 = ufloat( 5480 ,  ) 


G_diff = 0.5*((1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)+(R_D2)/(R_C2))*(1+2*(R_B1)/(R_A))


G_modo = (1+(R_D2)/(R_C2))*(R_D1)/(R_C1+R_D1)-(R_D2)/(R_C2)



print("guadagno differenziale: " + G_diff)

print("guadagno di modo comune: " + G_modo)