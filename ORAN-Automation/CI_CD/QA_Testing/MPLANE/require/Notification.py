###############################################################################
"""
 * ---------------------------------------------------------------------------
 *                              VVDN CONFIDENTIAL
 * ---------------------------------------------------------------------------
 * Copyright (c) 2016 - 2023 VVDN Technologies Pvt Ltd.
 * All rights reserved
 *
 * NOTICE:
 *      This software is confidential and proprietary to VVDN Technologies.
 *      No part of this software may be reproduced, stored, transmitted,
 *      disclosed or used in any form or by any means other than as expressly
 *      provided by the written Software License Agreement between
 *      VVDN Technologies and its license.
 *
 * PERMISSION:
 *      Permission is hereby granted to everyone in VVDN Technologies
 *      to use the software without restriction, including without limitation
 *      the rights to use, copy, modify, merge, with modifications.
 *
 * ---------------------------------------------------------------------------
 */

/**
 *
 * @file     Notification.py
 * @part_of  CICD M PLANE O-RAN CONFORMANCE
 * @scope    Throughout the CD process
 * @author   CD Core Team. (Sebu Mathew, Vaibhav Dhiman,Vikas Saxena)
 *             (sebu.mathew@vvdntech.in,vaibhav.dhiman@vvdntech.in,vikas.saxena@vvdntech.in)
 * 
 *
 *
 */
 """
###############################################################################
import json, httplib2

def notification(msg):
    try:
        url = 'https://chat.googleapis.com/v1/spaces/AAAAuytRdP0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=8-_LAFt-tf-4RgN75jDHM1D7YQTGGuoN6ZFLqIzeXBQ%3D'

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
    notification('Test case SW update Started!! Status: Running')

