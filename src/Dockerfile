FROM public.ecr.aws/lambda/python:3.9

ENV LANG=ja_JP.UTF-8
WORKDIR ${LAMBDA_TASK_ROOT}
COPY app.py ./
COPY requirements.txt ./
COPY run-melos.pdf ./
RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && yum update -y && yum install -y poppler-utils tesseract tesseract-langpack-jpn \
    && pip install -U pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["app.lambda_handler"]
