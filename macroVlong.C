{

    double V , v , B , b , EV , ev , EB , eb;
    double V_hall , V_long;
    int i=0;
    string fileName = "VhvsB_150+.dat";
    string filename = "VhvsB_150-.dat";

    ifstream input1(fileName);
    ifstream input2(filename);


    //ofstream out1("vhall.dat");
    //ofstream out2("vlong.dat");
    
    TGraphErrors vhall, vlong;

    TF1 function1 ("f1","[0] + [1]*x");
    TF1  function2 ("f2","[2] + [3]*pow(x,2)");


    while (input1 >> V >> B >> EV >> EB) // maiuscole B+ , minuscole B-
    {
        input2 >> v >> b >> ev >> eb;

        V_hall = (V-v)/2;
        V_long = (V+v)/2;

        double ev_hall = V_hall*sqrt(pow(EV/V,2)+pow(ev/v,2));
        double ev_long = V_long*sqrt(pow(EV/V,2)+pow(ev/v,2));

        //out1 << V_hall << B << ev_hall << EB;
        //out2 << V_long << B << ev_long << EB;


        vhall.SetPoint(i, B , V_hall);
        vlong.SetPoint(i, B , V_long);

        vhall.SetPointError(i, EB , ev_hall);
        vlong.SetPointError(i, EB , ev_long);

        i++;
        
    }

    TCanvas c1("vhall_150", "vhall", 1920, 1080);
    TCanvas c2("vlong_150", "vlong", 1920, 1080);

    vhall.SetTitle("B vs V Hall");
    vhall.GetXaxis()->SetTitle("Campo magnetico [T]");
    vhall.GetYaxis()->SetTitle("V Hall [V]");

    vlong.SetTitle("B vs V long");
    vlong.GetXaxis()->SetTitle("Campo magnetico [T]");
    vlong.GetYaxis()->SetTitle("V long [V]");

    vhall.Fit("f1");
    vlong.Fit("f2");

    gStyle->SetOptFit();
    c1.cd();
    vhall.Draw("AP");
    c2.cd();
    vlong.Draw("AP");

    
}