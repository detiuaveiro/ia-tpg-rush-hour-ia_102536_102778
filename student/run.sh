#!/bin/bash

function main()
{
    # check args
    if [[ $1 == "-h" ]];
    then
        echo "Usage: ./run.sh [options]"
        echo "Options:"
        echo "  -h  Show this help message and exit"
        echo "  -v  Remove viewer"
        echo "  -m  Play manually"
        exit 1
    fi

    # activate the virtual environment
    source venv/bin/activate

    if [[ $1 == "-v" ]]
    then
        gnome-terminal \
        --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
        --tab -t "Student" -e "bash -c 'python3 student.py; exec bash'"\
        --active
        exit 0
    fi

    if [[ $1 == "-m" ]]
    then
        gnome-terminal \
        --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
        --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
        --tab -t "Client" -e "bash -c 'python3 client.py; exec bash'"
        exit 0
    fi

    gnome-terminal \
    --tab -t "Server" -e "bash -c 'python3 server.py; exec bash'" \
    --tab -t "Viewer" -e "bash -c 'python3 viewer.py; exec bash'" \
    --tab -t "Student" -e "bash -c 'python3 student.py; exec bash'" \
    --active
    
}

main "$@"