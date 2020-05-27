FROM python:3

ADD parse_to_db.py /
ADD MySqlCon.py /

RUN pip install DateTime
RUN pip install mysql-connector-python

CMD [ "python", "./parse_to_db.py" ]


