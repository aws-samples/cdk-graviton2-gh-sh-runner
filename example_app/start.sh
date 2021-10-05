#!/bin/bash

ENVIRO="${ENVIRO:-'development'}"

pipenv run gunicorn -w 4 -b localhost:5000 "graviton2_gh_runner_flask_app:create_app($ENVIRO)"
