import requests, datetime, hashlib, hmac, random, zlib, json

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning
def AWSsignature(access_key, secret_key, request_parameters, headers, method="GET", payload='', region="sdwdmwlll", service="vod"):
    # https://docs.aws.amazon.com/fr_fr/general/latest/gr/sigv4-signed-request-examples.html
    canonical_uri = '/'
    canonical_querystring = request_parameters
    canonical_headers = '\n'.join([f"{h[0]}:{h[1]}" for h in headers.items()]) + '\n'
    signed_headers = ';'.join(headers.keys())
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    amzdate = headers["x-amz-date"]
    datestamp = amzdate.split('T')[0]
    print(canonical_request)

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = access_key+'/'+datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    print(string_to_sign)
    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    print(signing_key)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    return signature
