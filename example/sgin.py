import datetime
import random
import hashlib
from urllib import parse


def sign_url(origin_url: str, private_key: str, uid: int, valid_duration: datetime.timedelta):
    # 有效时间戳
    t = datetime.datetime.now() + valid_duration
    ts = int(t.timestamp())

    # 随机正整数
    r_int = random.randint(0, 1000)

    # md5 生成
    url = parse.urlparse(origin_url)
    encoder = hashlib.md5(f"{url.path}-{ts}-{r_int}-{uid}-{private_key}".encode())
    md5 = encoder.hexdigest()

    # 组合
    auth_key = f"{ts}-{r_int}-{uid}-{md5}"
    new_url = f"{origin_url}?auth_key={auth_key}"
    return parse.quote(new_url, encoding="utf-8", safe=':/?=')


if __name__ == '__main__':
    signed_url = sign_url(
        # 待签名URL，即用户在123云盘直链空间目录下复制的直链url
        origin_url="http://vip.123pan.com/29/音乐/02.一千零一夜-李克勤.wma",
        # 鉴权密钥，即用户在123云盘直链管理中设置的鉴权密钥
        private_key="289ds32418bxdba",
        # 账号id，即用户在123云盘个人中心页面所看到的账号id
        uid=13,
        # 链接签名有效期
        valid_duration=datetime.timedelta(minutes=1)
    )
    print(signed_url)
