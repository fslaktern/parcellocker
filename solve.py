from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA
import requests

# factored with cado-nfs docker image
privkey = RSA.import_key(
    """-----BEGIN RSA PRIVATE KEY-----
MIGqAgEAAiEA1QAYKJmzYlPg/Zo2+NTvb/qRoaboxWr6b2ZiqsIQSokCAwEAAQIgXiN1ifQscSfL
R6px41YRICkzIznPLt19MT0y2ssoH2UCEQDkakBv+0Yf1f7qSfgvpirnAhEA7rlHIiL0MO+4u+hn
yFQhDwIRAJzDhqp023o/x3Ky3CvVJ0ACEA7cZftJhIyxECjGmaTM/7ECEBTKNlPWB+FOyz5K1+xh
qD0=
-----END RSA PRIVATE KEY-----"""
)

d = privkey.d
e = privkey.e
n = privkey.n
print(d, e, n)


def sign(id: int, nonce: bytes) -> int:
    m = bytes_to_long(b"".join([f"{id:02d}".encode("utf-8"), b".", nonce]))
    return pow(m, d, n)


for id in range(2 * 3 * 6):
    nonce = b"\x20"
    sig = sign(id, nonce)
    url = f"http://localhost:8001/open/{id}"
    params = {"nonce": hex(bytes_to_long(nonce)), "sig": hex(sig)}
    box = requests.get(url, params=params)
    print(box.json())
