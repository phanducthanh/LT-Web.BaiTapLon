import tempfile
import subprocess

tempfile.tempdir = r"C:\Users\trand\Desktop\LT-Web.BaiTapLon"

fp = tempfile.TemporaryFile()

fp.write(b"print('Hello world!')")

result = subprocess.check_output(['python', fp.name])

print(result.decode())
