docker-compose up --build -d

echo "Sleep a little bit for server to start \n"

sleep 10s

echo "Search request \n" >> out.txt

curl --request GET http://localhost:5004/search/distributed-systems >> out.txt

echo "\n" >> out.txt

echo "Search request \n" >> out.txt

curl --request GET http://localhost:5004/search/graduate-school >> out.txt

echo "\n" >> out.txt

echo "Lookup request \n" >> out.txt

curl --request GET http://localhost:5004/lookup/1 >> out.txt 

echo "\n" >> out.txt

echo "Buy request \n" >> out.txt

curl --request POST http://localhost:5004/buy/1 >> out.txt 

echo "Lookup request \n" >> out.txt

curl --request GET http://localhost:5004/lookup/1 >> out.txt 

docker-compose down -v --rmi all --remove-orphans