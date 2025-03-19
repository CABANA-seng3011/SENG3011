# FROM python:3.12

# WORKDIR /flask-api

# # Install dependencies
# RUN pip install flask

# # Copy the app code
# COPY . .

# # Set the Flask app environment variable
# ENV FLASK_APP=index.py

# EXPOSE 5000

# # Run the app
# CMD ["flask", "run", "--host=0.0.0.0"]

FROM python:3.12

WORKDIR /flask-api

# Copy the dependencies file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set Flask environment variable
ENV FLASK_APP=index.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
