import os,datetime,time
from api.kubernetes import KubernetesApi
from tools.slack import Slack

webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
project = os.environ.get('CURRENT_PROJECT')
channel = os.environ.get('CHANNEL')
api = KubernetesApi()
slack_client = Slack(webhook_url,project,channel)

if __name__ == '__main__':
    print(startdate,'monitor started')
    jobsNotificados = []
    startdate = datetime.datetime.now()
    while True:
        jobsVigentes = api.get_all_job_status(startdate)
        for job in jobsVigentes:
            if job.status.failed is not None and job not in jobsNotificados:
                print(datetime.datetime.now(),'error in job ' + job.metadata.name + ', sending notification' )
                logs=api.get_logs_pod_job(job)
                if logs:
                    if slack_client.send_message(job.metadata.name,logs):
                        jobsNotificados.append(job)
        time.sleep(60)
