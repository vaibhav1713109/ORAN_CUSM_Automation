import paramiko

def GET_SYSTEM_LOGS(host,user, pswrd):
        for _ in range(5):
            try:
                host = host
                port = 22
                username = user
                password = pswrd
                # self.add_page()
                # self.STORE_DATA('\t\t\t\t############ SYSTEM LOGS ##############',Format=True)
                command = "cat {};".format('/media/sd-mmcblk0p4/lpru.log')
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port, username, password,timeout = 20)

                stdin, stdout, stderr = ssh.exec_command(command)
                lines = stdout.readlines()
                for i in lines:
                    print("{}".format(i))
                return True
            except Exception as e:
                print(f'GET_SYSTEM_LOGS Error : {e}')
                pass

host,user, pswrd = '192.168.4.48', 'root','vvdn'
GET_SYSTEM_LOGS(host,user, pswrd)