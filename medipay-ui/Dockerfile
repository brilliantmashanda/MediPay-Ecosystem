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
# Copy the built files from the previous stage
COPY --from=build /app/dist/medipay-ui/browser /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]