# Scripts to easily run experiments

## Cheatsheet

Running sessions:
- run experiment: `./tmux-setup.sh`
- detach from session: Ctrl+L d
- list current sessions: `tmux list-sessions`
- kill session: `tmux kill-session -t my580`

Pushing things to docker:
- list images: docker images
- sudo docker tag some-image-from-list:some-version docker-username:release-name
- sudo docker push docker-username:release-name


To get UWB running: 
- `sudo chmod 666 /dev/ttyACM1` # or whatever port is being used
- putty # wait until connected, then run `les`
- close putty session
- run python distancemeasurer.py
