
import requests
import json
import ast
import os
import bs4
from twilio.rest import Client

url = 'https://api.ontario.ca/api/drupal/page%2F2020-ontario-immigrant-nominee-program-updates?fields=nid,field_body_beta,body'
req = requests.get(url)
text = json.loads(req.text)
dict = ast.literal_eval(json.dumps(text, indent=2))
result = dict['body']['und'][0]['value']
result = os.linesep.join([s for s in result.splitlines() if s])
soup = bs4.BeautifulSoup(result, 'html.parser')
find_all_h3 = soup.find_all('h3')
first = str(find_all_h3[0])
second = str(find_all_h3[1])
final = result.split(first)[1].split(second)[0]

base_path = '/Users/yyb/Documents/pnp_static.txt'
new_path = '/Users/yyb/Documents/pnp_dynamic.txt'

with open(new_path,'w') as f:
   f.write(final)

f_static = open(base_path,'r')
f_dynamic = open(new_path,'r')

print f_static.readlines() == f_dynamic.readlines()

if f_static.readlines() <> f_dynamic.readlines():
   account_sid = 'ACxxxxxxx'
   auth_token = 'xxxxx'
   client = Client(account_sid, auth_token)

   message = client.messages \
      .create(
      body='!!! There is a change deteded on https://www.ontario.ca/page/2020-ontario-immigrant-nominee-program-updates !!! Click on https://www.ontarioimmigration.gov.on.ca/oinp_index/resources/app/guest/index.html#!/ to join the queue !!!',
      from_='+1201234567',
      to='+13334556677'
   )

   print(message.sid)

