FROM public.ecr.aws/lambda/python:3.8

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY ./app ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
