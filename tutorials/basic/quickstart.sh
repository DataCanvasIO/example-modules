#!/bin/bash

echo "This is not a script to run. Please read this script"
exit


readonly MODULE_NAME=SVM
readonly MODULE_USERNAME=your_username
readonly MODULE_PATH=${MODULE_USERNAME,,}/${MODULE_NAME,,}

echo $MODULE_NAME
echo $MODULE_USERNAME
echo $MODULE_PATH

# initialize a module
screwjack init basic -n $MODULE_NAME -d "A simple SVM" -v "0.1" -c "python main.py" -b "zetdata/sci-python:2.7"

# change directory into the module
cd ${MODULE_NAME,,}

# Add param/input/output
screwjack param_add C float
screwjack input_add X csv
screwjack input_add Y csv
screwjack output_add MODEL model.dummy

# Test in local
screwjack --username=$MODULE_USERNAME run local --param-C=0.1 --X=iris_X.csv --Y=iris_Y.csv --MODEL=tmp.model

# Test in docker
screwjack --username=$MODULE_USERNAME run docker --param-C=0.1 --X=iris_X.csv --Y=iris_Y.csv --MODEL=tmp.model

# Clean up
docker rm $(docker ps -aq)
docker rmi $(docker inspect -f "{{ .id }}" $MODULE_PATH)
