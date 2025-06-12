FROM --platform=linux/amd64 node:20-slim

WORKDIR /app

# Copy package files and install dependencies
COPY package.json ./
RUN npm install --force

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
