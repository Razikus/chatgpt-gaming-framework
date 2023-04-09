FROM node:18 as builder
WORKDIR /app
COPY . .
RUN yarn
RUN node_modules/.bin/quasar build -m spa

FROM nginx
COPY --from=builder /app/dist/spa /usr/share/nginx/html
RUN mkdir -p /etc/nginx/templates
COPY nginx.conf /etc/nginx/templates/default.conf.template
EXPOSE 80