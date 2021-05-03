FROM alpine:3.10

WORKDIR /app

RUN apk update && apk add --update --no-cache python3 py3-pip nginx bash curl openrc \
    && ln -sf python3 /usr/bin/python \
    && pip3 install --no-cache --upgrade pip setuptools

COPY nginx.conf /etc/nginx/conf.d
COPY . .

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && pip3 install -r requirements.txt \
    && chmod +x start.sh && cp start.sh /usr/bin/ \
    && mkdir -p /run/nginx \
    && rm -f /etc/nginx/conf.d/default.conf

CMD ["start.sh"]
