# # Use Node official image
# FROM node:20

# WORKDIR /cabana

# COPY ./cabana/package*.json ./
# RUN yarn install

# COPY ./cabana .

# EXPOSE 3000
# CMD ["yarn", "dev"]

# ---------------------------- ABOVE IS NOOR's CODE ----------------------------
# ---------------------------- BELOW IS BYRON's CODE ----------------------------

# # Use Node official image
# FROM node:20

# # Set the working directory inside the container
# WORKDIR /cabana

# # Copy package.json and yarn.lock first (dependency caching)
# COPY package*.json ./

# # Install dependencies
# RUN yarn install

# # Copy the rest of the application code
# COPY . .

# # Expose Next.js port
# EXPOSE 3000

# # Start the Next.js app
# CMD ["yarn", "dev"]

# ---------------------------- BELOW IS BYRON's CODE ----------------------------

# Use Node official image
FROM node:20

# Set the working directory inside the container
WORKDIR /cabana

# Copy only package.json and yarn.lock first (dependency caching)
COPY package*.json ./
COPY yarn*.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY . .

# Expose Next.js port
EXPOSE 3000

# Start the Next.js app
CMD ["yarn", "dev"]