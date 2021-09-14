FROM python:alpine

# navigate to the directory where the app is located

WORKDIR /usr/app

COPY ./requirements.txt ./

# Step 2: Download and install dependency

RUN pip install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy everything from current cowking dir of your pc to current working dir oc container
COPY ./ ./

# Step 3: Tell the image what to do when it starts as container
EXPOSE 8000

CMD python manage.py makemigrations ; python manage.py migrate ; python manage.py runserver 0.0.0.0:8000