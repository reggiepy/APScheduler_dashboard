openssl req -x509  \
  -newkey RSA:4096 \
  -subj "/C=CN/ST=Beijing/L=Beijing/O=MyTest/OU=test/CN=Test" \
  -days 9999 \
  -nodes \
  -keyout caprivate.key \
  -out cacert.crt