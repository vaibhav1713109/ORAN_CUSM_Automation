import json, httplib2

def notification(msg):
    try:
        url = 'https://chat.googleapis.com/v1/spaces/AAAARK0pkNs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=s7gvoVMj9l1y35wK82laZGUgWSi-kEsuPrM8wat9eQk'

        message = {'text' : msg}

        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = httplib2.Http()

        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=json.dumps(message),
        )
        pass
    except Exception as e:
        print(f'Notification Error : {e}')
    
    finally:
        print(msg)


if __name__ == '__main__':
    notification('Test case 64_QAM_Comp_9_bit_DL_UL !! Status: Running')

