#!/usr/bin/env bash
kill -9 $(cat /tmp/crontab_runner_pid); sleep 0.2 && sudo nice -n -10 su pi ~/Tornadoscope_show/crontab_runner.sh