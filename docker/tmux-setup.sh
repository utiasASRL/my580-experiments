#!/bin/bash

session="ros2-record"

tmux new-session -d -s $session

window=0
tmux rename-window -t $session:$window 'bag'
tmux send-keys -t $session:$window 'make run-bag-record' C-m

window=1
tmux new-window -t $session:$window -n 'zed2'
tmux send-keys -t $session:$window 'make run-zed2' C-m

window=2
tmux new-window -t $session:$window -n 'vicon'
tmux send-keys -t $session:$window 'make run-vicon' C-m

window=3
tmux new-window -t $session:$window -n 'rviz'
tmux send-keys -t $session:$window 'make run-rviz' C-m


tmux attach-session -t $session
