mosquitto="garden"
helm uninstall telegraf-garden

helm uninstall garden-influxdb
helm uninstall grafana-garden

mosquittoPod=$(kubectl get pods -l app=$mosquitto-mosquitto -o jsonpath='{.items..metadata.name}')
kubectl delete svc $mosquittoPod

helm uninstall garden

kubectl get pods
kubectl get svc
kubectl get deployments
