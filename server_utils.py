import re
import requests
import urllib
import json

bad_stuns = {
    r"stun[\d]{0,1}\.l\.google\.com": "Google"
}

# the checkStun function is based on:
# https://git.jugendhacker.de/j.r/jitsi-list-generator/
# and 
# https://gist.github.com/duncanturk/243d26a0390ec8620ff64cbd36d185aa
# thanks to:
# Julian (https://git.jugendhacker.de/j.r)
# and
# Christopher Rossbach (https://github.com/duncanturk)
def trustworthyStun(domain):
  try:
    r = requests.get(domain + "random-redirect-test", timeout=15.0)
  except Exception as inst:
    return False
  if (r.status_code != requests.codes.ok):
    return False
  for (bad_stun, reason) in bad_stuns.items():
    matches = re.findall("\n.*" + bad_stun, r.text)
    for match in matches:
      if "//" not in match:
        return False
  return True

badAsnDesc = [
    "GOOGLE",
    "AMAZON",
    "CLOUDFLARE",
    "MICROSOFT"
]

# the hasBadHoster function is based on:
# https://git.jugendhacker.de/j.r/jitsi-list-generator/
# thanks to:
# Julian (https://git.jugendhacker.de/j.r)
def hasBadHoster(domain):
  with urllib.request.urlopen("https://tools.keycdn.com/geo.json?host=" + domain[8:].split("/", 1)[0]) as url:
    data = json.loads(url.read().decode())
    if data['status'] == "success":
      for asnDesc in badAsnDesc:
        if data['data']['geo']['isp'].casefold().find(asnDesc.casefold()) != -1:
          return True
      return False
    return True

# the getCountry function is based on:
# https://git.jugendhacker.de/j.r/jitsi-list-generator/
# thanks to:
# Julian (https://git.jugendhacker.de/j.r)
def getCountry(domain):
  with urllib.request.urlopen("https://tools.keycdn.com/geo.json?host=" + domain[8:].split("/", 1)[0]) as url:
    data = json.loads(url.read().decode())
    if data['status'] == "success":
      return data['data']['geo']['country_code']
    else:
      return "n.A."

