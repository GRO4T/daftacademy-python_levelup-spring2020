curl -X POST -vv -u trudnY:PaC13Nt http://localhost:8000/login

curl -X POST -vv -H "Content-Type: application/json;" -H "Cookie: session_token=928b88efd118bea58f23edd73bf869310308b4ce53de18b4ca78350cc72f3468;" -d '{"name":"Damian", "surename":"Kolaska"}' http://localhost:8000/patient

curl -X POST -vv -H "Content-Type: application/json;" -H "Cookie: session_token=928b88efd118bea58f23edd73bf869310308b4ce53de18b4ca78350cc72f3468;" -d '{"name":"Piotr", "surename":"Nowak"}' http://localhost:8000/patient

curl -X GET -vv -H "Cookie: session_token=928b88efd118bea58f23edd73bf869310308b4ce53de18b4ca78350cc72f3468;" http://localhost:8000/patient

curl -X DELETE -vv -H "Cookie: session_token=928b88efd118bea58f23edd73bf869310308b4ce53de18b4ca78350cc72f3468;" http://localhost:8000/patient/0

curl -X GET -vv -H "Cookie: session_token=928b88efd118bea58f23edd73bf869310308b4ce53de18b4ca78350cc72f3468;" http://localhost:8000/patient
