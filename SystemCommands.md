Start Kafka  
Use Command Prompt 
   D:
   cd D:\kafka
   set KAFKA_HEAP_OPTS=-Xmx1G -Xms1G
   bin\windows\kafka-server-start.bat config\broker.properties



Start Consumer.py (PowerShell)
   D:
   cd D:\FeatureStore
   python consumer.py

Start Producer.py (PowerShell)
   D:
   cd D:\FeatureStore
   python producer.py



#Topic commands 
Delete : 
cd D:\kafka
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --delete --topic transactions --bootstrap-server localhost:9092 

Recreate :
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092
cd D:\kafka


Verify: 
cd D:\kafka
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
