FROM node:22-alpine AS dev
WORKDIR /app
CMD ["sh", "-c", "npm ci && npm run dev -- --host 0.0.0.0"]

FROM dev AS build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
