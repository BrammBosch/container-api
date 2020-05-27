FROM python:3

ADD parse_to_db.py /
ADD MySqlCon.py /

RUN pip install -r requirements.txt

CMD [ "python", "./parse_to_db.py" ]


