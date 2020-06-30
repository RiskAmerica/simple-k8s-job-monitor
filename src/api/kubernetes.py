from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
import datetime

class KubernetesApi:
    def __init__(self):
        """
        Note that in cluster you'll use the in cluster config,
        meanwhile when you try it on your local, you'll use your own kubeconfig.
        """
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        self.configuration = client.Configuration()
        self.api_instance = client.BatchV1Api(client.ApiClient(self.configuration))
        self.pod_api_instance = client.CoreV1Api(client.ApiClient(self.configuration))

    def get_all_job_status(self, startdate):
        jobsVigentes=[]
        calculated_date = datetime.datetime.today() - datetime.timedelta(days=1) 
        try:
            jobs_list = self.api_instance.list_job_for_all_namespaces(watch=False)
        except ApiException as e:
            print ("Exception when calling CoreV1Api->list_job_for_all_namespaces: %s\n" % e)
        for cron_job in jobs_list.items:
            if cron_job.status.active is None:
                self.get_pod_job(cron_job)
                if cron_job.status.conditions[0].last_transition_time.tzinfo is not None:
                    cron_job.status.conditions[0].last_transition_time = cron_job.status.conditions[0].last_transition_time.replace(tzinfo=None)
                if cron_job.status.conditions[0].last_transition_time >= max([startdate,calculated_date]):
                    jobsVigentes.append(cron_job)
            else:
                print (datetime.datetime.now(),'job '+ cron_job.metadata.name + ' in execucion')
                jobsVigentes.append(cron_job)
        return jobsVigentes

    def get_logs_pod_job(self, job):
        try:
            labels= job.metadata.labels
            filtro='job-name==' + labels['job-name']
            pods=self.pod_api_instance.list_namespaced_pod(namespace=job.metadata.namespace,label_selector = filtro)
        except ApiException as e:
            print ("Exception when calling CoreV1Api->list_namespaced_cron_job: %s\n" % e)
        if pods.items!=[]:
            logs=""
            for container in pods.items[0].status.container_statuses:
                try:
                    logs_container=self.pod_api_instance.read_namespaced_pod_log(namespace=job.metadata.namespace,name=pods.items[0].metadata.name, container=container.name)
                except ApiException as e:
                    print ("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)
                    return False
                logs=logs+logs_container
            return logs
        else:
            log= str(datetime.datetime.now()) + ' error, cannot get pods for job ' + labels['job-name']
            print (log)
            return log
        #read_namespaced_pod_log

