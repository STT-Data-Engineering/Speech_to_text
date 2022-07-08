from kafka import KafkaProducer
from json import dumps, loads
from time import sleep
from kafka import KafkaConsumer

class AllKafka():
    
    def __init__ (self):
        pass
    
    def create_producer(self):
        """
        A function that creates a Kafka producer
        """
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

        return producer
    
    def extract_sentence(self, path, start, end):
        """
        A function to extract sentence from a text file(s)
        """
        allSentence = []
        for i in range(start,end):
            file = open(path+'/data_%i.txt'%i,encoding="utf8")
            sentences = file.readlines()
            allSentence.extend(sentences)
        return allSentence

    def csv_to_list(self, data):
        "A function to include list of texts in csv"
        text_lis =[]
        for i in range(len(data)):
            text_lis.append(data["text"][i])

        return (text_lis)
    
    def create_consumer(self, topic):
        """
        A function to create a Kafka consumer
        """
        consumer = KafkaConsumer(topic,
                                 bootstrap_servers='localhost:9092',
                             value_deserializer=lambda x: loads(x.decode('utf-8')))
        return consumer
    
    def create_topic(self, topic):
        """
        A function to create topic in Kafka cluster
        """
        admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092", 
        client_id='test'
    )

        topic_list = []
        topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        return(admin_client.create_topics(new_topics=topic_list, validate_only=False))
    
    
if __name__ == "__main__":
    kf = AllKafka()