FROM ubuntu

# Update package list
RUN apt-get update

# Install Python3 and required packages
RUN apt-get install -y python3 python3-flask python3-redis

# Copy your application files to /opt/
COPY app.py /opt/
COPY static /opt/static/
COPY templates /opt/templates/

# Set the working directory to /opt/
WORKDIR /opt/

# Set FLASK_APP environment variable
ENV FLASK_APP=app.py

# Set ENTRYPOINT to run your app
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
