import boto.ec2
import sys,json,time

AKEY = 'AKIAJ3VTN4NVS2C2MZBQ'
SKEY = 'xRVznB/v8RfSHL4Pq1aZNf4fURrfOlGZdSZKjmTw'

def main(key_file, ras_key_name):
    try:
        with open(key_file) as f:
            ckey = json.load(f)
    except:
        raise Exception("Invalid key file")

    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=ckey['AKEY'],
                                    aws_secret_access_key=ckey['SKEY'])
#    try:
#        kp = conn.create_key_pair("csc326_group18")
#        kp.save('.')
#    except:
#        print "Key is alreay created"
#        pass
#
#    try:
#        web = conn.create_security_group('csc326-group18', 'csc326-group18')
#        web.authorize('ICMP', -1, -1, '0.0.0.0/0')
#        web.authorize('TCP', 80, 80, '0.0.0.0/0')
#        web.authorize('TCP', 22, 22, '0.0.0.0/0')
#    except:
#        print "Group is already created"
#        pass
    reservation = conn.run_instances('ami-9aaa1cf2',
                key_name='rsa_keyfile_name',
                instance_type='t2.micro',
                security_groups=['csc326-group18'])

    instance = reservation.instances[0]
    print('Waiting for instance to start...')
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        time.sleep(15)
        status = instance.update()
    if status == 'running':
        pub_dns = instance.public_dns_name
        pub_ip = instance.ip_address
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name + " DNS/IP: " + pub_dns + "/" + pub_ip )
    else:
        print('Instance status: ' + status)
        return

    copy_file_cmd = '''ssh -i {}.pem ubuntu@{} "rm -rf pl_works && git clone https://github.com/wlz1028/pl_works.git"'''.format(rsa_keyfile_name, pub_ip)



#   >>> conn.allocate_address()
#   Address:54.165.139.125
#    r_id = conn.get_all_instances()[-1].instances[-1].id
#    conn.associate_address(r_id, public_ip='54.165.139.125')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Help: arg1=key file, arg2=rsa_keyfile_name"
    main(sys.argv[1], sys.argv[2)
