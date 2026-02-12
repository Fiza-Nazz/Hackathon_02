# --- Lightweight Frontend Dockerfile (Dev Mode) ---
FROM node:20.10-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++

# Install dependencies (ignoring peer deps to save time)
RUN npm install --legacy-peer-deps --no-audit --no-fund

# Copy source
COPY . .

# Skip build step for speed
# RUN npm run build

# Set environment to development
ENV NODE_ENV=development

# Expose port
EXPOSE 3000

# Start command
CMD ["npm", "run", "dev"]













