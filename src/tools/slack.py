import json, requests, datetime

class Slack:
    def __init__(self, webhook_url, project, channel):
        self.webhook_url = webhook_url
        self.project=project
        self.channel=channel

    def send_message(self, job_name, logs):
        message = {'channel':self.channel,
        'blocks':[
            {'type':'section','text':{'type':'mrkdwn','text':'*Error in Job '+ job_name + ' in ' + self.project + '*'}},
            {'type':'section','text':{'type':'plain_text','text': logs}}
        ]}
        response = requests.post(
            self.webhook_url, data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            return False
            print (datetime.datetime.now(),'slack return an error %s, respose is:\n%s' % (response.status_code, response.text))
        else:
            print (datetime.datetime.now(),'notification sent')
            return True
