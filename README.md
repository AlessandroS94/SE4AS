# SE4AS

[![GoPkg Widget]][GoPkg] [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/569/badge)](https://bestpractices.coreinfrastructure.org/projects/569)

<img src="https://github.com/kubernetes/kubernetes/raw/master/logo/logo.png" width="100">

![immagine](https://user-images.githubusercontent.com/27149998/116787367-dda68100-aaa3-11eb-81b5-2cf695e84b67.png)

![immagine](https://user-images.githubusercontent.com/27149998/116787378-f151e780-aaa3-11eb-9ad1-338098a3a565.png)

----

MACOS instruction

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
