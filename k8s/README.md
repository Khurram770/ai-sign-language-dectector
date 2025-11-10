# Kubernetes Deployment Files

This directory contains Kubernetes manifests for deploying the Sign Language Detector application.

## Files

- `deployment.yaml` - Kubernetes Deployment manifest
- `service.yaml` - Kubernetes Service manifest
- `configmap.yaml` - Configuration map for environment variables
- `ingress.yaml` - Ingress manifest for external access (optional)

## Quick Start

1. **Build and push Docker image:**
   ```bash
   docker build -t your-registry/sign-language-detector:latest .
   docker push your-registry/sign-language-detector:latest
   ```

2. **Update image in deployment.yaml:**
   ```yaml
   image: your-registry/sign-language-detector:latest
   ```

3. **Deploy to Kubernetes:**
   ```bash
   kubectl apply -f configmap.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f ingress.yaml  # Optional
   ```

4. **Verify deployment:**
   ```bash
   kubectl get pods -l app=sign-language-detector
   kubectl get service sign-language-detector-service
   ```

5. **Access the application:**
   ```bash
   # Port forward
   kubectl port-forward service/sign-language-detector-service 5000:80
   
   # Or use LoadBalancer external IP
   kubectl get service sign-language-detector-service
   ```

## Camera Access

For camera access in Kubernetes, ensure:

1. Camera device is available on the node
2. Pod has access to `/dev/video0` (or appropriate device)
3. Use nodeSelector to schedule on nodes with cameras
4. Consider using DaemonSet for better camera access

## Configuration

Edit `configmap.yaml` to change configuration:

```yaml
data:
  CAMERA_INDEX: "0"
  TTS_ENABLED: "true"
  PORT: "5000"
```

Then apply:

```bash
kubectl apply -f configmap.yaml
kubectl rollout restart deployment/sign-language-detector
```

## Troubleshooting

See DEPLOYMENT.md for detailed troubleshooting guide.

