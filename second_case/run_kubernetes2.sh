kubectl apply -f logs-persistenvolumeclaim.yaml
kubectl apply -f airflow-rbac.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f requirements-configmap.yaml
kubectl apply -f airflow-envvars-configmap.yaml
kubectl apply -f airflow-webserver-service.yaml
kubectl apply -f airflow-webserver-deployment.yaml
kubectl apply -f airflow-scheduler-deployment.yaml

minikube service airflow-webserver