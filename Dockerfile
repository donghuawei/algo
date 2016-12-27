FROM dliu/ubuntu-miniconda:16.04

ADD requirements.txt requirements.txt

ADD . /algo

RUN pip install -r requirements.txt

ENV PYTHONPATH=.:/algo

EXPOSE 8000

CMD cd /algo && python algo/start.py 
