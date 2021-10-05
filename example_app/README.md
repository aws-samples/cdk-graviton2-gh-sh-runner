# graviton2-gh-runner-flask-app

Our example application is an online bookstore where users can find books, add them to their cart, and create orders. The application is written in Python using the Flask framework, and it uses DynamoDB for data storage.

The .github directory contains a workflow that will execute on the Runner on each repository push or pull request.

## Local development

### Dynamodb Local
We have included a helper script in the repo, `dynamodb_local.sh`, that includes shorthand commands for starting DynamoDB local in Docker, creating a table, and loading fake data.

```bash
# Start the database and create the table
./dynamodb_local.sh start
./dynamodb_local.sh create

# Load the local environment and install deps
pipenv shell
pipenv install

# Create and insert fake data
./dynamodb_local.sh load
```

### Starting the application

To start the application, run the start.sh script. This starts the Gunicorn server and Flask application.
```bash
./start.sh
```
