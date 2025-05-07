# Stage 1: Build the React application
FROM node:18-alpine as build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./
# If using yarn, copy yarn.lock as well
# COPY yarn.lock ./

# Install dependencies
# If using npm:
RUN npm install
# If using yarn:
# RUN yarn install

# Copy the rest of the application code
COPY . .

# Build the application
# If using npm:
RUN npm run build
# If using yarn:
# RUN yarn build

# Stage 2: Serve the application with Nginx
FROM nginx:stable-alpine

# Copy the build output from Stage 1
COPY --from=build /app/build /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
