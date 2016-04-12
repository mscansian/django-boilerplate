#!/bin/bash

PROJECT_DIR=$1
if [ "$2" == "--pretty" ]; then
    COMMAND="lessc"
    OPTIONS=""
    EXTENSION="css"
elif [ "$2" == "--clean" ]; then
    COMMAND="rm"
else
    COMMAND="lessc"
    OPTIONS="--clean-css"
    EXTENSION="min.css"
fi

compile_css() {
    if [ "$COMMAND" == "lessc" ]; then
        lessc $OPTIONS $1.less $1.$EXTENSION
    elif [ "$COMMAND" == "rm" ]; then
        rm -f $1.css
        rm -f $1.min.css
    fi
}

#compile_css $PROJECT_DIR/apps/example/static/css/main
