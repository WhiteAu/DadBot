#!/bin/bash

source /app/Lmod/lmod/lmod/init/bash

virtualenv dadbotenv

source ./databotenv/bin/activate

pip install slackclient 

