keypass="test123"

ssl_dir=/tmp/ssl
tmpdir=/tmp

CN=$1
if [ -z "$CN" ]
then
    echo "/CN is empty"
    usage "./ssl.sh <hostname_fqdn>"
    exit 1;
else
    keystore="$ssl_dir/kafka.${CN}.keystore.jks"
    truststore="$ssl_dir/kafka.truststore.jks"
    mkdir -p ${ssl_dir}

    dname="CN=$CN,OU=Streaming,O=Myorg,L=Richmond,ST=VA,C=US"

    if [ -s "${tmpdir}/ca-key" ]; then
        echo "Skipping root key/ca generation"
    else
        echo "Generating CA key"
        openssl req -new -x509 -keyout ${tmpdir}/ca-key -out ${tmpdir}/ca-cert -days 365 -nodes -subj "/CN=caroot"
    fi

    echo "Generting a keystore with ${dname}...."
    keytool -genkey -keystore ${keystore} -alias ${CN} -validity 365 -keyalg RSA -dname "${dname}" -keysize 2048 -storepass ${keypass} -keypass ${keypass}

    echo "Generating Cert...."
    keytool -certreq -keystore ${keystore} -alias ${CN} -file ${tmpdir}/${CN}.csr -storepass ${keypass} -keypass ${keypass}

    echo "Signing Cert...."
    openssl x509 -req -in ${tmpdir}/${CN}.csr -CA ${tmpdir}/ca-cert -CAkey ${tmpdir}/ca-key \
    -CAcreateserial -out ${ssl_dir}/${CN}.crt -days 365 -passin pass:${keypass}

    echo "Import RootCA into keystore"
    keytool -import -noprompt -keystore ${keystore} -alias caroot -file ${tmpdir}/ca-cert \
    -storepass ${keypass} -keypass ${keypass}

    echo "Import Signed Cert into keystore"
    keytool -import -noprompt -trustcacerts -keystore ${keystore} -alias ${CN} -file ${ssl_dir}/${CN}.crt -storepass ${keypass} -keypass ${keypass}

    if [ -s ${truststore} ]; then
        echo "Skipping truststore generation"
    else
        keytool -keystore ${truststore} -alias caroot -import -file ${tmpdir}/ca-cert -storepass ${keypass} -keypass ${keypass} -noprompt

    fi
fi