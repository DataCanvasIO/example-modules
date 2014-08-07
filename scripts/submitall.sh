#!/bin/bash

USERNAME=$1
PASSWORD=$2
SPEC_SERVER=$3

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

echo $#
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 username password spec_server"
    exit
fi

. $SCRIPT_DIR/functions.sh

#######
# Main
#######
login_spec_server

# modules=( "hello" "world" )
# modules=$(find modules/ -name Dockerfile -exec dirname {} \;)

WORKING_ROOT_DIR=`pwd`

MODULE_LIST_FILE=${MODULE_LIST_FILE:-$SCRIPT_DIR/modules}
echo "Loading module file : '$MODULE_LIST_FILE'"
modules=$(cat $MODULE_LIST_FILE)

for i in ${modules[@]}; do
    submit_module $i
done

rm -rf ./build/

