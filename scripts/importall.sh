#!/bin/bash

USERNAME=$1
PASSWORD=$2
SPEC_SERVER=$3

echo $#
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 username password spec_server"
    exit
fi

login_spec_server() {
    screwjack --username=$USERNAME --spec_server=$SPEC_SERVER login --password=$PASSWORD
    if [ $? -eq 0 ]; then
        echo "Login successfully"
    else
        echo "Login failed"
        exit 2
    fi
}

prebuild() {
    [[ -x ./prebuild.sh ]] && ./prebuild.sh
    true
}

submit_module() {
    local dir=$1

    [[ -d "$1" ]] && \
        cd "$1" && \
        prebuild && \
        screwjack --username=$USERNAME --spec_server=$SPEC_SERVER submit_import
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
login_spec_server

# modules=( "hello" "world" )
# modules=$(find modules/ -name Dockerfile -exec dirname {} \;)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
WORKING_ROOT_DIR=`pwd`

MODULE_LIST_FILE=${MODULE_LIST_FILE:-$SCRIPT_DIR/modules}
echo "Loading module file : '$MODULE_LIST_FILE'"
modules=$(cat $MODULE_LIST_FILE)

for i in ${modules[@]}; do
    echo "Submitting module at : $i"
    rm -rf ./build/
    cp -Lrfp $i ./build
    module_dirname=$(basename $i)
    module_version=$( cat $i/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
    echo "submit $module_dirname version=$module_version ==> $module_tag_with_version"
    submit_module ./build
done

rm -rf ./build/

