FROM public.ecr.aws/lambda/python:3.8

ENV TARGET_BUCKET=replace_me

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./
RUN ls ./

CMD [ "handler.lambda_handler" ]