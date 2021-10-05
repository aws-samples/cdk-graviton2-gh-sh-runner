#!/bin/bash

ACTION=$1

function check_for_docker() {
	if $(docker --version >/dev/null); then
		echo "found docker, proceeding"
		return 0
	else
		echo "no docker"
		return 1
	fi
}

function check_dynamodb_local_running() {
	if $(docker container inspect -f '{{.State.Status}}' g2_gh_runner_example_dynamodb >/dev/null); then
		return 0
	else
		echo "Run ./dynamo_local.sh start then try again"
		return 1
	fi
}

function create_dynamodb_table_local() {
	check_dynamodb_local_running && aws dynamodb create-table --table-name graviton2-gh-runner-flask-app \
		--attribute-definitions AttributeName=pk,AttributeType=S \
		AttributeName=sk,AttributeType=S \
		AttributeName=gsi1_pk,AttributeType=S AttributeName=gsi1_sk,AttributeType=S \
		--key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE \
		--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
		--global-secondary-indexes file://gsi.json --endpoint-url http://localhost:8000
}

function start_dynamodb_local() {
	echo "starting dynamodb"
	check_for_docker && docker run -d -p 8000:8000 --name g2_gh_runner_example_dynamodb amazon/dynamodb-local
}

function stop_dynamodb_local() {
	echo "stopping dynamodb"
	docker stop g2_gh_runner_example_dynamodb && docker rm g2_gh_runner_example_dynamodb
}

function pull_dynamodb_local_image() {
	check_for_docker && docker pull amazon/dynamodb-local
}

function check_for_table() {
	if $(aws dynamodb describe-table --table-name graviton2-gh-runner-flask-app --endpoint-url http://localhost:8000 >/dev/null); then
		return 0
	else
		return 1
	fi
}

function load_test_data() {
	check_dynamodb_local_running && check_for_table && python load_local_data.py
}

case $ACTION in
	pull)
		pull_dynamodb_local_image
		;;
	start)
		start_dynamodb_local
		;;
	stop)
		stop_dynamodb_local
		;;
	create)
		create_dynamodb_table_local
		;;
	load)
		load_test_data
		;;
	*)
		echo $"Usage: $0 {pull|start|stop|create|load}"
		exit 1
esac
