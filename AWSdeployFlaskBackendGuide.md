# AWS EC2 Setup Guide

## Reference this [link](https://www.twilio.com/blog/deploy-flask-python-app-aws#:~:text=A%20GitHub%20repository%20with%20files,starting%20a%20basic%20Flask%20app.) for deploying a backend in AWS EC2 instance.

## To transfer your project files to remote host
1. Use "ruina-db-test.pem" located inside of this project folder
``` bash
scp -i "ruina-db-test.pem" ./* ubuntu@54.210.56.237:/home/ubuntu/RuinaDB
```

## To run the app
1. cd into project folder
2. run "python3 run.py"