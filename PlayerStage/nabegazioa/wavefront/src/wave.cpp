#include <libplayerc++/playerc++.h>
#include <iostream>
#include <unistd.h>

int 
main(int argc, char **argv)
{
  float x, y, a;
  int i, gc;
  int oldgc;
  float helb[6][3] = {{4, 4, 0},{4, -1.5, 0},{-4.5, -3.5, 0},
		       {4.5, 2, 0},{-4, 3, 0},
		       {4, 4, 0}};

  try
  {
    using namespace PlayerCc;

    // Sortu bezeroa eta konektatu zerbitzariarekin.
    PlayerClient bezeroa("localhost", 6666);
    // Sortu laser interfazea eta harpidetu bezeroarekin
    PlannerProxy planifikatzailea(&bezeroa, 1);
    // Sortu position2d interfazea eta harpidetu bezeroarekin

    gc = 0;
    oldgc = -1;
    while (gc < 6)
      {
	bezeroa.Read();
	if (oldgc != gc)
	  {
	    x = helb[gc][0];
	    y = helb[gc][1];
	    a = DTOR(helb[gc][2]);
	    fprintf(stdout, "Helburu berria: %d (%f %f %f)\n",
		    gc, x, y, a);
	    planifikatzailea.SetGoalPose(x, y, a);
	    usleep(2000000);
	    for (i = 0; i < 20; i++)
	      bezeroa.Read();
	    if (!planifikatzailea.GetPathValid())
	      {
		fprintf(stdout, "Helburua ez da atzigarria.\n");
		oldgc = gc;
		gc ++;
	      }
	    else
	      {
		fprintf(stdout, 
			"Helburua zilegizkoa da. Helburu zenbakia = %d\n", gc);
		oldgc = gc;
	      }
	  }
	if (planifikatzailea.GetPathDone())
	  {
	    fprintf(stdout, 
		    "ROBOTA %d. HELBURUAN: Robotaren posea: %f %f %f Helburua: %f %f %f\n", 
		    gc,
		    planifikatzailea.GetPose().px, planifikatzailea.GetPose().py, 
		    RTOD(planifikatzailea.GetPose().pa),
		    planifikatzailea.GetGx(), 
		    planifikatzailea.GetGy(), 
		    RTOD(planifikatzailea.GetGa()));
	    oldgc = gc;
	    gc ++;
	  
	  }
      }
  }
  catch (PlayerCc::PlayerError & e)
    {
      std::cerr << e << std::endl;
      return -1;
    }
  
}


