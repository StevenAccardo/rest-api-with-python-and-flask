#Use the official Python runtime as a base image
FROM python:3.11

# Set the CWD
WORKDIR /app

# Copy in the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies ensuring to not use a cache if present and to upgrade any libraries where allowed by the requirements.txt file
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Documents what port we want exposed on the container in order for requests to access our service
EXPOSE 4000

# CMD ["flask", "run", "--host", "0.0.0.0"]

# Use gunicorn to start the application on port 4000
CMD ["gunicorn", "-b", "0.0.0.0:4000", "app:create_app()"]
