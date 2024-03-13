# 1.ติดตั้ง ENV

python -m venv envdjango

.\envdjango\Scripts\activate  เปิดการใช้งาน

.\envdjango\Scripts\deactivate ปิดการใช้งาน

(myenv) C:\xxx\
 
# 2.ติดตั้ง pip 

#  pip install -r requirements.txt
นำ index.html ไป localhost
http://localhost/index.html

# RUN
py manage.py runserver



# Dockerfile ไว้เทส
หากคุณลง Docker สำเร็จแล้วลองใช่คำสั่ง
1.สร้าง IMAGE
docker image build -t <imagename>.
docker image build -t my-django .
docker image build -t my-django:v1.0 . // version

2.ทำ Container
docker run -d --name <containername> -p 8000:8000 <image>:<optional>


# Example Code
1.Create Image
docker image build -t my-django . // none version
or
docker image build -t my-django:v1.0 . // version

2.Create Container

docker run -d --name pethzero-django -p 8000:8000 my-django // image-none-version 
or
docker run -d --name pethzero-django -p 8000:8000 my-django:v1.0 // version


3.RUN
docker container start pethzero-django //name
or
docker container start 02b8815fae6c //Container Name

พิมพ์ http://127.0.0.1:8000/