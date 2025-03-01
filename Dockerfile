FROM datagutten/switchinfo
RUN apt-get update && apt-get install -y --no-install-recommends nginx
COPY nginx/nginx_nossl.conf /etc/nginx/sites-enabled/default
WORKDIR /home/app/web
COPY pimanager /home/app/web/pimanager
COPY pi_device_manager /home/app/web/pi_device_manager
ENV DJANGO_SETTINGS_MODULE=pi_device_manager.settings