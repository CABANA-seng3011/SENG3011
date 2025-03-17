# # Use Node official image
# FROM node:20

# WORKDIR /cabana

# COPY ./cabana/package*.json ./
# RUN yarn install

# COPY ./cabana .

# EXPOSE 3000
# CMD ["yarn", "dev"]

# Use Node official image
FROM node:20

# Set working directory inside the container
WORKDIR /app

# Copy package.json and yarn.lock first (dependency caching)
COPY cabana/package*.json ./

# Install dependencies
RUN yarn install

# Copy the rest of the application code
COPY cabana/. .

# Expose Next.js port
EXPOSE 3000

# Start the Next.js app
CMD ["yarn", "dev"]
