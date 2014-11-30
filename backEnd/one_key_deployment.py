import sys,json,time,os

"""
1. User specifies AWS credentials in a separate key file;
    * arg1=access key, arg2=secret key"
2. User invokes your deployment script;
    * python one_key_deployment.py  ACCESS_KEY SECRETE_KEY
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
def main(AKEY, SKEY):
    import boto.ec2
    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=AKEY,
                                    aws_secret_access_key=SKEY)

    #create rsa key
    try:
        kp = conn.create_key_pair("csc326_group18")
        kp.save('.')
    except:
        print "Key is alreay created"
        pass

    #create security group
    try:
        web = conn.create_security_group('csc326-group18_1', 'csc326-group18_1')
        web.authorize('ICMP', -1, -1, '0.0.0.0/0')
        web.authorize('TCP', 80, 80, '0.0.0.0/0')
        web.authorize('TCP', 8080, 8080, '0.0.0.0/0')
        web.authorize('TCP', 22, 22, '0.0.0.0/0')
    except:
        print "Group is already created"

    #run new instance
    reservation = conn.run_instances('ami-9aaa1cf2',
                key_name="csc326_group18",
                instance_type='t2.micro',
                security_groups=['csc326-group18_1'])


    #Checking new instance status
    instance = reservation.instances[0]
    print('Waiting for instance to start...')
    status = instance.update()
    while status == 'pending':
        print "Not yet, Check status again after 30secs"
        time.sleep(30)
        status = instance.update()

    if status == 'running':
        instance_id = instance.id
        pub_dns = instance.public_dns_name
        pub_ip = instance.ip_address
        print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name + " DNS/IP: " + pub_dns + "/" + pub_ip )
    else:
        print('Instance status: ' + status)
        return

    print "Wait 5 mins until instance is stable"
    time.sleep(60*5)

    #Download code to AWS
    copy_file_cmd = '''ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {}.pem ubuntu@{} "rm -rf pl_works && sudo apt-get update && sudo apt-get -y install git && git clone https://github.com/wlz1028/pl_works.git"'''.format("csc326_group18", pub_ip)
    print "Downlaoding source code to instance"
    print "executing -> "+ copy_file_cmd
    os.system(copy_file_cmd)

    #Deploy search engine on aws
    print "Run deploy script"
    deploy_cmd = '''ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i {}.pem ubuntu@{} "cd pl_works && chmod +x deploy.sh && sudo ./deploy.sh" '''.format("csc326_group18", pub_ip)
    print "executing -> "+ deploy_cmd
    os.system(deploy_cmd)

    print('New instance "' + instance.id + '" accessible at ' + instance.public_dns_name + " DNS/IP: " + pub_dns + "/" + pub_ip )
    print "Please use port:80 now"
    return (instance_id, pub_dns, pub_ip)

if __name__ == "__main__":
    try:
        import boto.ec2
    except:
        os.system("chmod +x boto.sh && ./boto.sh")
    if len(sys.argv) != 3:
        print "Help: arg1=access key, arg2=secret key"
    main(sys.argv[1], sys.argv[2])
