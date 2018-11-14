from config import CLIENTID, CLIENTSECRET
import requests


def compile_code(script, stdin, language, version):
    data = {
        "clientId": CLIENTID,
        "clientSecret": CLIENTSECRET,
        "script": script,
        "stdin": stdin,
        "language": language,
        "versionIndex": version
    }
    headers = {
        "Content-Type": "application/json"
    }
    req = requests.post(url="https://api.jdoodle.com/v1/execute",
                        json=data,
                        headers=headers)
    return req.json()

