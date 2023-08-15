
## Add repo
```bash
  # Add a private Git repository via HTTPS using username/password:
  argocd repo add https://git-codecommit.us-east-1.amazonaws.com/v1/repos/skillsets --username git --password secret
```
## Create argocd applications
```bash
# Only deployable on the cluster where argocd server is installed!
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-skillsets-api
  namespace: argocd
spec:
  destination:
    server: 'https://0807E0011E71891914718E9F1BC052A3.gr7.us-east-1.eks.amazonaws.com'
  source:
    repoURL: 'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/skillsets'
    path: kustomize/dev
    targetRevision: argocd
    kustomize:
      images:
      - SKILLSETS_API_IMAGE_NAME=codesenju/skillsets-api:latest
  project: uat
EOF

# Deployable anywhere!
argocd app create dev-skillsets \
    --repo 'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/skillsets' \
    --dest-server 'https://0807E0011E71891914718E9F1BC052A3.gr7.us-east-1.eks.amazonaws.com' \
    --path kustomize/dev \
    --revision argocd \
    --project uat \
    --kustomize-image 'SKILLSETS_API_IMAGE_NAME=codesenju/skillsets-api:cors'

```
### skillsets-ui
```bash
argocd app create uat-skillsets-ui \
    --repo 'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/skillsets' \
    --dest-server 'https://0807E0011E71891914718E9F1BC052A3.gr7.us-east-1.eks.amazonaws.com' \
    --path kustomize.ui/uat \
    --revision argocd \
    --project uat \
    --kustomize-image 'SKILLSETS_UI_IMAGE_NAME=codesenju/skillsets-ui:latest'

argocd app delete uat-skillsets-ui -y
```
## Clean up
```bash
# Option 1
cat <<EOF | kubectl delete -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-skillsets
  namespace: argocd
spec:
  destination:
    server: 'https://0807E0011E71891914718E9F1BC052A3.gr7.us-east-1.eks.amazonaws.com'
  source:
    repoURL: 'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/skillsets'
    path: kustomize/dev
    targetRevision: argocd
    kustomize:
      images:
      - SKILLSETS_API_IMAGE_NAME=codesenju/skillsets-api:cors
  project: uat
EOF

# Option 2
argocd app delete uat-skillsets -y
```