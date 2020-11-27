#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>
#include <fstream>
#include <gsl/gsl_fit.h>

/* PARAMETROAK ZEHAZTU */

#define LASER_IZPI_KOP 90

std::ofstream datuFitx;

void closeAll(int signum)
{
  std::cout << "Interrupt signal (" << signum << ") received\n";
  datuFitx.close();
  exit(signum);
}

int main(int argc, const char **argv)
{
  int i, ind;
  float diff;
  float v, w;
  float dist;
  std::string fileName = "outData.txt";
  float Kp;

  signal(SIGINT, closeAll);
  if (argc < 2)
  {
    std::cout << "Robotak paretari jarraituko dio " << std::endl;
    std::cout << "angeluaren gaineko erregresio lineala erabiliz." << std::endl;
    std::cout << "Erabilera: " << argv[0] << " <Kp> [<outFitx>]" << std::endl;
    return -1;
  }
  Kp = atof(argv[1]);
  if (argc == 3)
    fileName = argv[2];
  datuFitx.open(fileName, std::ios::out);

  try
  {
    double c0, c1, cov00, cov01, cov11, batura;
    double x[LASER_IZPI_KOP], y[LASER_IZPI_KOP];
    double theta, angelua, y0, y1, maxRange;
    int j = 0;

    using namespace PlayerCc;

    // Sortu bezeroa eta konektatu zerbitzariarekin.
    PlayerClient bezeroa("localhost", 6665);
    // Sortu laser interfazea eta harpidetu bezeroarekin
    LaserProxy laserra(&bezeroa, 0);
    // Sortu position2d interfazea eta harpidetu bezeroarekin
    Position2dProxy robota(&bezeroa, 0);

    for (i = 0; i < 10; i++)
      bezeroa.Read();

    maxRange = laserra.GetMaxRange() - 6;

    while (1)
    {
      diff = 0;
      bezeroa.Read();
      /* Kalkulatu irakurketa "motzen" proiekzioak */
      j = 0;
      for (i = 0; i < LASER_IZPI_KOP; i++)
      {
        /* Hemen laser izpiak proiektuatu behar dira */
        if (laserra.GetRange(i) < maxRange) {
          x[j] = laserra.GetRange(i) * cos(laserra.GetBearing(i));
          y[j] = laserra.GetRange(i) * sin(laserra.GetBearing(i));
          j++;
        }
      }

      /* regresio lineala: karratu txikienen metodoa */
      /* KONTUZ!! j indizeak regresioa kalkulatzeko erabiliko den */
      /* puntu kopurua adierazten du!!  */
      gsl_fit_linear(x, 1, y, 1, j,
                     &c0, &c1, &cov00, &cov01, &cov11,
                     &batura);

      /* Kalkulatu robota eta paretaren arteko angelua */
      y0 = c0; //x0 = 0
      y1 = c0 + c1; //x1 = 1
      angelua = atan2(y1-y0, 1);
      if (angelua < 0 || isnan(angelua)) angelua=0.0;
      printf("Angelua %f \n" , angelua);
      /* Abiadurak finkatu */
      w = angelua * Kp;
      v = min(1 / w, 0.2f);
      robota.SetSpeed(v, w);
      // Kp = 0.45;
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
    return -1;
  }

  return 0;
}
