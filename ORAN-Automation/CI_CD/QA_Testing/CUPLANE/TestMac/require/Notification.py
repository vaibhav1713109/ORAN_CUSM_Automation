import json, httplib2

def notification(msg):
    try:
        # url = 'https://chat.googleapis.com/v1/spaces/AAAAuytRdP0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=8-_LAFt-tf-4RgN75jDHM1D7YQTGGuoN6ZFLqIzeXBQ%3D'

        # message = {'text' : msg}

        # message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        # http_obj = httplib2.Http()

        # response = http_obj.request(
        #     uri=url,
        #     method='POST',
        #     headers=message_headers,
        #     body=json.dumps(message),
        # )
        pass
    except Exception as e:
        print(f'Notification Error : {e}')
    
    finally:
        print(msg)


if __name__ == '__main__':
    notification('Test case SW update Started!! Status: Running')
