FROM fluxrm/flux-sched:focal

# docker build -t flamingo-mamma .

WORKDIR /code
COPY . /code
RUN python3 -m pip install pytest && \
    sudo chmod +x /code/run_tests.sh
ENV PATH=$PATH:/home/fluxuser/.local/bin
