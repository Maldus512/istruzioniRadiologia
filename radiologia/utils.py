import hashlib

def filemd5(filename, block_size=2**20):
    f = open(filename, 'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()
