FROM gcr.io/google-appengine/python@sha256:c6480acd38ca4605e0b83f5196ab6fe8a8b59a0288a7b8216c42dbc45b5de8f6

LABEL python_version=python3

RUN virtualenv --no-download /env -p python3

ENV VIRTUAL_ENV /env

ENV PATH /env/bin:$PATH

ADD requirements.txt /app/

RUN python -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN mv /env/lib/python3.7/site-packages/fasttext /env/lib/python3.7/site-packages/fastText

ADD . /app/

CMD exec gunicorn -b :$PORT app:app
