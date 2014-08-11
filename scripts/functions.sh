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

get_module_version() {
    local original_dir=$1
    cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Version"]'
}

get_module_name() {
    local original_dir=$1
    cat $original_dir/spec.json | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["Name"]'
}

get_module_docker_name() {
    local original_dir=$1
    cat $original_dir/spec.json | python -c 'import json,sys,re;obj=json.load(sys.stdin);print re.sub(r"\s+", "_", obj["Name"].lower())'
}

get_module_docker_tag() {
    local original_dir=$1
    cat $original_dir/spec.json | python -c 'import json,sys,re;obj=json.load(sys.stdin);print re.sub(r"\s+", "_", obj["Name"].lower())'
}

get_module_docker_tagv() {
    local original_dir=$1
    cat $original_dir/spec.json | python -c 'import json,sys,re;obj=json.load(sys.stdin);print "%s:%s" % (re.sub(r"\s+", "_", obj["Name"].lower()), obj["Version"])'
}

show_info() {
    local original_dir=$1
    local module_name=$(get_module_docker_name $original_dir)
    local module_version=$(get_module_version $original_dir)
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_name"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_name:$module_version"
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
    local module_name=$(get_module_docker_name $original_dir)
    local module_version=$(get_module_version $original_dir)
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_name"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_name:$module_version"
    echo "submit $module_name version=$module_version ==> $module_tag_with_version"

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
    local module_name=$(get_module_docker_name $original_dir)
    local module_version=$(get_module_version $original_dir)
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_name"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_name:$module_version"
    echo "submit_import $module_name version=$module_version ==> $module_tag_with_version"

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

    local module_name=$(get_module_docker_name $original_dir)
    local module_version=$(get_module_version $original_dir)
    local module_tag="$DOCKER_REGISTRY/$DOCKER_USER/$module_name"
    local module_tag_with_version="$DOCKER_REGISTRY/$DOCKER_USER/$module_name:$module_version"
    echo "build $module_name version=$module_version ==> $module_tag_with_version"

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


