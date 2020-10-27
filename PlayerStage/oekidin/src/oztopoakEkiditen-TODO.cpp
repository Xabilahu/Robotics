#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

std::ofstream datuFitx;
std::string fileName = "outData.txt";

void closeAll(int signum)
{
  std::cout << "Interrupt signal (" << signum << ") received\n";
  //datuFitx.close();
  exit(signum);
}

int main(int argc, const char **argv)
{
  int i;
  signal(SIGINT, closeAll);

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

    // Fitxategia prestatu
    // datuFitx.open(fileName, ios::out);
    // datuFitx  << "# Robotaren (rx ry) koordenatuak \n";

    int count = laserra.GetCount();

    std::cout << "Scan count: " << count << std::endl;
    std::cout << "Scan resolution: " << laserra.GetScanRes() << std::endl;
    std::cout << "Range resolution: " << laserra.GetRangeRes() << std::endl;
    std::cout << "Max Range: " << laserra.GetMaxRange() << std::endl;
    std::cout << "Max angle: " << laserra.GetMaxAngle() << std::endl;
    std::cout << "Min angle: " << laserra.GetMinAngle() << std::endl;

    int readingsPerSection = int(count / 3);

    while (1)
    {
      double meanLeft = 0.0, meanForward = 0.0, meanRight = 0.0;
      bezeroa.Read();

      /* Laserraren irakurketak kudeatu */

      for (int i = 0; i < count; i++)
      {
        int currentSection = int(i / readingsPerSection);
        double reading = laserra.GetRange(i);
        if (currentSection == 0)
        {
          meanRight += reading;
        }
        else if (currentSection == 1)
        {
          meanForward += reading;
        }
        else
        {
          meanLeft += reading;
        }
      }

      meanLeft /= readingsPerSection;
      meanForward /= readingsPerSection;
      meanRight /= readingsPerSection;

      // This piece of code aims to add noise into robot's decisions.
      // if (fabs(meanLeft - meanRight) < 1.0) {
      //   int multiplier = rand() % 2 - 1;
      //   double shift = rand() % 1000 / 1000.0;
      //   meanLeft += shift * multiplier;
      //   meanRight += shift * (1 - multiplier);
      // }

      /* Robotaren abiadurak finkatu */
      float x = robota.GetXPos();
      float y = robota.GetYPos();
      //datuFitx  << x << " " << y  << "\n";

      printf("Forward: %.2f\tLeft: %.2f\tRight: %.2f\n", meanForward, meanLeft, meanRight);

      robota.SetSpeed(meanForward / 100, (meanLeft - meanRight) / 20);
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
    return -1;
  }
}
