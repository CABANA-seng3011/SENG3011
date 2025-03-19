FROM python:3.12

WORKDIR /flask-api

# Install dependencies
RUN pip install flask

# Copy the app code
COPY . .

# Set the Flask app environment variable
ENV FLASK_APP=index.py

EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]