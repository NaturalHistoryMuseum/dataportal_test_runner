from ubuntu:14.04

RUN apt-get update \
    && apt-get install -y python python-pip npm nodejs-legacy git fontconfig

RUN npm config set registry http://registry.npmjs.org/ \
    && npm install -g casperjs

RUN /usr/bin/pip install git+https://github.com/NaturalHistoryMuseum/dataportal_test_runner.git#egg=dataportal_test_runner
COPY dataportal_test_runner.json /etc/dataportal_test_runner/dataportal_test_runner.json

VOLUME /var/lib/dataportal_test_runner

CMD dataportal_test_runner run

