# todo-app

### Docker Image Build
#### Build
```docker build -f Dockerfile -t app:1.0.0 . ```
#### Run unit tests
```docker run --rm app:1.0.0 sh -c 'cd todo_list && coverage run --source=base manage.py test && coverage report'```

[test-report](media/coverage-report.png)

#### Run app
```docker run -d -p 8000:80 app:1.0.0```

[login-page](media/login-page.png)

### Jenkins
Jenkinsfile is configured do run following steps
* Install dependencies
* Run tests
* Generate code coverage report.

[jenkins-build-snapshot](media/jenkins-build-snapshot.png)
