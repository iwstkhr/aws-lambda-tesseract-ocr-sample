# AWS Lambda Tesseract OCR Sample
Tesseract OCR Sample with AWS Lambda Container Images using AWS SAM

Please refer to [How to Run Tesseract OCR + pytesseract in AWS Lambda Container Images](https://devnote.tech/2022/06/how-to-run-tesseract-ocr-pytesseract-in-aws-lambda-container-images) for more details.

## Requirements
- AWS SAM
- Python 3.9

## Build
```shell
sam build
```

## Local Invoke
```shell
sam local invoke
```

## Deploy
Set your ECR repository URI to `--image-repository`.

```shell
sam deploy \
  --stack-name aws-lambda-tesseract-ocr-sample \
  --image-repository 123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/tesseract-ocr-lambda \
  --capabilities CAPABILITY_IAM
```

## Delete
```shell
sam delete --stack-name aws-lambda-tesseract-ocr-sample
```
