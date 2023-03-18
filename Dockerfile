FROM python:3.10
ADD ./my_project/ /
RUN pip install --upgrade pip
RUN pip3 install -r setting/requirements.txt
CMD ["python", "src/start.py"] 