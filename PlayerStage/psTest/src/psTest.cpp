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
   
    while (1)
      { 
	bezeroa.Read();
	for (i = 0; i < count; i++)
	  {
	    std::cout << laserra.GetRange(i) << ", ";
	  }
	std::cout << "-----------------------------------" << std::endl;
	robota.SetSpeed(0, 0.2);
      }
  }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return -1;
    }
    
}




