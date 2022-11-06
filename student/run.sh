#!/bin/bash

# Authors:
# 102536 Leonardo Almeida
# 102778 Pedro Rodrigues

function main()
{
    # check args
    if [[ $1 == "-h" ]];
    then
        echo "Usage: ./run.sh [options]"
        echo "Options:"
        echo "  -h  Show this help message and exit"
        echo "  -m  Play manually"
        echo "  -v  Play without viewer"
        echo "  -t  Play with theoretical keys calculated"
        # echo "  -e  Play extreme mode"
        exit 0
    fi

    # activate the virtual environment
    source venv/bin/activate

    # delete highscores file
    rm -f ./highscores.json

    # run the game
    play $1 >/dev/null 2>&1
}

function play()
{
    # play manually
    if [[ $1 == "-m" ]]
    then
        gnome-terminal \
        --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
        --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
        --tab -t "Client" -e "bash -c 'python3 client.py; exec bash'" 
        exit 0
    fi

    # play without viewer
    if [[ $1 == "-v" ]]
    then
        gnome-terminal \
        --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
        --tab -t "Student" -e "bash -c 'sleep 1; python3 student.py; exec bash'" --active
        exit 0
    fi

    # play with theoretical keys calculated
    if [[ $1 == "-t" ]]
    then
        gnome-terminal \
        --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
        --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
        --tab -t "Client" -e "bash -c 'sleep 1; python3 tests/theoretical_max.py; exec bash'" 
        exit 0
    fi

    # play extreme mode
    # if [[ $1 == "-e" ]]
    # then
    #     gnome-terminal \
    #     --tab -t "Server" -e "bash -c 'python3 ./mods/server2.py; exec bash'" \
    #     --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
    #     --tab -t "Student" -e "bash -c 'sleep 1; python3 student.py; exec bash'" --active
    #     exit 0
    # fi

    # play normally
    gnome-terminal \
    --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
    --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
    --tab -t "Student" -e "bash -c 'sleep 1; python3 student.py; exec bash'" --active
    exit 0
}

main "$@"