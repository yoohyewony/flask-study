# 베이스 이미지 선택
FROM python:3.9

# ls /home/docai/hyewon/study/basicApp  # app.py 파일이 존재하는지 확인

# 작업 디렉토리 설정
WORKDIR /app

# 로컬 애플리케이션 코드를 Docker 이미지에 복사
COPY ./app /app

# 필요한 Python 패키지 설치
RUN apt-get update
RUN pip install flask

# Flask 애플리케이션 실행
CMD ["python", "app.py"]