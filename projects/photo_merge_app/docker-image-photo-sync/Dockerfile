FROM alpine:3.24.2 
RUN adduser -s /bin/bash -D -u 1000 -h /home/user user
RUN apk update && apk upgrade && apk add build-base wget zlib-dev bzip2-dev xz-dev openssl-dev libffi-dev sqlite-dev readline-dev ncurses-dev expat-dev mpdecimal-dev \
    gdbm-dev musl-libintl openssh bash 

# Python 3 install 
RUN mkdir /opt/py3
COPY py-3-install-script /opt/py3/
RUN chmod +x /opt/py3/py-3-install-script && /opt/py3/py-3-install-script 2>&1 

WORKDIR /app 
COPY . .
# Shove scripts into cont image 

RUN apk add openssl 
RUN chmod +x local_db.py && chmod +x server.py 
RUN chmod +x gen_certs  && mkdir -p ./photo_sync/certs && bash gen_certs && chown -R 1000:1000 ./photo_sync/certs 
RUN python3 -m pip install --upgrade pip && python3 -m pip install bcrypt
RUN rm py-3-install-script gen_certs
USER user 
CMD ["python", "server.py"]



