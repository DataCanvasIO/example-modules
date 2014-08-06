#!/bin/bash

echo $#

prebuild() {
    [[ -x ./prebuild.sh ]] && ./prebuild.sh
    true
}

build_module() {
    local dir=$1

    [[ -d "$1" ]] && \
        cd "$1" && \
        prebuild && \
        echo "$2!!!!!!!!!"
        sudo docker build --no-cache=true -t $2 ./
    if [ $? -eq 0 ]; then
        cd $WORKING_ROOT_DIR
    else
        cd $WORKING_ROOT_DIR
        exit 3
    fi
}

#######
# Main
#######

# modules=( "hello" "world" )
# modules=$(find modules/ -name Dockerfile -exec dirname {} \;)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
WORKING_ROOT_DIR=`pwd`

MODULE_LIST_FILE=${MODULE_LIST_FILE:-$SCRIPT_DIR/modules.rebuild}
echo "Loading module file : '$MODULE_LIST_FILE'"
modules=$(cat $MODULE_LIST_FILE)
DOCKER_REGISTRY="127.0.0.1:5000"
DOCKER_USER="admin"
for i in ${modules[@]}; do
    echo "building module at : $i"
    rm -rf ./build/
    cp -Lrfp $i ./build
    module_dirname=$(basename $i)
    module_version=$( cat $i/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
    echo "build $module_dirname version=$module_version ==> $module_tag_with_version"
    build_module ./build $module_tag_with_version
    sudo docker push $module_tag
done

rm -rf ./build/

