#include <cstdlib>
#include <cstring>
#include <libplayerc++/playerc++.h>
#include <iostream>
#if !defined(WIN32) || defined(__MINGW32__)
#include <unistd.h>
#endif
#if !HAVE_GETOPT
#include <replace.h>
#endif

std::string gHostname(PlayerCc::PLAYER_HOSTNAME);
uint32_t mPort(PlayerCc::PLAYER_PORTNUM);
uint32_t lPort(PlayerCc::PLAYER_PORTNUM + 1);
uint32_t lIndex(0);
uint32_t mIndex(0);
uint32_t gDebug(0);
uint32_t gFrequency(10); // Hz
uint32_t gDataMode(PLAYER_DATAMODE_PUSH);
bool gUseLaser(false);
std::string outFile;

void print_usage(int argc, char **argv);

int parse_args(int argc, char **argv)
{
     // set the flags
     const char *optflags = "h:mp:lp:mi:li:d:u:lm:";
     int ch;

     // use getopt to parse the flags
     while (-1 != (ch = getopt(argc, argv, optflags)))
     {
          switch (ch)
          {
               // case values must match long_options
          case 'h': // hostname
               gHostname = optarg;
               break;
          case 'mp': // port
               mPort = atoi(optarg);
               break;
          case 'lp': // port
               lPort = atoi(optarg);
               break;
          case 'mi': // index
               mIndex = atoi(optarg);
               break;
          case 'li': // index
               lIndex = atoi(optarg);
               break;
          case 'd': // debug
               gDebug = atoi(optarg);
               break;
          case 'u': // update rate
               gFrequency = atoi(optarg);
               break;
          case 'm': // datamode
               gDataMode = atoi(optarg);
               break;
          case 'l': // datamode
               gUseLaser = true;
               break;
          case 'of': //output datafile
               outFile = optarg;
               break;
          case '?': // help
          case ':':
          default: // unknown
               print_usage(argc, argv);
               exit(-1);
          }
     }

     return (0);
} // end parse_args

void print_usage(int argc, char **argv)
{
     using namespace std;
     cerr << "USAGE:  " << *argv << " [options]" << endl
          << endl;
     cerr << "Where [options] can be:" << endl;
     cerr << "  -h <hostname>  : hostname to connect to (default: "
          << PlayerCc::PLAYER_HOSTNAME << ")" << endl;
     cerr << "  -p <port>      : port where Player will listen (default: "
          << PlayerCc::PLAYER_PORTNUM << ")" << endl;
     cerr << "  -i <index>     : device index (default: 0)"
          << endl;
     cerr << "  -d <level>     : debug message level (0 = none -- 9 = all)"
          << endl;
     cerr << "  -u <rate>      : set server update rate to <rate> in Hz"
          << endl;
     cerr << "  -l      : Use laser if applicable"
          << endl;
     cerr << "  -m <datamode>  : set server data delivery mode"
          << endl;
     cerr << "  -of <outputFilename>  : output file name"
          << endl;
     cerr << "                      PLAYER_DATAMODE_PUSH = "
          << PLAYER_DATAMODE_PUSH << endl;
     cerr << "                      PLAYER_DATAMODE_PULL = "
          << PLAYER_DATAMODE_PULL << endl;
} // end print_usage
