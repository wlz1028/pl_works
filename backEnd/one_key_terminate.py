import boto.ec2
import sys,json,time,os

"""
1. User specifies AWS credentials in a separate key file;
    * key_file.json contains aws keys
    * csc326_group18.pem is the ras key to connect instance
2. User invokes termination script and pass the instance ID from command line;
    * python one_key_terminate.py key_file csc326_group18 $ID
3. Termination script shuts down AWS instance.
    * It may faile to terminate, and retry after 5 secs
4. Upon completion, the termination script returns message indicating whether the termination process has been completed successfully.
    * Print successful message at the end
    * Retrun True
"""

def main(key_file, rsa_keyfile_name, instance_id):
    try:
        with open(key_file+".json") as f:
            ckey = json.load(f)
    except:
        raise Exception("Invalid key file")

    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=ckey['AKEY'],
                                    aws_secret_access_key=ckey['SKEY'])
    print "Prepare terminate " + instance_id
    instance = conn.terminate_instances(instance_ids=[instance_id])
    counter = 10
    while (instance[0].update() != 'terminated' or counter == 0):
        print "{}/10 Let's try agin in 5sec".format(str(counter))
        time.sleep(5)
    print "Succesffuly terminated " + instance_id
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Help: arg1=key file, arg2=rsa_keyfile_name"
    main(sys.argv[1], sys.argv[2], sys.argv[3])
