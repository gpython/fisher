#encoding:utf-8
import requests

class HTTP:
  def get(self, url, return_json = True):
    r = requests.get(url)

    #简化if else
    if r.status_code != 200:
      return {} if return_json else ''
    return  r.json() if return_json else r.text