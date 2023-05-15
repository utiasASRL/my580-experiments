# Dataset collection May 2023

## Dataset collection Wednesday May 10

All dataset taken by Connor carrying rig, Frederike following with laptop.

Test round: 2023-05-10-T10-20
=============================
first dataset, which revealed a lot of issues such as
- not all vsk files have zero as origin
- camera tansform ill defined


First round: 2023-05-10-T16-XX
==============================

- loop2d: 3 loops of roughly same height, slowly
- loop2d fast: " " ", fast
- loop2d-fast-v2: changed to facing down more
from somewhere here didn't restart the nodes
- loop2d-v2: also facing down more
- loop3d: two loops, with circular egomotion
- loop3d-v2: three loops, without circular egomotion

Did a few tests with anchors 6 which was bad, in the end we swtiched 6 and 12 and noticed that 6 was still bad, so it was actually tag-dependent. 

Second round: 2023-05-10-T18-25-XXXX
====================================

- loop2d-v3: same as before but everything on a higher stick.
- loop-2d-fast-v3: " " " 
- loop-3d-v3: " " "
- zigzag: first round of zig-zag dataset (on stick)
- eight: first round of eight dataset (on stick) 

observations from second round: probably a lot of nlos for tag10
tag6 got tilted a little bit throughout these experiments (only noticed in the end)

## Dataset collection Thursday May 11

- Redid Mocap calibration, noticed cam 7 is faulty, so disabled it. 
- Moved a lot of landmarks and also placed anchor 9 on a plastic mount.
- Switched to setup with one tag only

All datasets taken by Mohammed carrying rig, Frederike following with laptop.

First round: 2023-05-11-T16-16-XXXX
===================================
-loop-2d-1tag: walked clockwise instead of counter-clockwise (so probably not seeing many apriltags).
-loop-2d-1tag-v2: switched to clockwise
-loop-2d-fast-1tag: " " "
-loop-3d-1tag: " " "
-zigzag-1tag: " " "
-eight-1tag: UWB crashed, no data
-eight-1tag-v2: everything okay

Jackal experiments: 2023-05-11-T18-25-jackal-XXX
================================================
- loop: no UWB data, but camera data okay, have video. Teach step, pause for 2 minutes, then 3 loops.
- loop-v2: all data recorded, no video. Repeat step: 2.5 loops, then VTR crashed because out of memory.
- zigzag: all data recorded (manual drive) and video stopped after 30 seconds.

## Dataset collection Friday May 12

Extra NLOS / z-var experiments: 2023-05-12-T11-20-XXX
=====================================================
- loop-2d-tag1-nlos: no UWB measurements
- loop-2d-tag1-nlos-v2: no mocap measurements
- loop-2d-tag1-nlos-v3: all good, but not great nlos
- grid: go on a grid of 8 fixed positions, always facing in direciton of big glass Wall.
- ell: go on ell with large z motion, always facing directions with lots of apriltags
- loop-3d: loop3d with lots of vertical motion
tag 32 moved a bit after loop3d, moved it back manually using mocap as guide
- human-nlos: Static position, with Mohammed standing in the line of sight of one anchor
- apriltag: slow apriltag dataset where we make sure we definitely see all 

Decawave experiments: 2023-05-12-T16-00-decawave
================================================
- decawave: loop with Decawave by Connor
- decawave-v2: loop with Decawave by Joey
- dwm-loop-3d-v2: standard dataset with more complex motion
- dwm-loop-3d-v3: dataset with a lot of motion above and below the anchors plane
