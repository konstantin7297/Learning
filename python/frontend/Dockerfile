FROM nginx

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /app/static
COPY style.css /app/static
COPY script.js /app/static

COPY nginx.conf /etc/nginx/nginx.conf

#COPY ./static /usr/share/nginx/html/static
#COPY ./index.html /usr/share/nginx/html
#COPY ./nginx.conf /etc/nginx/nginx.conf