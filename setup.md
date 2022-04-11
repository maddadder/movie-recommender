### Setup
  - docs start here https://github.com/maddadder/postgres-operator/blob/master/docs/quickstart.md#deployment-options
  - Run the following
    ```
    git clone https://github.com/maddadder/postgres-operator
    cd postgres-operator
    microk8s helm3 install postgres-operator ./charts/postgres-operator
    #microk8s helm3 install postgres-operator-ui ./charts/postgres-operator-ui
    #microk8s kubectl port-forward svc/postgres-operator-ui 8081:80
    ```
    
    # create a Postgres cluster
    ```
    #cd into this folder
    microk8s kubectl create -f ./minimal-postgres-manifest.yaml
    # go get the secret of zalando.acid-minimal-cluster.credentials.postgresql.acid.zalan.do and save in docker file
    # rename Dockerfile.example to Dockerfile
    # build the image with the secret
    docker-compose build
    docker push 192.168.1.151:32000/movie-recommender:1.0.13
    microk8s helm3 install movie-recommender ./movie-recommender
    OR 
    helm upgrade movie-recommender ./movie-recommender
    #kubectl -n default expose deployment acid-minimal-cluster-0 --port=5432
    # get name of master pod of acid-minimal-cluster
    export PGMASTER=$(microk8s kubectl get pods -o jsonpath={.items..metadata.name} -l application=spilo,cluster-name=acid-minimal-cluster,spilo-role=master -n default)

    # set up port forward
    microk8s kubectl port-forward $PGMASTER 6432:5432 -n default
    ```
    # reinstalling
    - microk8s kubectl get pdb
    - then delete it if you get an error about an existing pdb
    - then run microk8s kubectl delete -f ./minimal-postgres-manifest.yaml
    - then run microk8s kubectl apply -f ./minimal-postgres-manifest.yaml


### patch postgress to use nodeport (if installed)
```
# just keep in mind this will reset after a period of time
kubectl patch svc acid-minimal-cluster --patch '{"spec": { "type": "NodePort", "ports": [ { "nodePort": 30001, "port": 5432, "protocol": "TCP", "targetPort": 5432 } ] } }'
```