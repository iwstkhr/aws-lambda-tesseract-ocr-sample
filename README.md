## Introduction

Developers can run [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) with [pytesseract](https://pypi.org/project/pytesseract/) using [Lambda container images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html) for efficient and scalable OCR operations.

## Prerequisites

Ensure the following tools are installed on your system:

- [AWS SAM](https://aws.amazon.com/serverless/sam/)
- Python 3.x

## Setting Up the Project

### Writing the AWS SAM Template

The following SAM template sets up the Lambda function triggered by EventBridge, since API Gateway has a [maximum timeout limit of 29 seconds](https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html). The sample Python script execution exceeds this limit.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Tesseract OCR Sample with AWS Lambda Container Images using AWS SAM
Resources:
  TesseractOcrSample:
    Type: AWS::Serverless::Function
    Properties:
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Enabled: true
            Schedule: cron(0 * * * ? *)
      MemorySize: 512
      PackageType: Image
      Timeout: 900
    Metadata:
      DockerTag: latest
      DockerContext: ./src/
      Dockerfile: Dockerfile
```

## Creating the Dockerfile

Create a `Dockerfile` to define the runtime environment. If your application processes text in a specific language like Japanese, set the **`LANG` environment variable** (line 3) accordingly to avoid encoding issues.

```dockerfile line="3"
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
```

## Writing the Python Script

### Define `requirements.txt`

Add the required libraries to `requirements.txt`.

```text
pdf2image==1.16.0
pytesseract==0.3.9
```

### Implement `app.py`

The script converts a PDF to images, performs OCR, and logs the results.

```python
import re
from datetime import datetime

import pdf2image
import pytesseract


def lambda_handler(event: dict, context: dict) -> None:
    start = datetime.now()
    result = ''

    images = to_images('run-melos.pdf', 1, 2)
    for image in images:
        result += to_string(image)
    result = normalize(result)

    end = datetime.now()
    duration = end.timestamp() - start.timestamp()

    print('----------------------------------------')
    print(f'Start: {start}')
    print(f'End: {end}')
    print(f'Duration: {int(duration)} seconds')
    print(f'Result: {result}')
    print('----------------------------------------')


def to_images(pdf_path: str, first_page: int = None, last_page: int = None) -> list:
    """ Convert a PDF to a PNG image.

    Args:
        pdf_path (str): PDF path
        first_page (int): First page starting 1 to be converted
        last_page (int): Last page to be converted

    Returns:
        list: List of image data
    """

    print(f'Convert a PDF ({pdf_path}) to a png...')
    images = pdf2image.convert_from_path(
        pdf_path=pdf_path,
        fmt='png',
        first_page=first_page,
        last_page=last_page,
    )
    print(f'A total of converted png images is {len(images)}.')
    return images


def to_string(image) -> str:
    """ OCR an image data.

    Args:
        image: Image data

    Returns:
        str: OCR processed characters
    """

    print(f'Extract characters from an image...')
    return pytesseract.image_to_string(image, lang='jpn')


def normalize(target: str) -> str:
    """ Normalize result text.

    Applying the following:
    - Remove newlines.
    - Remove spaces between Japanese characters.

    Args:
        target (str): Target text to be normalized

    Returns:
        str: Normalized text
    """

    result = re.sub('\n', '', target)
    result = re.sub('([あ-んア-ン一-鿐])\s+((?=[あ-んア-ン一-鿐]))', r'\1\2', result)
    return result
```

## Building and Deploying

### Build the Application

Run the following command to build the application:

```shell
sam build
```

Execute the following command to run the application locally:

```shell
sam local invoke
```

### Deploy the Application

If an ECR repository does not exist, create one:

```shell
aws ecr create-repository --repository-name tesseract-ocr-lambda
```

Deploy the application:

```shell
sam deploy \
  --stack-name aws-lambda-tesseract-ocr-sample \
  --image-repository 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/tesseract-ocr-lambda \
  --capabilities CAPABILITY_IAM
```

After deployment, the Lambda function will run hourly and the OCR results will be written to CloudWatch Logs.

## Cleaning Up

To clean up the provisioned AWS resources, use the following command:

```shell
sam delete --stack-name aws-lambda-tesseract-ocr-sample
```

## Conclusion

Running Tesseract OCR in AWS Lambda using container images provides an efficient, scalable way to handle complex OCR workflows.

Happy Coding! 🚀
