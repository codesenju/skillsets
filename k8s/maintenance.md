## End
```bash
kubectl delete hpa redis skillsets && \
kubectl -n api scale sts pgmoviedb --replicas 0 && \
kubectl -n skillsets scale deploy skillsets --replicas 0 && \
kubectl -n skillsets scale sts redis --replicas 0 && \
kubectl scale deploy my-collector-cloudwatch-collector --replicas 0 -n opentelemetry-operator-system
```

## Start
```bash
kubectl -n api scale sts pgmoviedb --replicas 1 && \
kubectl -n skillsets scale deploy skillsets --replicas 1 && \
kubectl -n skillsets scale sts redis --replicas 1 && \
kubectl scale deploy my-collector-cloudwatch-collector --replicas 1 -n opentelemetry-operator-system
```