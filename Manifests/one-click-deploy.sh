#!/ bin/bash

aws eks update-kubeconfig --region ap-south-1 --name Tasklist

kubectl apply -f storage_class.yaml

kubectl create namespace backend
kubectl create namespace auth
kubectl create namespace argocd

kubectl apply -f pvc.yaml

kubectl apply -f auth-configs.yaml
kubectl apply -f auth-secrets.yaml
kubectl apply -f backend-configs.yaml
kubectl apply -f backend-secrets.yaml
kubectl apply -f cluster-autoscaler.yaml

kubectl apply -f auth_deploy.yaml
kubectl apply -f backend_deploy.yaml

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f argo-secret.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
kubectl apply -f argocd.yaml