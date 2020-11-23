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
  if ((i >= 0 && i < MXSIZE) && (j >= 0 && j < MYSIZE))
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

void oztopoakDeitu(int argc, char **args)
{
  char *callString;

  for (int i = 2; i < argc; i++) {
    asprintf(&callString, "%s %s", callString, args[i]);
  }

  asprintf(&callString, "../../oekidin/build/oztopoakEkidin%s", callString);
  system(callString);
  free(callString);
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

  if (avoidObstacles) th1 = std::thread(oztopoakDeitu, argc, argv);
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