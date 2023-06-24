#!/bin/bash

# Determine the current script's directory
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
parent_dir="$(dirname "$script_dir")"

manage_py="$parent_dir/../nirikshana/manage.py"
python_script="$script_dir/generate_events_data.py"

poetry run python "$manage_py" shell < "$python_script"
