import boto.ec2

AKEY = 'AKIAJ3VTN4NVS2C2MZBQ'
SKEY = 'OlQeiY/NeFAmuJCLo8VLknV19XctE3JqLMvu61xr'
SKEY = 'xRVznB/v8RfSHL4Pq1aZNf4fURrfOlGZdSZKjmTw'

def main():
    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=AKEY,
                                    aws_secret_access_key=SKEY)
    try:
        kp = conn.create_key_pair("csc326_group18")
        kp.save('.')
    except:
        print "Key is alreay created"
        pass

    try:
        web = conn.create_security_group('csc326-group18', 'csc326-group18')
        web.authorize('ICMP', -1, -1, '0.0.0.0/0')
        web.authorize('TCP', 80, 80, '0.0.0.0/0')
        web.authorize('TCP', 22, 22, '0.0.0.0/0')
    except:
        print "Group is already created"

    conn.run_instances('ami-9aaa1cf2',
        key_name='csc326_group18',
        instance_type='t2.micro',
        security_groups=['csc326-group18'])

#   >>> conn.allocate_address()
#   Address:54.165.139.125
#    r_id = conn.get_all_instances()[-1].instances[-1].id
#    conn.associate_address(r_id, public_ip='54.165.139.125')


