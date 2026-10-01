# TaskFlow — Kubernetes & AWS Student Kit

Projet fil rouge : application web de gestion de tâches.

Architecture :
Frontend → REST API FastAPI → PostgreSQL

Parcours :
Docker → Minikube → Helm → Amazon ECR → Amazon EKS → CloudWatch.

## Lancer localement

```bash
docker compose up --build
```

Frontend : http://localhost:8080
API : http://localhost:8000/docs

## Important

Les secrets réels et identifiants AWS ne doivent jamais être commités.
