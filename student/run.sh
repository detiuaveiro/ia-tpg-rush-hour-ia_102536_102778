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
        gnome-terminal --tab --title="Server" --command="bash -c 'python3 server.py; exec bash'" \
        --tab --title="Student" --command="bash -c 'python3 student.py; exec bash'"
        exit 0
    fi

    if [[ $1 == "-m" ]]
    then
        gnome-terminal --tab --title="Server" --command="bash -c 'python3 server.py; exec bash'" \
        --tab --title="Viewer" --command="bash -c 'python3 viewer.py; exec bash'" \
        --tab --title="Client" --command="bash -c 'python3 client.py; exec bash'"
        exit 0
    fi

    gnome-terminal --tab --title="Server" --command="bash -c 'python3 server.py; exec bash'" \
    --tab --title="Viewer" --command="bash -c 'python3 viewer.py; exec bash'" \
    --tab --title="Student" --command="bash -c 'python3 student.py; exec bash'"
    

}

main "$@"