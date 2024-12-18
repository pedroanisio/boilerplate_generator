#!/bin/bash

# Define the base directory
BASE_DIR="."

# Create the main directory
mkdir -p $BASE_DIR

# Create the main file
touch $BASE_DIR/main.py

# Create subdirectories and files
mkdir -p $BASE_DIR/handlers
touch $BASE_DIR/handlers/__init__.py
touch $BASE_DIR/handlers/base_handler.py
touch $BASE_DIR/handlers/env_check.py
touch $BASE_DIR/handlers/planning.py
touch $BASE_DIR/handlers/folder_setup.py
touch $BASE_DIR/handlers/backend_setup.py
touch $BASE_DIR/handlers/frontend_setup.py
touch $BASE_DIR/handlers/docker_setup.py
touch $BASE_DIR/handlers/ci_cd.py
touch $BASE_DIR/handlers/observability.py
touch $BASE_DIR/handlers/documentation.py

mkdir -p $BASE_DIR/utils
touch $BASE_DIR/utils/__init__.py
touch $BASE_DIR/utils/commands.py
touch $BASE_DIR/utils/input_helpers.py

# Create the requirements.txt file
touch $BASE_DIR/requirements.txt

echo "Project structure created successfully."
