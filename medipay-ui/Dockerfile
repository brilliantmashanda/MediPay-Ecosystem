# Stage 1: Build
FROM node:20 AS build
WORKDIR /app

# --- ADD THIS LINE TO FIX THE SSL ERROR ---
RUN npm config set strict-ssl false

COPY package*.json ./
RUN npm install
COPY . .

# --- CHANGE THIS LINE TO USE THE LOCAL SCRIPT ---
RUN npm run build --configuration=production
# Stage 2: Serve with Nginx
FROM nginx:alpine

# 1. Copy the custom config file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 2. Copy the built Angular files
COPY --from=build /app/dist/medipay-ui/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]