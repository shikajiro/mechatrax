import aws_lambda_typing as lambda_typing
import requests


def handler(event: lambda_typing, context: lambda_typing.Context):
    res = requests.get("https://api.github.com/users/shikajiro/repos")
    return res.content