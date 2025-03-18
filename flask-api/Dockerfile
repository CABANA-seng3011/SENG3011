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

# ---------------------------- ABOVE IS NOOR's CODE ----------------------------
# ---------------------------- BELOW IS BYRON's CODE ----------------------------

FROM python:3.12

WORKDIR /flask-api

# Install dependencies
RUN pip install flask

# ✅ Copy only files inside the flask-api directory
COPY ./flask-api /flask-api

# Set the Flask app environment variable
ENV FLASK_APP=index.py

EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
