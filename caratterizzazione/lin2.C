{
   //-------------------------------------------------------
   //  Macro ROOT per fare plot e fit di una serie di punti
   //-------------------------------------------------------
   /*
    * Il file del file di input deve avere il formato
    *
    *   x_1 y_1 ex_1 ey_1
    *   x_2 y_2 ex_2 ey_2
    *   ..  ..  ..   .. 
    *   x_N y_N ex_N ey_N
    *
    * Altri formati possono essere trattati modificando la parte della macro
    * che legge il file
    */
   string filename = "gen.dat";
  string fileName = "gen_manipolato.dat"; 
  //cout<<"File Fit:"<<flush;
  //cin>>fileName;

   /* controllo che il file esista e sia leggibile */
   ifstream inputfile(filename); 
   if (!inputfile.good()) {  
      cout << "Impossibile leggere il file: " << fileName << endl;
      return;
   }

   /* lettura dei dati dal file */
   TGraphErrors gr;
   int i = 0;
   double x, y, ex, ey;
   string uno, due, tre, quattro;
   inputfile >> uno >> due >> tre >> quattro;
   while (inputfile >> x >> ex >> y >> ey) {
      //Qui e' possibile aggiungere un'eventuale propagazione degli errori
      double e_vin = (0.035*8*ex)/sqrt(3);
      double e_vout = ((500/1000000)*y+(400/1000000)*ey)/sqrt(3);
      
      gr.SetPoint(i, x, y);
      gr.SetPointError(i, e_vin, 0.0000001);
      i++;
   }

   
   // Calcolo dell'intervallo di definizione della funzione a partire dai
   // dati contenuti nel grafico
   double xMin = TMath::MinElement(gr.GetN(), gr.GetX());
   double xMax = TMath::MaxElement(gr.GetN(), gr.GetX());
   double clearance = 0.1*(xMax - xMin);
   xMin -= clearance;
   xMax += clearance;

   
   /*
    * Definizione della funzione ed inizializzazione dei parametri
    *
    *
    * Alcuni esempi di funzioni:
    *
    * "[0] + [1]*x"           --> polinomio di primo grado, 2 parametri
    *
    * "[0] + [1]*x + [2]*x*x" --> polinomio di secondo grado, 3 parametri
    *
    * "[0]*exp(-[1]*x)"       --> esponenziale decrescente, 2 parametri
    *
    * "[0]*sin([1]*x - [2])"   --> funzione armonica di ampiezza, frequenza
    *                              e fase configurabili, 3 parametri
    */
   TF1 f("f","[0]+x*[1]", xMin, xMax);
   f.SetParameter(0,0);
   f.SetParameter(1,4);

   /* plot dei dati */
   gr.Draw("AP");
   gr.SetTitle("Vin vs Vout");
   gr.GetXaxis()->SetTitle("Vin [V]");
   gr.GetYaxis()->SetTitle("Vout [V]");

   gr.Print();

   // Fit con la funzione f (che viene automaticamente graficata sui dati)
   gr.Fit("f");
}
