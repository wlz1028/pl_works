import boto.ec2
import sys,json,time,os

AKEY = 'AKIAJ3VTN4NVS2C2MZBQ'
SKEY = 'xRVznB/v8RfSHL4Pq1aZNf4fURrfOlGZdSZKjmTw'

def main(key_file, rsa_keyfile_name):
    try:
        with open(key_file+".json") as f:
            ckey = json.load(f)
    except:
        raise Exception("Invalid key file")

    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=ckey['AKEY'],
                                    aws_secret_access_key=ckey['SKEY'])
    reservation = conn.run_instances('ami-9aaa1cf2',
                key_name=rsa_keyfile_name,
                instance_type='t2.micro',
                security_groups=['csc326-group18'])

    instance = reservation.instances[0]
    print('Waiting for instance to start...')
    # Check up on its status every so often
    status = instance.update()
    while status == 'pending':
        print "Not yet"
        time.sleep(30)
        status = instance.update()
    if status == 'running':
        pub_dns = instance.public_dns_name
        pub_ip = instance.ip_address
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name + " DNS/IP: " + pub_dns + "/" + pub_ip )
    else:
        print('Instance status: ' + status)
        return

    copy_file_cmd = '''ssh -i {}.pem ubuntu@{} "rm -rf pl_works && sudo apt-get install git &&git clone https://github.com/wlz1028/pl_works.git"'''.format(rsa_keyfile_name, pub_ip)
    print "Downlaoding source code to instance"
    print "executing "+ copy_file_cmd
    os.system(copy_file_cmd)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Help: arg1=key file, arg2=rsa_keyfile_name"
    main(sys.argv[1], sys.argv[2])
