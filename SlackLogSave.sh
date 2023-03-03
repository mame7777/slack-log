#!bin/bash

COMMAND="source /home/mame77/workspace/slack-log/env/bin/activate"
eval $COMMAND

COMMAND="/home/mame77/workspace/slack-log/env/bin/python3 /home/mame77/workspace/slack-log/codes/main.py"
eval $COMMAND

COMMAND="deactivate"
eval $COMMAND
