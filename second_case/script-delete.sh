kubectl delete -f airflow-rbac.yaml
kubectl delete -f postgres-service.yaml
kubectl delete -f postgres-deployment.yaml
kubectl delete -f requirements-configmap.yaml
kubectl delete -f airflow-envvars-configmap.yaml
kubectl delete -f airflow-webserver-service.yaml
kubectl delete -f airflow-webserver-deployment.yaml
kubectl delete -f airflow-scheduler-deployment.yaml
kubectl delete -f logs-persistenvolumeclaim.yaml

minikube stop