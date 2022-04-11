FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="https://peterchen.pythonanywhere.com/"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root
# because default user(nginx) dosen't have permission to create file(touch command),
# so need to create default.conf file by root user
# chmod +x /run.sh means that gives executable permission to the run script
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]