#!/bin/bash

echo $#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
. $SCRIPT_DIR/functions.sh

#######
# Main
#######

WORKING_ROOT_DIR=`pwd`

# modules=( "hello" "world" )
# modules=$(find modules/ -name Dockerfile -exec dirname {} \;)
MODULE_LIST_FILE=${MODULE_LIST_FILE:-$SCRIPT_DIR/modules.rebuild}
echo "Loading module file : '$MODULE_LIST_FILE'"
modules=$(cat $MODULE_LIST_FILE)

for i in ${modules[@]}; do
    build_module_locally $i
done

rm -rf ./build/

