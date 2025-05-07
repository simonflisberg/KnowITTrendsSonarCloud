# Use Python 3.12.9
FROM python:3.12.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Cloud Run's required port
EXPOSE 8080

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Use gunicorn to run the Flask app on port 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
