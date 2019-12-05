"""
This script is to enable a user to trigger mock health events for testing the netcool integration solution.
It allows a user to trigger events in a given account in a specified region
however many times a user would like.
"""

import boto3
import time
import sys
import json
import argparse

# try:
#     REGION = sys.argv[1]
# except IndexError as ex:
#     REGION = 'us-east-1'
#     print('Running script in us-east-1')
#
#
# try:
#     LOOPS = sys.argv[2]
# except IndexError as ex:
#     LOOPS = 1
#     print('Running with one loop')


def get_account_id():
    """
    gets the account id
    :return:
    """
    sts_client = boto3.client('sts', region_name=REGION)
    account_id = sts_client.get_caller_identity()["Account"]
    return account_id


def get_all_ec2_ids():
    """
    gets all ec2 ids in region in account
    :return: list of instance ids
    """
    ec2_client = boto3.client('ec2', region_name=REGION)
    instances = ec2_client.describe_instances()
    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    return instance_ids


def pull_instance_id(instance_ids, counter):
    """
    this exists to grab an instance ID from the list of IDs. It allows for lists of 0 length as well
    by creating
    :param instance_ids: list of instance ids
    :param counter: do you want the first or second entry?
    :return: the instance id
    """
    try:
        instance = instance_ids[counter]
    except IndexError as ex:
        print('not enough instances in this region. creating sample instance id')
        instance = 'i-00000000000000000'
    return instance


def create_detail(region, account_id, id1, id2):
    """
    creates the detail of the message
    :param region: region
    :param account_id: account id
    :param id1: first ec2 instance id
    :param id2: second ec2 instance id
    :return:
    """
    detail = {'eventArn': 'arn:aws:health:global::event/AWS_ABUSE_DOS_REPORT_3223324344_3243_234_34_34',
              'service': 'ABUSE',
              'eventTypeCode': 'AWS_ABUSE_DOS_REPORT',
              'eventTypeCategory': 'issue',
              'startTime': time.ctime(),
              'eventDescription':
                  [
                      {'language': 'en_US',
                       'latestDescription':
                           '[test] Denial of Service (DOS) attack has been reported '
                           'to have been caused by AWS resources in your account.'}
              ],
              'affectedEntities':
                  [
                      {'entityValue': 'arn:aws:ec2:{}:{}:instance/{}'.format(region, account_id, id1)},
                      {'entityValue': 'arn:aws:ec2:{}:{}:instance/{}'.format(region, account_id, id2)}
                  ]
              }
    return detail


def trigger_event(detail, id1, id2):
    """
    triggers the actual event by doing a put event api call
    :param detail: the detail of the message
    :param id1: instance id #1
    :param id2: instance id #2
    :return: response of the api call
    """
    event_client = boto3.client('events', region_name=REGION)
    response = event_client.put_events(
        Entries=[
            {
                'Time': time.ctime(),
                'Source': 'awsmock.health',
                'Resources': [
                    id1,
                    id2
                ],
                'DetailType': 'AWS Health Abuse Event',
                'Detail': detail
            },
        ]
    )
    return response


def main():
    """
    main function to run. this will trigger as many events as the user specifies in the region
    that they specify.
    :return:
    """
    error_list = {}
    account_id = get_account_id()
    instance_ids = get_all_ec2_ids()
    id1 = pull_instance_id(instance_ids, 0)
    id2 = pull_instance_id(instance_ids, 1)
    detail = create_detail(REGION, account_id, id1, id2)
    for loop in range(int(LOOPS)):
        trigger_response = trigger_event(json.dumps(detail), id1, id2)
        if trigger_response['ResponseMetadata']['HTTPStatusCode'] != 200:
            error_list[loop] = 'error in response of this loop'
    return error_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region')
    parser.add_argument('-l', '--loops')
    args = parser.parse_args()
    REGION = args.region
    LOOPS = args.loops
    main()
    print("Running")

