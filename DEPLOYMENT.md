# Deployment Guide

This guide explains how to deploy the Sign Language Detector application on Kubernetes and Docker.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Deployment

- Docker installed and running
- Camera device accessible (for local deployment)
- At least 2GB RAM available

### For Kubernetes Deployment

- Kubernetes cluster (v1.20+)
- kubectl configured
- Camera device accessible on cluster nodes (or use alternative input methods)
- Ingress controller (optional, for external access)

## Docker Deployment

### Build Docker Image

```bash
docker build -t sign-language-detector:latest .
```

### Run with Docker

```bash
docker run -d \
  --name sign-language-detector \
  -p 5000:5000 \
  --device=/dev/video0 \
  --privileged \
  -e CAMERA_INDEX=0 \
  -e TTS_ENABLED=true \
  sign-language-detector:latest
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Kubernetes Deployment

### Step 1: Build and Push Docker Image

```bash
# Build the image
docker build -t sign-language-detector:latest .

# Tag for your registry (replace with your registry)
docker tag sign-language-detector:latest your-registry/sign-language-detector:latest

# Push to registry
docker push your-registry/sign-language-detector:latest
```

### Step 2: Update Deployment Configuration

Edit `k8s/deployment.yaml` and update the image name:

```yaml
image: your-registry/sign-language-detector:latest
```

### Step 3: Deploy to Kubernetes

```bash
# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Create Deployment
kubectl apply -f k8s/deployment.yaml

# Create Service
kubectl apply -f k8s/service.yaml

# Create Ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

### Step 4: Verify Deployment

```bash
# Check deployment status
kubectl get deployment sign-language-detector

# Check pods
kubectl get pods -l app=sign-language-detector

# Check service
kubectl get service sign-language-detector-service

# View logs
kubectl logs -f deployment/sign-language-detector
```

### Step 5: Access the Application

#### Using LoadBalancer Service

```bash
# Get external IP
kubectl get service sign-language-detector-service

# Access via external IP
curl http://<EXTERNAL-IP>
```

#### Using Port Forwarding

```bash
kubectl port-forward service/sign-language-detector-service 5000:80
```

Then access at: `http://localhost:5000`

#### Using Ingress

Update `k8s/ingress.yaml` with your domain and apply:

```bash
kubectl apply -f k8s/ingress.yaml
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | `5000` |
| `HOST` | Bind host | `0.0.0.0` |
| `CAMERA_INDEX` | Camera device index | `0` |
| `TTS_ENABLED` | Enable text-to-speech | `true` |
| `FLASK_ENV` | Flask environment | `production` |
| `DEBUG` | Enable debug mode | `false` |

### Updating Configuration

#### Using ConfigMap (Kubernetes)

```bash
# Edit ConfigMap
kubectl edit configmap sign-language-detector-config

# Restart deployment to apply changes
kubectl rollout restart deployment/sign-language-detector
```

#### Using Environment Variables (Docker)

```bash
docker run -e CAMERA_INDEX=1 -e TTS_ENABLED=false sign-language-detector:latest
```

## Camera Access in Kubernetes

### Option 1: Host Path Volume (Node with Camera)

The deployment uses hostPath volumes to access camera devices:

```yaml
volumes:
- name: dev-video
  hostPath:
    path: /dev/video0
    type: CharDevice
```

**Requirements:**
- Camera must be connected to the Kubernetes node
- Pod must be scheduled on the node with the camera
- Use nodeSelector or nodeAffinity to ensure correct node

### Option 2: DaemonSet (Recommended for Camera Access)

For better camera access, use a DaemonSet:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: sign-language-detector
spec:
  selector:
    matchLabels:
      app: sign-language-detector
  template:
    spec:
      nodeSelector:
        camera: "available"  # Label nodes with cameras
      # ... rest of configuration
```

### Option 3: WebRTC (Alternative)

For remote camera access, consider implementing WebRTC to stream video from client browsers.

## Scaling

### Horizontal Scaling

The application can be scaled, but note:
- Each pod needs camera access (use DaemonSet)
- Or use a shared camera service
- Consider using a message queue for multiple instances

```bash
kubectl scale deployment sign-language-detector --replicas=3
```

### Resource Limits

Adjust resources in `k8s/deployment.yaml`:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

## Monitoring

### Health Checks

The application provides health check endpoint:

```bash
curl http://localhost:5000/api/health
```

### Logs

```bash
# Docker
docker logs sign-language-detector

# Kubernetes
kubectl logs -f deployment/sign-language-detector
```

### Metrics

Monitor resource usage:

```bash
kubectl top pods -l app=sign-language-detector
```

## Troubleshooting

### Camera Not Working

1. **Check camera device:**
   ```bash
   ls -la /dev/video*
   ```

2. **Test camera access:**
   ```bash
   docker run --rm --device=/dev/video0 ubuntu ls -la /dev/video0
   ```

3. **Check permissions:**
   ```bash
   # Kubernetes: Ensure privileged mode or proper device access
   # Docker: Use --device flag or --privileged
   ```

### Application Not Starting

1. **Check logs:**
   ```bash
   kubectl logs deployment/sign-language-detector
   ```

2. **Check health endpoint:**
   ```bash
   curl http://localhost:5000/api/health
   ```

3. **Verify dependencies:**
   ```bash
   kubectl exec -it deployment/sign-language-detector -- pip list
   ```

### Video Feed Not Loading

1. **Check camera availability:**
   ```bash
   kubectl exec -it deployment/sign-language-detector -- ls -la /dev/video*
   ```

2. **Test camera in container:**
   ```bash
   kubectl exec -it deployment/sign-language-detector -- python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
   ```

3. **Check network:**
   ```bash
   kubectl get endpoints sign-language-detector-service
   ```

### High Resource Usage

1. **Reduce video resolution:**
   Edit `app.py` and change camera resolution

2. **Adjust worker threads:**
   Edit Dockerfile CMD to reduce gunicorn workers

3. **Increase resource limits:**
   Update `k8s/deployment.yaml` resources section

## Security Considerations

1. **Camera Access:**
   - Use least privilege principle
   - Consider using device plugins
   - Isolate camera access

2. **Network:**
   - Use TLS/SSL for production
   - Implement authentication
   - Use network policies

3. **Resources:**
   - Set appropriate resource limits
   - Monitor resource usage
   - Implement auto-scaling

## Production Recommendations

1. **Use HTTPS:**
   - Configure TLS certificates
   - Use Ingress with TLS

2. **Implement Authentication:**
   - Add user authentication
   - Use OAuth or JWT

3. **Monitor and Log:**
   - Set up logging aggregation
   - Implement metrics collection
   - Set up alerts

4. **Backup and Recovery:**
   - Backup configuration
   - Implement disaster recovery
   - Test backup restoration

## Support

For issues or questions, please refer to the main README.md file or open an issue on the project repository.

