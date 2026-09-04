1) Create the docker file

2) Create image using the docker file
```
docker build -t myapp:latest .
```
3) Run the docker image
```
docker run -p 80:80 myapp:latest
```

4) Verify the application is running by accessing it in your web browser at `http://localhost:80` or using curl:
```
# Stop the current container (Ctrl+C)
# Then run with port mapping
docker run -p 80:80 myapp:latest

# OR if port 80 is already in use on your machine:
docker run -p 8080:80 myapp:latest
# Then access: http://localhost:8080

```