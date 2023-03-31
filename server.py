# -*- coding: utf-8 -*-

from pygics import rest, server
import uuid
import json

#===============================================================================
# SECRET
#===============================================================================
# read saved secrets
try:
    with open('secrets.data', 'r') as fd:
        secrets = json.loads(fd.read())
except:
    secrets = {}
    with open('secrets.data', 'w') as fd:
        fd.write(json.dumps(secrets, indent=2))
    
# reading secret interface

def find_secret(condition):
    if condition in secrets: return secrets[condition]
    else:
        for secret in secrets.values():
            if condition == secret['name']: return secret
        raise Exception(f'could not find secret with condition: {condition}')

@rest('GET', '/secret')
def read_secret(req, condition=None):
    if condition: return find_secret(condition) 
    return [secret for secret in secrets.values()]

# creating secret interface
@rest('POST', '/secret')
def create_secret(req):
    data = req.data
    # create ID
    id = str(uuid.uuid4())
    # check & set new data
    secret = {
        'id': id,
        'name': data['name'],
        'type': data['type'],
        'projectId': data['projectId'],
        'privateKeyId': data['privateKeyId'],
        'privateKey': data['privateKey'],
        'clientEmail': data['clientEmail'],
        'clientId': data['clientId'],
        'authUri': data['authUri'],
        'tokenUri': data['tokenUri'],
        'authProviderX509CertUrl': data['authProviderX509CertUrl'],
        'clientX509CertUrl': data['clientX509CertUrl']
    }
    
    # save secret
    with open('secrets.data', 'w') as fd:
        secrets[id] = secret
        print(f'Create Secret\n{json.dumps(data, indent=2)}\n{json.dumps(secret, indent=2)}\n')
        fd.write(json.dumps(secrets, indent=2))
    return secret

# updating secret interface
@rest('PUT', '/secret')
def update_secret(req, id):
    # check existing
    if id not in secrets: raise Exception(f'could not find secret with id: {id}')
    data = req.data
    # check & set updated data
    with open('secrets.data', 'w') as fd:
        secret = secrets[id]
        if 'type' in data: secret['type'] = data['type']
        if 'projectId' in data: secret['projectId'] = data['projectId']
        if 'privateKeyId' in data: secret['privateKeyId'] = data['privateKeyId']
        if 'privateKey' in data: secret['privateKey'] = data['privateKey']
        if 'clientEmail' in data: secret['clientEmail'] = data['clientEmail']
        if 'clientId' in data: secret['clientId'] = data['clientId']
        if 'authUri' in data: secret['authUri'] = data['authUri']
        if 'tokenUri' in data: secret['tokenUri'] = data['tokenUri']
        if 'authProviderX509CertUrl' in data: secret['authProviderX509CertUrl'] = data['authProviderX509CertUrl']
        if 'clientX509CertUrl' in data: secret['clientX509CertUrl'] = data['clientX509CertUrl']
        print(f'Update Secret\n{json.dumps(data, indent=2)}\n{json.dumps(secret, indent=2)}\n')
        fd.write(json.dumps(secrets, indent=2))
    return secret

# deleting secret interface
@rest('DELETE', '/secret')
def delete_secret(req, id):
    # check existing
    if id not in secrets: raise Exception(f'could not find secret with id: {id}')
    # delete & save secret
    with open('secrets.data', 'w') as fd:
        secret = secrets.pop(id)
        print(f'Delete Secret\n{json.dumps(secret, indent=2)}\n')
        fd.write(json.dumps(secrets, indent=2))
    return secret

#===============================================================================
# BUCKET
#===============================================================================
# read saved buckets
try:
    with open('buckets.data', 'r') as fd:
        buckets = json.loads(fd.read())
except:
    buckets = {}
    with open('buckets.data', 'w') as fd:
        fd.write(json.dumps(buckets, indent=2))

# reading bucket interface
@rest('GET', '/bucket')
def read_bucket(req, id=None):
    if id:
        if id in buckets: return buckets[id]
        else: raise Exception(f'could not find bucket with id: {id}')
    return [bucket for bucket in buckets.values()]

# creating bucket interface
@rest('POST', '/bucket')
def create_bucket(req):
    data = req.data
    
    # get secret ###############################################################
    gcpSecretName = data['gcpSecretName']
    secret = find_secret(gcpSecretName)
    # USE CONNECT TO GCP USING "secret" ########################################
    
    #===========================================================================
    # MAKING SAMPLE BUCKET DATA
    #===========================================================================
    # bucket id == bucket name
    id = data['name']
    if id in buckets: raise Exception(f'bucket {id} is already existing')
    # check & set new data
    bucket = {
        'id': id,
        'name': data['name'],
        'gcpSecretName': data['gcpSecretName'],
        'gcpProjectName': data['gcpProjectName']
    }
    # save data
    with open('buckets.data', 'w') as fd:
        buckets[id] = bucket
        print(f'Create Bucket\n{json.dumps(data, indent=2)}\n{json.dumps(secret, indent=2)}\n{json.dumps(bucket, indent=2)}')
        fd.write(json.dumps(buckets, indent=2))
    return bucket

# updating bucket interface
@rest('PUT', '/bucket')
def update_bucket(req, id):
    if id not in buckets: raise Exception(f'could not find bucket with id: {id}')
    data = req.data
    
    # get secret ###############################################################
    gcpSecretName = data['gcpSecretName']
    secret = find_secret(gcpSecretName)
    # USE CONNECT TO GCP USING "secret" ########################################
    
    #===========================================================================
    # UPDATING SAMPLE BUCKET DATA
    #===========================================================================
    # check & set updated data
    with open('buckets.data', 'w') as fd:
        bucket = buckets[id]
        if 'gcpProjectName' in data: bucket['gcpProjectName'] = data['gcpProjectName']
        print(f'Update Bucket\n{json.dumps(data, indent=2)}\n{json.dumps(secret, indent=2)}\n{json.dumps(bucket, indent=2)}')
        fd.write(json.dumps(buckets, indent=2))
    return bucket

# deleting bucket interface
@rest('DELETE', '/bucket')
def delete_bucket(req, id):
    if id not in buckets: raise Exception(f'could not find bucket with id: {id}')
    data = buckets[id]
    
    # get secret ###############################################################
    gcpSecretName = data['gcpSecretName']
    secret = find_secret(gcpSecretName)
    # USE CONNECT TO GCP USING "secret" ########################################
    
    #===========================================================================
    # DELETING SAMPLE BUCKET DATA
    #===========================================================================
    # delete & save secret
    with open('buckets.data', 'w') as fd:
        bucket = buckets.pop(id)
        print(f'Delete Bucket\n{json.dumps(secret, indent=2)}\n{json.dumps(bucket, indent=2)}')
        fd.write(json.dumps(buckets, indent=2))
    return bucket

if __name__ == '__main__':
    server('0.0.0.0', 8080)
