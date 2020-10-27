#include <libplayerc++/playerc++.h>
#include <iostream>

int
main(int argc, const char **argv)
{
  int i; 
  int xzentroa;

  try
  {
    using namespace PlayerCc;

    // Sortu bezeroa eta konektatu zerbitzariarekin.
    PlayerClient bezeroa("localhost", 6665);
    // Sortu blobfinder interfazea eta harpidetu bezeroarekin
    BlobfinderProxy blobfinderra(&bezeroa, 0);
    // Sortu position2d interfazea eta harpidetu bezeroarekin
    Position2dProxy robota(&bezeroa, 0);

    robota.SetMotorEnable (true);

    for (i = 0; i < 10; i++)
      bezeroa.Read();
    
    xzentroa = blobfinderra.GetWidth()/2;
    std::cout << "INFO: zabalera: " << blobfinderra.GetWidth()  << "  zentroa: " << xzentroa << std::endl;

    for (;;)
      {
	bezeroa.Read();
	int blobKop = blobfinderra.GetCount();
	std::cout << "Blob kopurua: " << blobKop << std::endl;

	if (blobKop != 0)
	  {
	    for (i = 0; i < blobKop; i++)
	      fprintf(stdout, "%d. BLOBarean kolorea: %d, azalera: %d, \
zentroidea: (%d, %d), zentrora distantzia: %f\n", 
		      i, blobfinderra.GetBlob(i).color,
		      abs(blobfinderra.GetBlob(i).area),
		      blobfinderra.GetBlob(i).x,
		      blobfinderra.GetBlob(i).y,
		      blobfinderra.GetBlob(i).range);
	    
	    robota.SetSpeed(0, 0);
	  }
	else
	  {
	    fprintf(stdout, 
		    "EZ DUT BLOB-IK IKUSTEN... biraka arituko naiz...\n");
	    robota.SetSpeed(0, 0.5);
	  }
      }
    
  }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return -1;
    }
  
}

