# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

FROM python:3.9
WORKDIR /docker/
RUN apt update
RUN apt install -y git neofetch
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "__main__.py" ]
