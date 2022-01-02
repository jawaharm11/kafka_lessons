#!/bin/bash

cd $KAFKA_SSL_SECRETS_DIR

set -o nounset \
    -o errexit \
    -o verbose \
    -o xtrace

# Generate CA key
openssl req -new -x509 -keyout ca-1.key -out ca-1.crt -days 365 -subj '/CN=ca1.xbyte.io/OU=Test/O=XByte/L=Richmond/S=VA/C=US' -passin pass:test123 -passout pass:test123



for i in broker1 broker2 broker3 producer consumer
do
	echo $i
	# Create keystores
	keytool -genkey -noprompt \
				 -alias $i \
				 -dname "CN=$i.xbyte.io, OU=Test, O=XByte, L=Richmond, S=VA, C=US" \
				 -keystore kafka.$i.keystore.jks \
				 -keyalg RSA \
				 -storepass test123 \
				 -keypass test123

	# Create CSR, sign the key and import back into keystore
	keytool -keystore kafka.$i.keystore.jks -alias $i -certreq -file $i.csr -storepass test123 -keypass test123

	openssl x509 -req -CA ca-1.crt -CAkey ca-1.key -in $i.csr -out $i-ca1-signed.crt -days 9999 -CAcreateserial -passin pass:test123

	keytool -keystore kafka.$i.keystore.jks -alias CARoot -import -file ca-1.crt -storepass test123 -keypass test123

	keytool -keystore kafka.$i.keystore.jks -alias $i -import -file $i-ca1-signed.crt -storepass test123 -keypass test123

	# Create truststore and import the CA cert.
	keytool -keystore kafka.$i.truststore.jks -alias CARoot -import -file ca-1.crt -storepass test123 -keypass test123

  echo "test123" > ${i}_sslkey_creds
  echo "test123" > ${i}_keystore_creds
  echo "test123" > ${i}_truststore_creds
done