# Define the base image
FROM python:3.8-slim as base

# Add curl for healthchecks and other utilities
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# set the working directory
WORKDIR /usr/local/app

# Install the requirements
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Dev defines a stage for development, which includes additional tools and dependencies
FROM base as dev
# Install watchdog for development purposes
RUN pip install watchdog
# Set Environment variable for development
ENV FLASK_ENV=development
CMD ["python", "app.py" ]

# Final stage that will bundle the application for production
FROM base as final
# Copy the application code to the container
COPY . .
# Make Port 80 available to the world outside this container
EXPOSE 80
# Define the command to run while starting the container
CMD ["gunicorn","app:app","-b","0.0.0.0:80", "--log-file","-", "--workers","4","--keep-alive","0"]


