from time import sleep
import requests
import json

def jss_post(ip, port, path, query):
    url = 'http://%s:%s/%s' % (ip, port, path)
    print(url)
    try:
        r = requests.post(url=url, data=query)
        return r.text
    except:
        return ""
    
def test_sql(ip, port):
    
    query_json = {}
    query_json['text'] = '字表中字为"挣"的所有信息。'
    ret = jss_post(ip, port, 'nl2sql', json.dumps(query_json))
    print(ret)
    print()

def test_bcc(ip, port, text):
    query_json = {}
    query_json['text'] = text
    ret = jss_post(ip, port, 'nl2bcc', json.dumps(query_json))
    print(ret)
    print()

if __name__ == "__main__":
    # test_sql('127.0.0.1', '8102')
    test_bcc('127.0.0.1', '8102', "昨天\"加任意一个或者多个字加\"唱歌\"加任意一个或者多个字，并且以标点符号结尾")