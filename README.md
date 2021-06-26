# SE4AS


<img src="https://github.com/kubernetes/kubernetes/raw/master/logo/logo.png" width="100">

----

MACOS instruction:

cd SE4AS

cd Container-Code

cd Mosquitto-Broker && kubectl apply -f Mosquitto2

cd Sensor && kubectl apply -f deployment.yaml

cd Planning && kubectl apply -f deployment.yaml

cd Management && kubectl apply -f deployment.yaml

cd Executing && kubectl apply -f deployment.yaml

cd Analyzing && kubectl apply -f deployment.yaml

After deployed all deployment run this command

kubectl port-forward service/mosquitto 27000:9001

minikube service angular-service

With this command you can connect with the angular-dashboard to console
