#!/bin/bash

session="my580"

tmux new-session -d -s $session

window=0
tmux rename-window -t $session:$window 'zed2'
tmux send-keys -t $session:$window 'make run-zed2' C-m

tmux split-window -v 
tmux send-keys -t $session:$window 'make run-vicon' C-m

tmux split-window -h
tmux send-keys -t $session:$window 'make run-uwb' C-m

# background window: do not need to look at this much
window=1
tmux new-window -t $session:$window -n 'background'
tmux send-keys -t $session:$window 'make run-rviz' C-m

# last: start recording bag file.
tmux split-window -v 
tmux send-keys -t $session:$window 'make run-bag-record' C-m

tmux attach-session -t $session
