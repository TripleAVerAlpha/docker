FROM python:3.10
ADD ./my_project/ /my_project/
RUN pip install --upgrade pip
RUN pip3 install -r my_project/setting/requirements.txt
CMD ["python", "my_project/start.py"] 