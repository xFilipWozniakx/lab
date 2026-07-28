#ST 1:
FROM ubuntu:24.04 AS builder

WORKDIR /build
COPY generate-status . 
RUN chmod +x generate-status && ./generate-status > index.html

#ST 2:
FROM nginxinc/nginx-unprivileged:1.28
COPY --from=builder /build/index.html /usr/share/nginx/html/index.html

EXPOSE 8080

