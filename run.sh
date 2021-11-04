#!bin/bash
tmux new-session -d -s 0
tmux send-keys -t 0 "cd /home/www/buddhachess" C-m
sleep 2
tmux send-keys -t 0 "source ./.venv/bin/activate" C-m
sleep 8
tmux send-keys -t 0 "poetry update" C-m
sleep 15
tmux send-keys -t 0 "uvicorn app.main:app --reload --workers 4" C-m