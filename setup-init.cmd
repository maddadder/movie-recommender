cd C:\git\movie-recommender
py -m venv ../mrbif
C:\git\mrbif\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install pipwin 
pipwin install psycopg2
pip install -r setup-init-requirements.txt

# just keep in mind this will reset after a period of time
# open Cygwin64 Terminal
kubectl patch svc acid-minimal-cluster --patch '{"spec": { "type": "NodePort", "ports": [ { "nodePort": 30001, "port": 5432, "protocol": "TCP", "targetPort": 5432 } ] } }' --namespace leenet

cd C:\git\movie-recommender
#to set the db once, run:
python flask_app/init_data.py
#python flask_app/train_svd_model.py
