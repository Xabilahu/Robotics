#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <algorithm>

std::ofstream datuFitx;
std::string fileName = "outData.txt";

void closeAll(int signum)
{
  std::cout << "Interrupt signal (" << signum << ") received\n";
  //datuFitx.close();
  exit(signum);
}

/*  Experiment ideas:
 *
 *  [X]  Try different statistics apart from the mean: median, max, etc.
 *  [X]  Try different section counts.
 *  [ ]  Discard edge values (close to -\frac{\pi}{2} -- \frac{\pi}{2}).
 *  [ ]  Buffer over ceratin time-window.
 *  [ ]  Try different functions for estimating velocities.
 *  [ ]  Distance Histogram approach. 
 *        -> AngleVel = (\theta_{d} - \theta) * \alpha
 *              - \theta_{d}=\frac{Right-Left}{2}
 *              - \alpha=Normalizing term (e.g. between 0-0.3)
 *        -> LinearVel=\abs{\frac{1}{AngleVel}} * \beta
 *              - \beta=Normalizing term (e.g. between 0-0.3)
 *  [ ]  Clamp LinearVel to [-0.3, 0.3] and AngleVel to [-0.4, 0.4] 
 *  [ ]  Try different maps
 */

/*
 * Statistics (-s): DEFAULT <0, Mean> <1, Max> <2, Median>
 * Section Count (-n): DEFAULT 3
 */
int main(int argc, const char **argv)
{

  int st = 0; // Mean
  int secCount = 3;

  if (argc != 1) {
    for (int i=1; i < argc; i++) {
      std::string currentArg(argv[i]);
      std::transform(currentArg.begin(), currentArg.end(), currentArg.begin(), ::tolower);
      bool nextSafe = (i + 1 < argc);

      if ((currentArg.compare("-s") == 0) && nextSafe) {
        st = atoi(argv[++i]);
      } else if ((currentArg.compare("-n") == 0) && nextSafe) {
        secCount = atoi(argv[++i]);
        if (secCount < 3) {
          fprintf(stderr, "[ERROR] Section count cannot be < 3.\n");
          exit(1);
        }
      }
    }
  }

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

    int readingsPerSection = int(count/secCount);
    double sections[secCount][readingsPerSection];
    bool emergency = false;
    double left = 0.0, right = 0.0, forward = 0.0, sleepTime = 0.1;

    while (1)
    {
      bezeroa.Read();

      /* Laserraren irakurketak kudeatu */

      for (int i = 0; i < secCount; i++){
        for (int j = 0; j < readingsPerSection; j++) {
          sections[i][j] = laserra.GetRange(i * readingsPerSection + j);
        }
      }

      double statistics[secCount][3];

      for (int i = 0; i < secCount; i++) {
        double mean = 0.0;
        double maxVal = 0.0;
        for (int j = 0; j < readingsPerSection; j++) {
          mean += sections[i][j];
          if (sections[i][j] > maxVal) maxVal = sections[i][j];
        }
        mean /= readingsPerSection;
        std::sort(sections[i], sections[i] + readingsPerSection);
        statistics[i][0] = mean;
        statistics[i][1] = maxVal;
        statistics[i][2] = sections[i][int(readingsPerSection / 2)];
      }

      /* Robotaren abiadurak finkatu */
      // float x = robota.GetXPos();
      // float y = robota.GetYPos();
      //datuFitx  << x << " " << y  << "\n";
      double stopCond = (secCount / 2);

      if (secCount % 2 == 0) stopCond -= 1;

      if (!emergency) {
        left = 0.0;
        right = 0.0;
        for (int i = 0, j = (secCount / 2) + 1; i <  stopCond; i++, j++) {
          left += statistics[i][st];
          right += statistics[j][st];
        }

        left /= stopCond;
        right /= stopCond;
      }

      if (secCount % 2 == 0) forward = (statistics[(secCount / 2) - 1][st] + statistics[(secCount / 2)][st]) / 2;
      else forward = statistics[(secCount / 2)][st];

      if (forward < 1.0 && !emergency) {
        forward = 0.0;
        if (left > right) {
          left = 6.0; // When divided by 20 = 0.3 rad/s
          right = 0.0;
        } else {
          right = 6.0; // When divided by 20 = 0.3 rad/s
          left = 0.0;
        }
        emergency = true;
        printf("Emergency stop!\n");
      } else if (emergency) {
        if (forward < 1.0) forward = 0.0;
        else emergency = false;
      } 

      // bezeroa.Read();
      // double angleVel = (laserra.GetBearing(((targetSec + 1) * readingsPerSection) - int(readingsPerSection / 2)) - robota.GetYaw()) * 0.1;
      // double linearVel = 1 / max(angleVel, 0.1) * 0.001;

      // printf("Linear: %.2f\tAngular: %.2f\n", linearVel, angleVel);

      // robota.SetSpeed(linearVel, angleVel);
      printf("Forward: %.2f\tLeft: %.2f\n", forward/ 100, (right - left) / 20);
      robota.SetSpeed(forward / 100, (right - left) / 20);
      if (emergency) sleepTime = 2.6;
      else sleepTime = 0.1;

      sleep(sleepTime);
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
    return -1;
  }
}
