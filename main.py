import aws_lambda_typing as lambda_typing


def handler(event: lambda_typing, context: lambda_typing.Context):
    return "hello"