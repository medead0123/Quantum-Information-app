import time
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def bench_rsa():
    msg = b"Hello Q-ALERT demo"
    t0 = time.perf_counter()
    key = RSA.generate(2048)
    t_gen = time.perf_counter() - t0
    pub = key.publickey()
    cipher = PKCS1_OAEP.new(pub)
    t0 = time.perf_counter()
    ct = cipher.encrypt(msg)
    t_enc = time.perf_counter() - t0
    t0 = time.perf_counter()
    dec = PKCS1_OAEP.new(key).decrypt(ct)
    t_dec = time.perf_counter() - t0
    return t_gen, t_enc, t_dec

def bench_ecc():
    msg = b"Hello Q-ALERT demo"
    t0 = time.perf_counter()
    key = ECC.generate(curve='P-256')
    t_gen = time.perf_counter() - t0
    signer = DSS.new(key, 'fips-186-3')
    h = SHA256.new(msg)
    t0 = time.perf_counter()
    sig = signer.sign(h)
    t_sign = time.perf_counter() - t0
    verifier = DSS.new(key.public_key(), 'fips-186-3')
    h2 = SHA256.new(msg)
    t0 = time.perf_counter()
    verifier.verify(h2, sig)
    t_verify = time.perf_counter() - t0
    return t_gen, t_sign, t_verify

if __name__ == "__main__":
    print("RSA times:", bench_rsa())
    print("ECC times:", bench_ecc())
