import boto.ec2
import sys,json,time,os

"""
1. User specifies AWS credentials in a separate key file;
    arg1=ACCESS_KEY arg2=SECRETE_KEY arg3=INSTANCE_ID
2. User invokes termination script and pass the instance ID from command line;
    * python one_key_terminate.py arg1=ACCESS_KEY arg2=SECRETE_KEY arg3=INSTANCE_ID
3. Termination script shuts down AWS instance.
    * handle by script
4. Upon completion, the termination script returns message indicating whether the termination process has been completed successfully.
    * Print successful message at the end
    * Retrun True
"""

def main(AKEY, SKEY, instance_id):
    conn = boto.ec2.connect_to_region("us-east-1",
                                    aws_access_key_id=AKEY,
                                    aws_secret_access_key=SKEY)
    print "Prepare terminate " + instance_id
    instance = conn.terminate_instances(instance_ids=[instance_id])
    counter = 10
    while (instance[0].update() != 'terminated' or counter == 0):
        print "{}/10 Let's check again in 10sec".format(str(counter))
        time.sleep(10)
        counter -= 1
    print "Succesffuly terminated " + instance_id
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Help: arg1=Access key, arg2=secret key, arg3:instence_id"
    main(sys.argv[1], sys.argv[2], sys.argv[3])
