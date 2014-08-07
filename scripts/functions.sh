#!/bin/bash

#
# Global variables required:
#   - USERNAME
#   - PASSWORD
#   - SPEC_SERVER
#   - WORKING_ROOT_DIR
#   - DOCKER_REGISTRY (optional)
#   - DOCKER_USER     (optional)
#

show_info() {
    local original_dir=$1
    module_dirname=$(basename $original_dir)
    module_version=$( cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
}

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

screwjack_submit() {
    if [[ -f ./.meta.json ]]
    then
        local ret=$(jq ".templateType" ./.meta.json)
        templateType=${ret//null/none}
        screwjack --username=$USERNAME --spec_server=$SPEC_SERVER submit --templateType=$templateType
    else
        screwjack --username=$USERNAME --spec_server=$SPEC_SERVER submit
    fi
}

submit_module() {

    if [[ -z "$1" ]]
    then
        echo "Usage: submit_module original_module_dir"
        exit
    fi

    local original_dir=$1
    local dir=./build/

    echo "Submitting module at : $original_dir"
    rm -rf $dir
    cp -Lrfp $original_dir $dir
    local module_dirname=$(basename $original_dir)
    local module_version=$( cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
    echo "submit $module_dirname version=$module_version ==> $module_tag_with_version"

    [[ -d "$dir" ]] && \
        cd "$dir" && \
        prebuild && \
        screwjack_submit
    if [ $? -eq 0 ]; then
        cd $WORKING_ROOT_DIR
    else
        cd $WORKING_ROOT_DIR
        exit 3
    fi
}

submit_import_module() {

    if [[ -z "$1" ]]
    then
        echo "Usage: submit_import_module original_module_dir"
        exit
    fi

    local original_dir=$1
    local dir=./build/

    echo "Submit-Import module at : $original_dir"
    rm -rf $dir
    cp -Lrfp $original_dir $dir
    local module_dirname=$(basename $original_dir)
    local module_version=$( cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
    echo "submit $module_dirname version=$module_version ==> $module_tag_with_version"

    [[ -d "$dir" ]] && \
        cd "$dir" && \
        prebuild && \
        screwjack --username=$USERNAME --spec_server=$SPEC_SERVER submit_import
    if [ $? -eq 0 ]; then
        cd $WORKING_ROOT_DIR
    else
        cd $WORKING_ROOT_DIR
        exit 3
    fi
}

build_module_locally() {

    if [[ -z "$1" ]]
    then
        echo "Usage: build_module_locally original_module_dir"
        exit
    fi

    local DOCKER_REGISTRY="127.0.0.1:5000"
    local DOCKER_USER="admin"
    local original_dir=$1
    local dir=./build/

    rm -rf $dir
    cp -Lrfp $original_dir $dir

    local module_dirname=$(basename $original_dir)
    local module_version=$( cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]')
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_dirname:$module_version"
    echo "build $module_dirname version=$module_version ==> $module_tag_with_version"

    [[ -d "$dir" ]] && \
        cd "$dir" && \
        prebuild && \
        sudo docker build --no-cache=true -t $module_tag_with_version ./ && \
        sudo docker push $module_tag
    if [ $? -eq 0 ]; then
        cd $WORKING_ROOT_DIR
    else
        cd $WORKING_ROOT_DIR
        exit 3
    fi
}


