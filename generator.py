#!/usr/bin/env python
import requests
from string import Template


posttemplate = requests.get('https://raw.githubusercontent.com/amerissa/cloudbreak-krb-recipe/master/postinstall.template').text
pretemplate = requests.get('https://raw.githubusercontent.com/amerissa/cloudbreak-krb-recipe/master/preinstall.template').text

while True:
    ADREALM = raw_input('Is AD available? (This will setup a local krb5 realm if not available ) y/n: ')
    if ADREALM not in ['y', 'n']:
        print('Answer has to be y or n')
        continue
    else:
        break
DOMAIN = raw_input('Domain: ')
UDOMAIN = DOMAIN.upper()
LDOMAIN = DOMAIN.lower()
CERTLOC = raw_input('Path of AD Cert in pem format: ')
CERT = open(CERTLOC, 'r').read()

if ADREALM is 'y':
    ADSERVER = raw_input('AD Server: ')
    MACHINEOU = raw_input('Machine OU (For SSSD configs): ')
    GROUPSFILTER = raw_input('Access Filter for SSSD: ')
    ADUSER = raw_input('AD User to use for binding: ')
    PASSWORD = raw_input('AD Password to use for binding: ')
    BASEDN = raw_input('AD Base DN for Ambari: ')
    CONTAINERDN = raw_input('AD Container DN for Kerberos: ')
else:
    PASSWORD= raw_input('Password for Kerberos Realm and Ambari: ')
    ADSERVER = None
    MACHINEOU = None
    GROUPSFILTER = None
    ADUSER = 'ambari/admin'
    BASEDN = None
    CONTAINERDN = None


template = { 'CERT' : CERT, 'UDOMAIN' : UDOMAIN, 'LDOMAIN' : LDOMAIN, 'ADREALM' : ADREALM, 'ADSERVER' : ADSERVER, 'MACHINEOU' : MACHINEOU, 'GROUPSFILTER' : GROUPSFILTER, 'ADUSER' : ADUSER, 'PASSWORD' : PASSWORD, 'BASEDN' : BASEDN,  'CONTAINERDN' : CONTAINERDN }

finaltemplatepost = open('./postinstall.sh', 'w')
finaltemplatepre = open('./preinstall.sh', 'w')

finaltemplatepost.write(posttemplate.format(**template))
finaltemplatepre.write(pretemplate.format(**template))
