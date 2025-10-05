# Use a lightweight Python base image
FROM python:3.12.3-slim-bullseye

# Set the working directory inside the container
WORKDIR /pholcidae

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Define the command to run the application when the container starts
CMD ["python", "manage.py", "runserver"]