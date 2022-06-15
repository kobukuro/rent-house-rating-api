FROM python:3.9-alpine3.13
LABEL maintainer="https://peterchen.pythonanywhere.com/"
# when running application, we want python
# to print any outputs directly to the console,
# so it dosen't buffer the outputs which can create issues
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

# when starting the container, working directory will be /app
# by this way,
# we can directly run the django command without specifying the full path
WORKDIR /app
EXPOSE 8000

# RUN的意思為 runs a command when we're building our image
# 多個指令使用同一個RUN目的為減少image layers, 讓image更輕量化
# (because docker will create a new image layer for every single run command)
#建立虛擬環境在/py資料夾
RUN python -m venv /py && \
#使用虛擬環境的pip
    /py/bin/pip install --upgrade pip && \
# apk:alpine package manager
#使用postgresql db
#.tmp-deps代表temporary dependencies
# postgresql-client is the dependencies needed AFTER the postgres driver is installed
# .tmp-deps的部分是 temp dependencies needed to install the driver
    apk add --update --no-cache postgresql-client && \
        bash gcc libc-dev libressl-dev libffi-dev \
        cargo openssl-dev rust && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
# delete temporary dependencies to keep the image lightweight
    apk del .tmp-deps && \
# 新增一個user名叫app(這個user不需要密碼, 也不需要建立home目錄給這個user)
    adduser --disabled-password --no-create-home app && \
# 建立資料夾(-p:create any sub directories that need to be created
# in order to create that full path)
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
# changes the ownership pf the file(because default will be root user) -R:recursive
    chown -R app:app /vol && \
# give permission(1.文件所有者可讀可寫可執行
#                 2.文件所有者同和其他用戶可讀可執行
#                 3.其它用戶组可讀可執行)
    chmod -R 755 /vol && \
    chmod -R +x /scripts

# 將/scripts以及/py/bin加入環境path中
# 使用python指令, 就會直接使用虛擬環境的(就不用specify full path)
ENV PATH="/scripts:/py/bin:$PATH"
# switch from root user(default user) to user named app
# 此為資安考量
USER app

CMD ["run.sh"]