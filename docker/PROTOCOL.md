# Dataset collection Wednesday May 10

Notes of anything important that happened during data collection.

first round
===========

- loop2d 
- loop2d fast
changed to facing down more
- loop2d-fast-v2
from somewhere here didn't restart the nodes
- loop2d-v2
- loop3d (two loops, with circular egomotion)
- loop3d-v2 (three loops, without circular egomotion)

testing
========
did a few tests with anchors 6 which was bad, in the end we swtiched 6 and 12 and noticed that 6 was still bad, so it was actually tag-dependent. 

second round
============
then recorded loop2d-v3 again, with everything on a higher stick.
same for other datasets with v3. 
also recorded zigzag and eight for the first time. 

observations from second round: probably a lot of nlos for tag10
tag6 tilted a little bit

# Dataset collection Thursday May 11

- Redid Mocap calibration, noticed cam 7 is faulty, so disabled it. 
- Moved a lot of landmarks and also placed anchor 9 on a plastic mount.

-loop-2d-1tag: walked clockwise instead of counter-clockwise (so probably not seeing many apriltags)
-loop-2d-ttag-v2: clockwise
-...
-first eight: UWB crashed, no data
-eight-v2: with UWB

Jackal: 
- loop: no UWB data, but camera data okay, have video. Teach step, pause for 2 minutes, then 3 loops.
- loop-v2: all data recorded, no video. Repeat step: 2.5 loops, then VTR crashed because out of memory. 
- zigzag: all data recorded (manual drive) and video stopped after 30 seconds.

# Dataset collection Friday May 12

- loop2d-tag1-nlos: no UWB
- loop2d-tag1-nlos-v2: no mocap
- loop2d-tag1-nlos-v3: all good, but not great nlos
- grid
- ell
- loop-3d
- nlos2

tag 32 moved a bit after loop3d, moved it back manually using mocap as guide
- all other experiments went smoothly

after lunch: replace UWB markers with Decawave ones
