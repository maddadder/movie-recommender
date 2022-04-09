cd /home/alice/git3/movie-recommender
python3 -m venv ../mrbif
source ../mrbif/bin/activate
pip install -r requirements.txt

cd /home/alice/git3/movie-recommender
source ../mrbif/bin/activate
#python test_flask_app.py
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask run


# just keep in mind this will reset after a period of time
kubectl patch svc acid-minimal-cluster --patch '{"spec": { "type": "NodePort", "ports": [ { "nodePort": 30001, "port": 5432, "protocol": "TCP", "targetPort": 5432 } ] } }'


