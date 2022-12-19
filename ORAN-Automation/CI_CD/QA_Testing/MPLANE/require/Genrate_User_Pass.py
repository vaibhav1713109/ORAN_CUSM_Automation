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
 * @file     Generate_username.py
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

import random, string

def genrate_password():
    a =(random.randint(8, 128))
    pun = '!$%^()_+~{}[].-'
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + pun
    password = ''.join(random.choice(characters) for i in range(a))
    return password

def genrate_username():
    a =(random.randint(3, 23))
    chars = string.digits
    # get random password pf length 8 with letters, digits, and symbols
    username = 'operator{}'.format(''.join(random.choice(chars) for i in range(a)))
    return username  

