# Operations Runbook

This runbook provides troubleshooting steps and operational procedures for the Capstone application.

## Table of Contents

1. [Common Issues](#common-issues)
2. [Troubleshooting Steps](#troubleshooting-steps)
3. [Emergency Procedures](#emergency-procedures)
4. [Maintenance Tasks](#maintenance-tasks)

---

## Common Issues

### 1. Pod Crash Loop (CrashLoopBackOff)

**Symptoms:**
- Pods repeatedly restart
- Status shows `CrashLoopBackOff`

**Diagnosis:**
```bash
# Check pod status
kubectl get pods -n firstname-lastname

# View pod logs
kubectl logs <pod-name> -n firstname-lastname

# Describe pod for events
kubectl describe pod <pod-name> -n firstname-lastname
```

**Common Causes:**

#### A. Image Pull Error
```bash
# Check if image exists in ECR
aws ecr describe-images \
  --repository-name firstname-lastname/frontend \
  --region <REGION>

# Verify imagePullSecrets
kubectl get secret ecr-secret -n firstname-lastname -o yaml
```

**Solution:**
- Verify ECR repository exists
- Check AWS credentials in GitHub Secrets
- Ensure imagePullSecrets is correctly configured

#### B. Application Error
```bash
# Check application logs
kubectl logs <pod-name> -n firstname-lastname --tail=50
```

**Solution:**
- Review application code for errors
- Check environment variables
- Verify database connection

#### C. Health Check Failure
```bash
# Check probe configuration
kubectl get deployment <deployment-name> -n firstname-lastname -o yaml | grep -A 10 "livenessProbe"
```

**Solution:**
- Increase `initialDelaySeconds` if app takes longer to start
- Verify `/health` endpoint returns 200 status
- Check timeout values

---

### 2. Service Not Accessible

**Symptoms:**
- Cannot reach application via Ingress URL
- 503 Service Unavailable errors

**Diagnosis:**
```bash
# Check ingress status
kubectl get ingress -n firstname-lastname

# Describe ingress
kubectl describe ingress capstone-ingress -n firstname-lastname

# Check service endpoints
kubectl get endpoints -n firstname-lastname

# Check if pods are ready
kubectl get pods -n firstname-lastname -o wide
```

**Common Causes:**

#### A. No Ready Pods
```bash
# Check pod readiness
kubectl get pods -n firstname-lastname
```

**Solution:**
- Ensure pods pass readiness probes
- Check application health endpoint

#### B. Service Misconfiguration
```bash
# Verify service selectors match pod labels
kubectl get svc frontend-service -n firstname-lastname -o yaml
kubectl get pods -n firstname-lastname --show-labels
```

**Solution:**
- Ensure service selector matches pod labels exactly
- Verify target port matches container port

#### C. Ingress Not Working
```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress logs
kubectl logs -n ingress-nginx <ingress-controller-pod>
```

**Solution:**
- Verify ingress annotations
- Check DNS configuration
- Verify TLS certificate (if using HTTPS)

---

### 3. High Latency / Slow Response

**Symptoms:**
- Application responds slowly
- Timeout errors

**Diagnosis:**
```bash
# Check pod resource usage
kubectl top pods -n firstname-lastname

# Check pod events
kubectl describe pod <pod-name> -n firstname-lastname | grep -A 20 Events

# Check if pods are being throttled
kubectl describe pod <pod-name> -n firstname-lastname | grep -i throttl
```

**Common Causes:**

#### A. Resource Constraints
```bash
# View current resource limits
kubectl get deployment backend -n firstname-lastname -o yaml | grep -A 5 resources
```

**Solution:**
- Increase CPU/memory limits
- Scale deployment replicas:
```bash
  kubectl scale deployment backend -n firstname-lastname --replicas=3
```

#### B. Database Connection Issues
```bash
# Check backend logs for database errors
kubectl logs -f deployment/backend -n firstname-lastname | grep -i database
```

**Solution:**
- Verify database credentials in secrets
- Check database connection pool settings
- Verify database is accessible from cluster

#### C. Too Many Requests
**Solution:**
- Implement Horizontal Pod Autoscaler (HPA):
```bash
  kubectl autoscale deployment backend \
    -n firstname-lastname \
    --cpu-percent=70 \
    --min=2 \
    --max=10
```

---

### 4. Database Connection Failures

**Symptoms:**
- Backend returns "Database connection failed"
- 503 errors from backend API

**Diagnosis:**
```bash
# Check if database secret exists
kubectl get secret postgres-secret -n firstname-lastname

# View secret (base64 encoded)
kubectl get secret postgres-secret -n firstname-lastname -o yaml

# Check backend environment variables
kubectl exec -it <backend-pod> -n firstname-lastname -- env | grep DB_
```

**Solution:**
```bash
# Verify secret is correctly mounted
kubectl describe pod <backend-pod> -n firstname-lastname | grep -A 10 Mounts

# Test database connectivity from pod
kubectl exec -it <backend-pod> -n firstname-lastname -- \
  python -c "import psycopg2; conn = psycopg2.connect(host='...', database='...', user='...', password='...'); print('Connected!')"
```

---

### 5. CI/CD Pipeline Failures

**Symptoms:**
- GitHub Actions workflow fails
- Deployment doesn't update

**Common Failures:**

#### A. ECR Push Failed
```bash
# Check ECR repository exists
aws ecr describe-repositories --region <REGION>
```

**Solution:**
- Verify AWS credentials in GitHub Secrets
- Check ECR repository name matches workflow
- Ensure IAM permissions include ECR push

#### B. kubectl Apply Failed
**Solution:**
- Verify kubeconfig is correctly configured
- Check namespace exists
- Ensure proper RBAC permissions

#### C. Image Not Updating
**Solution:**
- Use `imagePullPolicy: Always` in deployment
- Or use git-sha tags instead of `latest`
- Delete pods to force pull:
```bash
  kubectl delete pods -l app=backend -n firstname-lastname
```

---

## Troubleshooting Steps

### Step-by-Step Debugging Process

1. **Check Overall Status**
```bash
   kubectl get all -n firstname-lastname
```

2. **Review Pod Status**
```bash
   kubectl get pods -n firstname-lastname -o wide
```

3. **Check Logs**
```bash
   # Current logs
   kubectl logs <pod-name> -n firstname-lastname
   
   # Previous container logs (if crashed)
   kubectl logs <pod-name> -n firstname-lastname --previous
```

4. **Describe Resources**
```bash
   kubectl describe pod <pod-name> -n firstname-lastname
   kubectl describe deployment <deployment-name> -n firstname-lastname
   kubectl describe service <service-name> -n firstname-lastname
```

5. **Execute Commands in Pod**
```bash
   kubectl exec -it <pod-name> -n firstname-lastname -- /bin/sh
```

6. **Check Events**
```bash
   kubectl get events -n firstname-lastname --sort-by='.lastTimestamp'
```

---

## Emergency Procedures

### Rollback Deployment
```bash
# View rollout history
kubectl rollout history deployment/backend -n firstname-lastname

# Rollback to previous version
kubectl rollout undo deployment/backend -n firstname-lastname

# Rollback to specific revision
kubectl rollout undo deployment/backend -n firstname-lastname --to-revision=2
```

### Scale Down (Emergency Stop)
```bash
# Scale to 0 replicas
kubectl scale deployment backend -n firstname-lastname --replicas=0
kubectl scale deployment frontend -n firstname-lastname --replicas=0
```

### Restart All Pods
```bash
# Rolling restart
kubectl rollout restart deployment/frontend -n firstname-lastname
kubectl rollout restart deployment/backend -n firstname-lastname
```

### Delete and Recreate
```bash
# Delete all resources
kubectl delete -f k8s/ -n firstname-lastname

# Recreate
kubectl apply -f k8s/ -n firstname-lastname
```

---

## Maintenance Tasks

### Update Application

1. Make code changes
2. Commit and push to `main` branch
3. GitHub Actions will automatically build and deploy
4. Monitor deployment:
```bash
   kubectl rollout status deployment/backend -n firstname-lastname
```

### Update Kubernetes Manifests
```bash
# Apply changes
kubectl apply -f k8s/ -n firstname-lastname

# Verify
kubectl get all -n firstname-lastname
```

### View Resource Usage
```bash
# Current usage
kubectl top pods -n firstname-lastname
kubectl top nodes

# Resource quotas (if configured)
kubectl describe resourcequota -n firstname-lastname
```

### Clean Up Old Images
```bash
# List images in ECR
aws ecr list-images \
  --repository-name firstname-lastname/backend \
  --region <REGION>

# Delete specific image
aws ecr batch-delete-image \
  --repository-name firstname-lastname/backend \
  --image-ids imageTag=<tag> \
  --region <REGION>
```

### Backup Database (if applicable)
```bash
# Export from PostgreSQL
kubectl exec -it <backend-pod> -n firstname-lastname -- \
  pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup.sql
```

---

## Health Check Endpoints

### Frontend
```bash
# Local test
curl http://localhost/health

# In cluster
kubectl exec -it <frontend-pod> -n firstname-lastname -- \
  wget -O- http://localhost/health
```

### Backend
```bash
# Local test
curl http://localhost:8000/health

# In cluster
kubectl exec -it <backend-pod> -n firstname-lastname -- \
  curl http://localhost:8000/health
```

---

## Useful Commands Reference
```bash
# Watch pod status
kubectl get pods -n firstname-lastname -w

# Follow logs
kubectl logs -f deployment/backend -n firstname-lastname

# Port forward for local testing
kubectl port-forward -n firstname-lastname svc/backend-service 8000:8000

# Copy files from pod
kubectl cp firstname-lastname/<pod-name>:/path/to/file ./local-file

# Run one-off command
kubectl run -it --rm debug --image=busybox --restart=Never -n firstname-lastname -- sh

# Check resource quotas
kubectl describe limits -n firstname-lastname
```

---

## Contact Information

For issues not covered in this runbook, contact:

**DevOps Team:**
- dan@tiberbu.com
- njoroge@tiberbu.com
- elvis@tiberbu.com

**Escalation Path:**
1. Check this runbook
2. Review GitHub Actions logs
3. Check application logs
4. Contact DevOps team
5. Escalate to mentors (Daniel, James, Elvis)