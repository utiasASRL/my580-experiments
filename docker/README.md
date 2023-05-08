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
