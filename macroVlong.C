{

    double V , v , B , b , EV , ev , EB , eb;
    double V_hall , V_long;
    int i=0;
    string fileName = "VhvsB+.dat";
    string filename = "VhvsB-.dat";

    ifstream input1(fileName);
    ifstream input2(filename);


    ofstream out1("vhall.dat");
    ofstream out2("vlong.dat");
    
    TGraphErrors vhall, vlong;

    TF1 function1 ("f1","[0] + [1]*x");
    TF1  function2 ("f2","[2] + [3]*pow(x,2)");


    while (input1 >> V >> B >> EV >> EB) // maiuscole B+ , minuscole B-
    {
        input2 >> v >> b >> ev >> eb;

        V_hall = (V-v)/2;
        V_long = (V+v)/2;

        double ev_both = sqrt(pow(EV,2)+pow(ev,2));

        //out1 << V_hall << B << ev_both << EB;
        //out2 << V_long << B << ev_both << EB;


        vhall.SetPoint(i, B , V_hall);
        vlong.SetPoint(i, B , V_long);

        vhall.SetPointError(i, EB , ev_both);
        vlong.SetPointError(i, EB , ev_both);

        i++;
        
    }

    TCanvas c1("vhall", "vhall", 1920, 1080);
    TCanvas c2("vlong", "vlong", 1920, 1080);

    vhall.Fit("f1");
    vlong.Fit("f2");

    gStyle->SetOptFit();
    c1.cd();
    vhall.Draw("AP");
    c2.cd();
    vlong.Draw("AP");

    
}