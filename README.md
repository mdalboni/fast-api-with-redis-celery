# Simple FastAPI With Celery and Redis

## Run Locally with your docker

### Build and start the server

If you need to build (prepare) the server and then start it, run:

```sh
make build_and_start_server
```

### Start the server and execute a command:

If you want to start the server and then run a command inside it, use:

```sh
make start_server_and_exec
```

After running this command you will be connected to the docker. You can run any command you want.

## Run Tests
The tests will behave similar to integration tests, since it has a dependency on Redis.  
Due the time constraints, I didn't feel the need to mock the Redis dependency.

### Run when you are in the docker

This will start the webservice and the redis. Now you will be able to run tests and see how much of your code is tested,
run:

```sh
make start_server_and_exec
make run_tests
```

Or you can run this for coverage:

```sh
make run_tests_with_coverage
```

### Run when you are not in the docker

This will start the webservice and the redis. And will connect to the docker and run the tests.

```sh
make run_tests_in_docker
```

Or you can run this for coverage:

```sh
make run_tests_with_coverage_in_docker
```

## Endpoints

### HTTP files 
You can use the .HTTP
### Postman Collection
You can import the postman collection from the file `postman_collection.json` in the apis folder.

## Possible Improvements

1. Exception handling
   1. Custom exceptions for extra clarity
2. Logging
    1. Clean up the logger config and add more logs
3. Tests
   1. Add more tests to cover more scenarios
   2. Remove the redis dependency from the tests
4. Observability
   1. Add the foundations for monitoring and alerting 
5. Use the dependency injection tools from FastAPI
   1. To make the code more testable and maintainable