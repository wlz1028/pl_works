import boto.ec2
import sys,json,time,os

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
    status = instance[0].update()
    if status == "terminated":
        print "Succesffuly terminated " + instance_id
    else:
        print "Failed to terminate " + instance_id

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Help: arg1=key file, arg2=rsa_keyfile_name"
    main(sys.argv[1], sys.argv[2], sys.argv[3])
