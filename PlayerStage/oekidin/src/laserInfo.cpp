#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <libplayerc++/playerc++.h>
#include <iostream>

int
main(int argc, const char **argv)
{
  int i;  

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
    
    robota.SetMotorEnable (true);

    for (i = 0; i < 10; i++)
      bezeroa.Read();

    
    int count = laserra.GetCount();
    
    std::cout << "Scan count: "  <<  count << std::endl;    
    std::cout << "Scan resolution: "  <<  laserra.GetScanRes() << std::endl;
    std::cout << "Range resolution: " <<  laserra.GetRangeRes() << std::endl;
    std::cout << "Max Range: " <<  laserra.GetMaxRange() << std::endl;
    std::cout << "Max angle: " <<  laserra.GetMaxAngle() << std::endl;
    std::cout << "Min angle: " <<  laserra.GetMinAngle() << std::endl;

    std::cout << "Bearings: " << std::endl;
    for (i = 0; i < count; i++)
      {
	std::cout << laserra.GetBearing(i) << ", ";
      }
    std::cout << "-----------------------------------" << std::endl;


    while (1)
      { 
	float max = -1.0;
	float min = laserra.GetMaxRange();
	int maxind = -1;
	int minind = -1;
	bezeroa.Read();
	for (i = 0; i < count; i++)
	  {
	    if (laserra.GetRange(i) > max && laserra.GetRange(i) != laserra.GetMaxRange())
	      {
		max = laserra.GetRange(i);
		maxind = i;
	      }
	    if (laserra.GetRange(i) < min)
	      {
		min = laserra.GetRange(i);
		minind = i;
	      }
	  }
	// Print info
	
	std::cout << "Max Reading: " <<  max << " Index:" << maxind << std::endl;
	std::cout << "Min Reading: " <<  min << " Index:" << minind << std::endl;
	std::cout << "-----------------------------------" << std::endl;
	// robota.SetSpeed(0, 0.2);
      }
  }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return -1;
    }
    
}




