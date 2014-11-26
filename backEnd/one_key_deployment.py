import boto.ec2
import sys,json,time,os

"""
1. User specifies AWS credentials in a separate key file;
    * key_file.json contains aws keys
    * csc326_group18.pem is the ras key to connect instance
2. User invokes your deployment script;
    * python one_key_deployment.py  key_file csc326_group18
3. Deployment script loads the AWS key file, launches AWS instance, copies application files to the new instance, installs packages on AWS instance, and launch the search engine on server.
    * use ssh and git to download source code
4. When the server is stable, the deployment script returns the IP address or public DNS of the new AWS instance. Also, the instance ID of new machine should be returned.
    * auto run delpy.sh script to download package
    * auto generate backend database
    * auto run frontend
    * ID, IP, and DNS is printed and returned
5. User accesses the search engine service through the returned IP address or public
DNS from browser
"""
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
        print "Not yet, Check status again after 30secs"
        time.sleep(30)
        status = instance.update()
    time.sleep(30)
    if status == 'running':
        instance_id = instance.id
        pub_dns = instance.public_dns_name
        pub_ip = instance.ip_address
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name + " DNS/IP: " + pub_dns + "/" + pub_ip )
    else:
        print('Instance status: ' + status)
        return

    print "Wait 5 mins until instance is stable"
#    time.sleep(60*5)

    copy_file_cmd = '''ssh -i {}.pem ubuntu@{} "rm -rf pl_works && yes | sudo apt-get install git && git clone https://github.com/wlz1028/pl_works.git"'''.format(rsa_keyfile_name, pub_ip)
    print "Downlaoding source code to instance"
    print "executing -> "+ copy_file_cmd
    os.system(copy_file_cmd)

    print "Run deploy script"
    deploy_cmd = '''ssh -i {}.pem ubuntu@{} "cd pl_works && chmod +x deploy.sh && sudo ./deploy.sh" '''.format(rsa_keyfile_name, pub_ip)
    print "executing -> "+ deploy_cmd
    os.system(deploy_cmd)

    return (instance_id, pub_dns, pub_ip)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Help: arg1=key file, arg2=rsa_keyfile_name"
    main(sys.argv[1], sys.argv[2])
