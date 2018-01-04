FROM python:3.5-jessie

COPY ./ /mnt/
RUN cd /mnt \
&& pip install -r requirements.txt

ENTRYPOINT cd /mnt ;python /mnt/app.py
