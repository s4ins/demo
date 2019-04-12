import requests
import json
import string
import hvac

#CHECK!!!
job_name = "symfony"
vault_url = "https://127.0.0.1:8202"
jenkins_url = "https://127.0.0.1"
params = {}

def jenkins_create_token(uri, payload):
    auth = ('Jks', (vault_requests(vault_token, 'jenkins', '', '', 'read')['data']['data']['password']))
    headers = {"Content-Type": "application/xml"}
    r = requests.post(jenkins_url + uri, data=payload, auth=auth, headers=headers, verify=False)
    vault_requests(vault_token, 'jenkins', 'tokenUuid', (json.loads(r.text))['data']['tokenUuid'], 'put')
    vault_requests(vault_token, 'jenkins', 'tokenValue', (json.loads(r.text))['data']['tokenValue'], 'put')


def jenkins_create_job(uri):
    f = open("/vagrant/symfony.xml", "r")
    auth = ('Jks', (vault_requests(vault_token, 'jenkins', '', '', 'read')['data']['data']['password']))
    headers = {"Content-Type": "text/xml"}
    r = requests.post(jenkins_url + uri, data=f.read(), auth=auth, headers=headers, verify=False)

def jenkins_run_job(uri):
    auth = ('Jks', (vault_requests(vault_token, 'jenkins', '', '', 'read')['data']['data']['password']))
    r = requests.post(jenkins_url + uri, auth=auth, verify=False)
    print(r.status_code)

def vault_requests(token, secret, key, value, req_type):
    client = hvac.Client(vault_url, token, verify=False)
    if req_type == 'put':
        params[key] = value
        client.secrets.kv.v2.create_or_update_secret(path=secret, secret=params)
    else:
        return client.secrets.kv.read_secret_version(path=secret)


def get_vault_token():
    #CHECK!!!
    with open("/vagrant/vault.log") as fp:
        for line in fp:
            if "Root Token" in line:
                return (line.split(":"))[1].strip()

if __name__=="__main__":
    vault_token = get_vault_token()
    # Put Jks user password to vault
    vault_requests(vault_token, 'jenkins', 'password', 'qwerty123', 'put')
    for i in "ABCD":
        vault_requests(vault_token, 'jenkins', 'foo' + i, 'bar' + i, 'put')
#    jenkins_create_token("/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken", { 'newTokenName' : 'testToken' }) 
    jenkins_create_job("/createItem?name="+job_name)
    jenkins_run_job("/job/"+job_name+"/build")
    
