FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY . /app


RUN apt update && apt install -y nginx && rm -rf /var/lib/apt/lists/*
RUN uv sync


COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]
