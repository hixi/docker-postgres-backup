FROM postgres:10

COPY ./install_deps.sh /install_deps.sh

RUN sh ./install_deps.sh
ENV PYTHONUNBUFFERED=yes
COPY ./scripts/* /usr/local/bin/
CMD python3 /usr/local/bin/schedule_backups.py
