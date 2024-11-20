
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import xml.etree.ElementTree as E
import json


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*"), ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', '*')
        self.end_headers()
        print(self.path)
        xml_resp = requests.get(
            f'https://cbr.ru/scripts/XML_daily.asp?date_req={self.path[1:]}')
        valutes = E.fromstring(xml_resp.text)
        my_json = {}
        for child in valutes:
            # print(child.attrib)
            my_json[child.find('CharCode').text] = {
                "Nominal": child.find('Nominal').text,
                "Value": child.find('Value').text
            }
        self.wfile.write(bytes(json.dumps(my_json), 'utf-8'))


server = HTTPServer(('127.0.0.1', 8081), MyServer)
server.serve_forever()
