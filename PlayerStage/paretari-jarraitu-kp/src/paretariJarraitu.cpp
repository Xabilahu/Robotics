#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>
#include <fstream>

#define MAX_LINEAR    0.3
#define MIN_LINEAR   -0.3
#define MAX_ANGULAR   0.4
#define MIN_ANGULAR  -0.4

std::ofstream datuFitx;

using namespace std;

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
  float batezbdist;
  float v, w;
  float dist;
  float Kp;

  string fileName = "outData.txt";

  signal(SIGINT, closeAll);
  if (argc < 3)
  {
    std::cout << "Robotak paretari jarraituko dio agindutako" << std::endl;
    std::cout << "distantzia mantenduz." << std::endl;
    std::cout << "Erabilera: " << argv[0] << " <distantzia> <Kp> [<outFitx>]" << std::endl;
    return -1;
  }
  dist = atof(argv[1]);
  Kp = atof(argv[2]);
  if (argc == 4)
    fileName = argv[3];
  datuFitx.open(fileName, ios::out);

  std::cout << "Distantzia: " << dist << " Kp: " << Kp << " outFileName: " << fileName << std::endl;
  datuFitx << "# Distantzia: " << dist << " Kp: " << Kp << "\n";
  datuFitx << "# BatezbDist  Errorea  w v X Y\n";

  try
  {
    using namespace PlayerCc;

    // Sortu bezeroa eta konektatu zerbitzariarekin.
    PlayerClient bezeroa("localhost", 6665);
    // Sortu laser interfazea eta harpidetu bezeroarekin
    LaserProxy laserra(&bezeroa, 0);
    // Sortu position2d interfazea eta harpidetu bezeroarekin
    Position2dProxy robota(&bezeroa, 0);

    std::cout << bezeroa << std::endl;

    robota.SetMotorEnable(true);

    for (i = 0; i < 10; i++)
      bezeroa.Read();

    int readingCount = int(laserra.GetCount() / 3);

    while (1)
    {
      batezbdist = 0;
      bezeroa.Read();
      diff = 0;

      /* Kalkulatu paretarako batezbesteko distantzia */
      for (int i = 0; i < 20; i++) {
        batezbdist += laserra.GetRange(i);
      }

      batezbdist /= 20;

      /* Kalkulatu errorea */
      diff = dist - batezbdist;

      /* Abiadurak finkatu proportzionalki */
      w = Kp * diff;
      v = fabs(1 / w);

      v = (v < MIN_LINEAR) ? MIN_LINEAR : (MAX_LINEAR < v) ? MAX_LINEAR : v;
      w = (w < MIN_ANGULAR) ? MIN_ANGULAR : (MAX_ANGULAR < w) ? MAX_ANGULAR : w;

      robota.SetSpeed(v, w);
      datuFitx << batezbdist << " " << diff << " " << w << " " << v << " " << robota.GetXPos() << " " << robota.GetYPos() << "\n";
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
    return -1;
  }
}
