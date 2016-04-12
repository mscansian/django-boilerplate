#!/bin/bash

PROJECT_DIR=$1
if [ "$2" == "--clean" ]; then
    COMMAND="rm"
else
    COMMAND="closure-compiler"
fi

compile_js() {
    if [ "$COMMAND" == "closure-compiler" ]; then
        closure-compiler --js $1.js --js_output_file $1.min.js
    elif [ "$COMMAND" == "rm" ]; then
        rm -f $1.min.js
    fi
}

#compile_js $PROJECT_DIR/apps/example/static/js/plugins
