# Use the official Python image from Docker Hub
FROM python:3.12.5

# Set the working directory inside the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 8000

# Set the environment variable for Flask app
ENV FLASK_APP=app.py

# Set the environment variable for Flask's debug mode
ENV FLASK_ENV=development

# Set the command to run the Flask app when the container starts
CMD ["python", "app.py"]

# # Set the command to run the Flask app when the container starts
# CMD python ./index.py
# # CMD ["python", "-m", "flask", "run"]




