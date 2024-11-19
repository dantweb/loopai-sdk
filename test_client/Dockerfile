# Dockerfile

FROM node:16-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Bundle app source
COPY . .

# Command to run the test client
CMD ["npm", "start"]
