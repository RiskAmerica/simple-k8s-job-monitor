# simple-k8s-job-monitor
Based on https://github.com/irvifa/kubernetes-batch-api-example
## Build

```aidl
docker build -t <dockerimage-name>
```

After building the image you can run this in your local, remember to set environment variables SLACK_WEBHOOK_URL,CURRENT_PROJECT,CHANNEL

## Deployment

- Build
```
docker build -t <dockerimage-name>
```
- Push `Dockerimage`
- Change the fields of `$namespace` and `$imageName` in the deployments file, set the environment values
- You can use `kubectl apply -f k8s --recursive`
