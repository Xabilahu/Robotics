#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>
#include <unistd.h>
#include <fstream>
#include <string.h>

#include <sstream>


using namespace std;

ofstream outfile;

/*
''' Helburua: odometria zer den landu eta dakarren errore metakorraz jabetu
    Hiru modu desberdinetara egin daiteke laukizuzena
    Ariketa gisa: hiru moduak zuzendu zehatzagoak izan daitezen trikimailuak
    erabiliz.
    Guztietan, errorea irudikatu grafika batean, posizioak denboran zehar jasoz
'''
*/
void
closeAll(int signum)
{
  std::cout << "Interrupt signal (" << signum << ") received\n";
  outfile.close();
  exit(signum);
}

/* Time based distance and angle calculation
'''  Ariketa:
     side eta v, w-ren araberako denbora teorikoa kalkulatu
     zuzendu denborak laukizuzena zehatzagoa izateko
'''
*/
void squareTime(float v, float w, float side, bool clockwise)
{

  // std::ostringstream ss;
  // ss << side;

  // string filename = "../data/squareTime_s"+ ss.str();
  // outfile.open(filename, ios::out);
  

  // outfile << "Parametroak. v: " << v << " w: " << w << "\n";
  // outfile << "#  Zutabeak: x y theta\n";
  // std::cout << "Abiadurak: " << "v = " << v << " w= " << w << std::endl;

  using namespace PlayerCc;

  try
    {
      // Sortu bezeroa eta konektatu zerbitzariarekin.
      PlayerClient bezeroa("localhost", 6665);
      // Sortu position2d interfazea eta harpidetu bezeroarekin
      Position2dProxy robota(&bezeroa, 0);
    
      for (int i = 0; i<10; i++)
	      bezeroa.Read();
      
      float x0 = robota.GetXPos();
      float y0 = robota.GetYPos();
      float theta0 = robota.GetYaw();
      float resta = 0., error = 20, mult = 1.0;
      int count = 1;
      // fprintf(stdout, "Initial pose:%.2f %.2f %.2f\n ", x0, y0, theta0);
      // outfile << x0 << " " << y0 << " " << theta0 << "\n";
      // while (1)
      // {
      while (error > 0) {
        bezeroa.Read();
        // if (clockwise) robota.SetSpeed(-v, 0);
        // else robota.SetSpeed(v,0);
        // usleep((side / v)*1e6); // Egokitu balioa
        if (clockwise) robota.SetSpeed(0, -w);
        else robota.SetSpeed(0, w);
        usleep((M_PI_2 / (w * mult)) * 1e6); // Egokitu balioa 5.8e6
        robota.SetSpeed(0, 0);
        bezeroa.Read();
        resta = robota.GetYaw();
        if (resta < 0) resta += 2 * M_PI;
        error = M_PI_2 - (resta - theta0);
        printf("%.4f\t%.10f\n", mult, error);
        bezeroa.Read();
        if (clockwise) robota.SetSpeed(0, w);
        else robota.SetSpeed(0, -w);
        usleep((M_PI_2 / (w * mult)) * 1e6); // Egokitu balioa 5.8e6
        bezeroa.Read();
        robota.SetSpeed(0,0);
        mult -= 0.0001;
        if (robota.GetYaw() != theta0) {
          printf("Error!! %.2f\t%.2f\n", robota.GetYaw(), theta0);
          return;
        }
        // outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
        // fprintf(stdout, "Robot pose:%.2f %.2f %.2f\n ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw());
      }
    }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return;
    }

}
/*  Odom based distance and angle calculation
''' Ariketa gisa: +- errore marjina erabili azpihelburu bakoitzera
    heldu dela detektatzeko eta laukizuzena zehatzagoa egiteko
'''
*/
void squareOdom(float v, float w, float side, bool clockwise)
{
  std::ostringstream ss;
  ss << side;
  string filename = "../data/squareOdom_s"+ ss.str();
  outfile.open(filename, ios::out);
  

  outfile << "Parametroak. v: " << v << " w: " << w << "\n";
  outfile << "#  Zutabeak: x y theta\n";


  using namespace PlayerCc;

  try
    {
      // Sortu bezeroa eta konektatu zerbitzariarekin.
      PlayerClient bezeroa("localhost", 6665);
      // Sortu position2d interfazea eta harpidetu bezeroarekin
      Position2dProxy robota(&bezeroa, 0);
    
      for (int i = 0; i<10; i++)
	      bezeroa.Read();
      
      float x0 = robota.GetXPos();
      float y0 = robota.GetYPos();
      float theta0 = robota.GetYaw();
      float x, y, theta;
      float dtheta = 0;
      float d = 0;

      bool inside = true;
      if (clockwise) inside = false;

      float normdtheta = 0, acumdtheta = 0;
      int turnCount = 0;

      while (1)
      {
        bezeroa.Read();
        if (inside)
          {
            robota.SetSpeed(v, 0);
            x = robota.GetXPos();
            y = robota.GetYPos();
            outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
            d = sqrt((x0 - x) * (x0 -x)+(y0 -y)*(y0-y));
            //fprintf(stdout, "d = %.2f\n", d);
            if (d>=side)
            {
              inside = false;
              robota.SetSpeed(0, 0);
              x0 = robota.GetXPos();
              y0 = robota.GetYPos();
              theta0 = robota.GetYaw();
            }
          }
        if (!inside)
          {
            if (clockwise && turnCount != 0) robota.SetSpeed(0, -w); // Aldatu eta egokitu biraketa kontrolatzeko
            else robota.SetSpeed(0, w);

            theta = robota.GetYaw();

            if (theta0 > 0 && theta < 0) theta += 2 * M_PI;
            else if (clockwise && (theta0 < 0 && theta > 0)) theta0 += 2 * M_PI;
            // Valor absoluto de theta + theta0
            dtheta = abs(theta0 - theta) + 2 * normdtheta;
            printf("theta0: %.5f\ttheta: %.5f\tdtheta: %.5f\tnormdtheta: %.5f\n", theta0, theta, dtheta, normdtheta);
            if (dtheta >= M_PI_2)
            {
              inside = true;
              robota.SetSpeed(0, 0);
              x0 = robota.GetXPos();
              y0 = robota.GetYPos();
              theta0 = robota.GetYaw();
              acumdtheta += dtheta - M_PI_2;
              turnCount++;
              normdtheta = acumdtheta / turnCount;
            }
          }
      }
    }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return;
    }
  
}


// /*
// ''' Posizio absolutuak eman behar zaizkio GoTo funtzioari
//     Gainera, itxoin denbora finkatu behar da
//     Ariketa gisa: odometriako balioak jaso ertz bakoitzean eta denboran zehar
//     metatzen den errorea aztertu, gps eta odom moduetan (.world fitxategia)
// '''
// */
void squareGoTo(float side, bool clockwise)
{
  std::ostringstream ss;
  ss << side;
  string filename = "../data/squareGoTo_s"+ ss.str();
  outfile.open(filename, ios::out);
  
  outfile << "#  Zutabeak: x y theta\n";

  using namespace PlayerCc;

  try
    {
      // Sortu bezeroa eta konektatu zerbitzariarekin.
      PlayerClient bezeroa("localhost", 6665);
      // Sortu position2d interfazea eta harpidetu bezeroarekin
      Position2dProxy robota(&bezeroa, 0);
    
      for (int i = 0; i<10; i++)
	      bezeroa.Read();
      
      float x0 = robota.GetXPos();
      float y0 = robota.GetYPos();
      float theta0 = robota.GetYaw();
      std::cout << "Initial pose: " << "x0 = " << x0 << " y0 = " << y0 << " theta0 = " << theta0 << std::endl;

      // Zuzen joan eta bira emateko denbora eman behar zaio
      float t = 10;
      while (1)
      {

        bezeroa.Read();
        if (clockwise) robota.GoTo(x0 - side, y0, theta0);
        else robota.GoTo(x0, y0+side, theta0 + M_PI_2);
        sleep(t);
        bezeroa.Read();
        outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
        fprintf(stdout, "Robot pose:%.2f %.2f %.2f\n ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw());

        bezeroa.Read();
        if (clockwise) robota.GoTo(x0-side, y0+side, theta0 - M_PI_2);
        else robota.GoTo(x0-side, y0+side, theta0 + M_PI);
        sleep(t);
        bezeroa.Read();
        outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
        fprintf(stdout, "Robot pose:%.2f %.2f %.2f\n ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw());

        bezeroa.Read();
        if (clockwise) robota.GoTo(x0, y0+side, theta0 - M_PI);
        else robota.GoTo(x0-side, y0, theta0 - M_PI_2);
        sleep(t);
        bezeroa.Read();
        outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
        fprintf(stdout, "Robot pose:%.2f %.2f %.2f\n ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw());

        bezeroa.Read();
        if (clockwise) robota.GoTo(x0, y0, theta0 + M_PI_2);
        else robota.GoTo(x0, y0, theta0);
        sleep(t);
        bezeroa.Read();
        outfile << robota.GetXPos() << " " << robota.GetYPos() << " " << robota.GetYaw() << "\n";
        fprintf(stdout, "Robot pose:%.2f %.2f %.2f\n ", robota.GetXPos(), robota.GetYPos(), robota.GetYaw());

        /* Eskema amaiera */
      }
    }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return;
    }
      
}


int
main(int argc, const char **argv)
{
  float v,w;
  float side;
  int mode;
  bool clockwise = true;

  signal(SIGINT, closeAll);
  if (argc != 5 && argc != 6)
    {
      std::cout << "Erabilera: " << argv[0] << " <v> <w> <side> <modua> " << std::endl;
      std::cout << "    v: abiadura lineala (m/s)"  << std::endl;
      std::cout << "    w: biraketa abiadura (rad/s)" << std::endl;
      std::cout << "    d: laukizuzenaren aldearen luzera (m)" << std::endl;
      std::cout << "    modua: 1 abiadura bidezko laukizuzena" << std::endl;
      std::cout << "           2 odometrian oinarritutako laukizuzena" << std::endl;
      std::cout << "           3 GoTo bidezko laukizuzena"  << std::endl;
      std::cout << "    noranzkoa: 1 -> clock-wise" << std::endl;
      std::cout << "               2 -> counter clock-wise" << std::endl;
      return(-1);
    }
  v = atof(argv[1]);
  w = atof(argv[2]);
  side = atof(argv[3]);
  mode = atoi(argv[4]);

  if (argc == 6) clockwise = atoi(argv[5]) == 1;

  switch (mode)
    {
    case 1:
      squareTime(v, w, side, clockwise);
      break;
    case 2:
      squareOdom(v, w, side, clockwise);
      break;
    case 3:
      squareGoTo(side, clockwise);
      break;
    default:
      std::cout << "Invalid mode" << std::endl;
      break;
    }
  
  
  return(0);
}
