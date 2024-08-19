# Microservices-Demo

# Overview
A simplified version of a Movie booking application to demonstrate the Microservice architecture and how to manage it using Kubernetes.


- Movie Service: Provides information like movie ratings, title, etc.
- Booking Service: Provides booking information.
- Users Service: Provides movie suggestions for users by communicating with other services.

# Deployment

- Run the deployments for the services in the k8s folder

```bash
kubectl apply -f users_deployment.yaml
kubectl apply -f bookings_deployment.yaml
kubectl apply -f movies_deployment.yaml
```

To allow external traffic to the services, create an Ingress resource
```bash
kubectl apply -f service-ingress.yaml
```
