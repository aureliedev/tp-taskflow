# TP — TaskFlow : Minikube → Helm → ECR → EKS

1. Tester l'application avec Docker Compose.
2. Construire les images API et frontend.
3. Charger les images dans Minikube.
4. Valider le Chart :
   `helm lint ./helm/taskflow`
5. Déployer TaskFlow avec Helm.
6. Créer les repositories ECR et pousser les images.
7. Créer le cluster EKS avec `eksctl`.
8. Réutiliser le même Chart avec `values-aws.yaml`.
9. Vérifier le Service `LoadBalancer`.
10. Activer/observer CloudWatch Container Insights.
11. Supprimer les ressources AWS à la fin du TP.
