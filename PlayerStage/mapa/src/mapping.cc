#include <libplayerc++/playerc++.h>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <csignal>
#include <math.h>

// Opencv
//#include <cv.h>
//#include <highgui.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui_c.h>

// threads
#include <thread>

// Keyboard
#include <ncurses.h>
#include <curses.h>

#define UP_ARROW 72
#define DOWN_ARROW 80
#define LEFT_ARROW 75
#define RIGHT_ARROW 77
#include "args.h"

#define WINC 0.2
#define VINC 0.1
#define VMAX 0.5
#define WMAX 1.0

#define MXSIZE 1000
#define MYSIZE 1000
#define SCALE 20

#define MIN_LINEAR    -0.3
#define MAX_LINEAR    0.3
#define MIN_ANGULAR   -0.4
#define MAX_ANGULAR   0.4

float rx, ry, rtheta;
float rx0, ry0, rtheta0;

cv::Mat map = cv::Mat(MXSIZE, MYSIZE, CV_8UC3, cv::Scalar(0, 0, 0));

/* Gorria, robotarentzat */
cv::Scalar color0 = cv::Scalar(0, 0, 255);
/* Urdina, oztopoentzat */
cv::Scalar color1 = cv::Scalar(255, 0, 0);

float v = 0, w = 0;

std::pair<float,float> pose2World(float robotX, float robotY, float robotAngle, float pointX, float pointY) {
  float worldX = cosf(robotAngle) * pointX - sinf(robotAngle) * pointY + robotX;
  float worldY = sinf(robotAngle) * pointX + cosf(robotAngle) * pointY + robotY;
  return std::make_pair(worldX, worldY);
}

int setObstacle(float xpos, float ypos, cv::Scalar &c)
{
  int i, j;
  int MX0 = MXSIZE / 2;
  int MY0 = MYSIZE / 2;

  i = MX0 + xpos * SCALE;
  j = MY0 + ypos * SCALE;
  if (i >= 0 && i < MXSIZE && j >= 0 && j < MYSIZE)
    circle(map, cv::Point(i, j), 0, c, 2, 8);
  return 1;
}

void keyJoystick()
{
  int c, old_c;
  using namespace std;
  initscr();
  crmode();
  keypad(stdscr, TRUE);
  noecho();
  clear();
  refresh();
  c = getch();

  for (;;)
  {

    switch (c)
    {
    case KEY_RIGHT:
      if (old_c == c)
        w = w - WINC;
      else
        w = 0; //-WINC;
      //printw("%s", "RIGHT key");
      break;
    case KEY_LEFT:
      if (old_c == c)
        w = w + WINC;
      else
        w = 0; //WINC;
      //printw("%s", "LEFT key");
      break;
    case KEY_UP:
      v = v + VINC;
      w = 0;
      //printw("%s", "UP key");
      break;
    case KEY_DOWN:
      v = v - VINC;
      w = 0;
      //printw("%s", "DOWN key");
      break;
    default:
      v = 0;
      w = 0;
      //printw("Unmatched - %d", c);
      break;
    }
    if (w > WMAX)
      w = WMAX;
    if (w < -WMAX)
      w = -WMAX;
    if (v > VMAX)
      v = VMAX;
    if (v < -VMAX)
      v = -VMAX;
    //cout << endl << "Vel: " << v << "Rot: " << w << endl;
    //cout << endl << "Pose: " << rx << ", "<< ry << ", " << rtheta << endl;
    old_c = c;
    refresh();
    c = getch();
  }
}

void oztopoakDeitu()
{
  int i;
  int st = 0; // Mean
  int secCount = 3;
  int sideSecCount = 1, forwardSecCount = 1;
  try
  {
    using namespace PlayerCc;

    // Sortu bezeroa eta konektatu zerbitzariarekin.
    PlayerClient bezeroa("localhost", 6665);
    // Sortu laser interfazea eta harpidetu bezeroarekin
    LaserProxy laserra(&bezeroa, 0);
    // Sortu position2d interfazea eta harpidetu bezeroarekin
    Position2dProxy robota(&bezeroa, 0);


    robota.SetMotorEnable(true);

    for (i = 0; i < 10; i++)
      bezeroa.Read();


    int count = laserra.GetCount();

    int readingsPerSection = int(count/secCount);
    double sections[secCount][readingsPerSection];
    bool emergency = false;
    double left = 0.0, right = 0.0, forward = 0.0, angular = 0.0, sleepTime = 0.1;


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

      if (!emergency) {
        left = 0.0;
        right = 0.0;
      }

      for (int i = 0; i < secCount; i++) {
        if (!emergency && i < sideSecCount) left += statistics[i][st];
        else if (i >= sideSecCount && i < sideSecCount + forwardSecCount) forward += statistics[i][st];
        else if (!emergency && i >= sideSecCount + forwardSecCount) right += statistics[i][st];
      }

      left /= sideSecCount;
      right /= sideSecCount;
      forward /= forwardSecCount;

      if (forward < 1.0 && !emergency) {
        forward = 0.0;
        if (left > right) {
          left = 6; // When divided by 20 = 0.3 rad/s
          right = 0.0;
        } else {
          right = 6; // When divided by 20 = 0.3 rad/s
          left = 0.0;
        }
        emergency = true;
        printf("Emergency stop!\n");
      } else if (emergency) {
        if (forward < 1.0) forward = 0.0;
        else emergency = false;
      } 

      forward /= 50;
      forward = (forward < MIN_LINEAR) ? MIN_LINEAR : (MAX_LINEAR < forward) ? MAX_LINEAR : forward;
      angular = (right - left) / 10;
      angular = (angular < MIN_ANGULAR) ? MIN_ANGULAR : (MAX_ANGULAR < angular) ? MAX_ANGULAR : angular;

      printf("Forward: %.2f\tAngular: %.2f\n", forward, angular);
      robota.SetSpeed(forward, angular);
      if (emergency) sleepTime = 2.6;
      else sleepTime = 0.1;

      sleep(sleepTime);
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
  }
}

void laserMapping()
{
  int i;
  float lx, ly;

  cv::namedWindow("MAP", CV_WINDOW_AUTOSIZE);

  try
  {
    using namespace PlayerCc;

    PlayerClient robotClient(gHostname, mPort);
    LaserProxy sick(&robotClient, lIndex);
    Position2dProxy robot(&robotClient, mIndex);
    robot.SetMotorEnable(true);
    std::pair<float,float> worldCoords;
    float pointX = 0.0, pointY = 0.0, savedX = 0.0, savedY = 0.0, savedYaw = 0.0;
    bool isStalled = false;

    for (i = 0; i < 10; i++)
      robotClient.Read();

    for (;;)
    {
      robotClient.Read();
      robot.SetSpeed(v, w);
      /* Robotaren posizioa munduan odometriaren arabera */
      rx = robot.GetXPos();
      ry = robot.GetYPos();
      rtheta = robot.GetYaw();

      if (robot.GetStall()) {
        robot.SetSpeed(0,0);
        if (!isStalled) {
          savedX = rx;
          savedY = ry;
          savedYaw = rtheta;
          isStalled = true;
        }
        continue;
      } else if (isStalled) {
        isStalled = false;
        robot.SetOdometry(savedX, savedY, savedYaw);
        rx = savedX;
        ry = savedY;
        rtheta = savedYaw;
      }

      /* Irudikatu robotaren posizioa mapan */
      setObstacle(rx, -ry, color0);
      /* Laserraren irakurketak proiektatu behar dira munduan */
      
      for (i = 0; i < int(sick.GetCount()); i++)
      {
        if (sick.GetRange(i) < sick.GetMaxRange())
        {
          pointX = sick.GetRange(i) * cosf(sick.GetBearing(i));
          pointY = sick.GetRange(i) * sinf(sick.GetBearing(i));
          worldCoords = pose2World(rx, ry, rtheta, pointX, pointY);
          lx = worldCoords.first;
          ly = worldCoords.second;
          // Set the obstacle in the map
          setObstacle(lx, -ly, color1);
        }
      }
      usleep(100000);
      /* Mapa bistaratu */
      cv::imshow("MAP", map);
      cv::waitKey(1);
    }
  }
  catch (PlayerCc::PlayerError &e)
  {
    std::cerr << e << std::endl;
  }
}

void closeAll(int signum)
{
  std::cout << "Interrupt signal (" << signum << ") received\n";
  cv::imwrite("mapa.png", map);
  exit(signum);
}

int main(int argc, char **argv)
{
  signal(SIGINT, closeAll);
  //parse_args(argc, argv);
  bool avoidObstacles = false;
  std::thread th1;

 if (argc != 1) {
    std::string currentArg(argv[1]);
    std::transform(currentArg.begin(), currentArg.end(), currentArg.begin(), ::tolower);

    if ((currentArg.compare("-o") == 0)) {
      avoidObstacles = true;
    } else if ((currentArg.compare("-k")) == 0) {
      avoidObstacles = false;
    } else {
      fprintf(stderr, "[ERROR] Unrecognized Command-Line argument.\n");
      exit(1);
    }
  } 

  if (avoidObstacles) th1 = std::thread(oztopoakDeitu);
  else th1 = std::thread(keyJoystick);

  std::thread th2(laserMapping);

  th1.detach();
  th2.detach();

  std::cout << "Exiting main..." << std::endl;
  while (1)
  {
    usleep(1000000);
  }
  return 0;
}