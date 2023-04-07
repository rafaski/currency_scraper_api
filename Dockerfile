FROM python:3.10

# Set the working directory to /app/app
WORKDIR /code

# Copy requirements.txt
COPY requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the entire app directory into the container
COPY ./app /code/app