<div align="center">
  
  ![Banner- Memphis dev streaming  (2)](https://github.com/memphisdev/memphis.go/assets/107035359/8d671d72-8478-41d3-afe6-3658104340ff)

  
</div>

<div align="center">

  <h4>

**[Memphis](https://memphis.dev)** is an intelligent, frictionless message broker.<br>Made to enable developers to build real-time and streaming apps fast.

  </h4>
  
  <a href="https://landscape.cncf.io/?selected=memphis"><img width="200" alt="CNCF Silver Member" src="https://github.com/cncf/artwork/raw/master/other/cncf-member/silver/white/cncf-member-silver-white.svg#gh-dark-mode-only"></a>
  
</div>

<div align="center">
  
  <img width="200" alt="CNCF Silver Member" src="https://github.com/cncf/artwork/raw/master/other/cncf-member/silver/color/cncf-member-silver-color.svg#gh-light-mode-only">
  
</div>
 
 <p align="center">
  <a href="https://memphis.dev/pricing">Cloud</a> - <a href="https://memphis.dev/docs/">Docs</a> - <a href="https://twitter.com/Memphis_Dev">Twitter</a> - <a href="https://www.youtube.com/channel/UCVdMDLCSxXOqtgrBaRUHKKg">YouTube</a>
</p>

<p align="center">
<a href="https://discord.gg/WZpysvAeTf"><img src="https://img.shields.io/discord/963333392844328961?color=6557ff&label=discord" alt="Discord"></a>
<a href="https://github.com/memphisdev/memphis/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/memphisdev/memphis?color=6557ff"></a> 
  <img src="https://img.shields.io/npm/dw/memphis-dev?color=ffc633&label=installations">
<a href="https://github.com/memphisdev/memphis/blob/master/CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/Code%20of%20Conduct-v1.0-ff69b4.svg?color=ffc633" alt="Code Of Conduct"></a> 
<a href="https://docs.memphis.dev/memphis/release-notes/releases/v0.4.2-beta"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/memphisdev/memphis?color=61dfc6"></a>
<img src="https://img.shields.io/github/last-commit/memphisdev/memphis?color=61dfc6&label=last%20commit">
</p>

Memphis.dev is more than a broker. It's a new streaming stack.<br><br>
It accelerates the development of real-time applications that require<br>
high throughput, low latency, small footprint, and multiple protocols,<br>with minimum platform operations, and all the observability you can think of.<br><br>
Highly resilient, distributed architecture, cloud-native, and run on any Kubernetes,<br>on any cloud without zookeeper, bookeeper, or JVM.

# Installation
After installing and running memphis broker,<br>
In your project's directory:

```shell
go get github.com/memphisdev/memphis.go
```

# Importing
```go
import "github.com/memphisdev/memphis.go"
```

### Connecting to Memphis
```go
c, err := memphis.Connect("<memphis-host>", 
	"<application type username>", 
	memphis.ConnectionToken("<connection-token>"), // you will get it on application type user creation
	memphis.Password("<password>")) // depends on how Memphis deployed - default is connection token-based authentication
```
<br>
It is possible to pass connection configuration parameters, as function-parameters.

```go
// function params
c, err := memphis.Connect("<memphis-host>", 
	"<application type username>", 
	memphis.ConnectionToken("<connection-token>"), // you will get it on application type user creation
	memphis.Password("<password>"), // depends on how Memphis deployed - default is connection token-based authentication
  memphis.AccountId(<int>) // You can find it on the profile page in the Memphis UI. This field should be sent only on the cloud version of Memphis, otherwise it will be ignored
  memphis.Port(<int>), // defaults to 6666       
	memphis.Reconnect(<bool>), // defaults to true
	memphis.MaxReconnect(<int>), // defaults to 10
  memphis.ReconnectInterval(<time.Duration>) // defaults to 1 second
  memphis.Timeout(<time.Duration>) // defaults to 15 seconds
	// for TLS connection:
	memphis.Tls("<cert-client.pem>", "<key-client.pem>",  "<rootCA.pem>"),
	)
```

Once connected, all features offered by Memphis are available.<br>

### Disconnecting from Memphis
To disconnect from Memphis, call Close() on the Memphis connection object.<br>

```go
c.Close();
```

### Creating a Station
**Unexist stations will be created automatically through the SDK on the first producer/consumer connection with default values.**<br><br>
Stations can be created from Conn<br>
Pass optional parameters by using provided functions<br>
_If a station already exists nothing happens, the new configuration will not be applied_<br>

```go
s0, err = c.CreateStation("<station-name>")

s1, err = c.CreateStation("<station-name>", 
 memphis.RetentionTypeOpt(<Messages/MaxMessageAgeSeconds/Bytes/AckBased>), // AckBased - cloud only
 memphis.RetentionVal(<int>), 
 memphis.StorageTypeOpt(<Memory/Disk>), 
 memphis.Replicas(<int>), 
 memphis.IdempotencyWindow(<time.Duration>), // defaults to 2 minutes
 memphis.SchemaName(<string>),
 memphis.SendPoisonMsgToDls(<bool>), // defaults to true
 memphis.SendSchemaFailedMsgToDls(<bool>), // defaults to true
 memphis.TieredStorageEnabled(<bool>), // defaults to false
 memphis.PartitionsNumber(<int>), // default is 1 partition
 memphis.DlsStation(<string>) // defaults to "" (no DLS station) - If selected DLS events will be sent to selected station as well
)
```

### Retention Types
Retention types define the methodology behind how a station behaves with its messages. Memphis currently supports the following retention types:

```go
memphis.MaxMessageAgeSeconds
```

When the retention type is set to MAX_MESSAGE_AGE_SECONDS, messages will persist in the station for the number of seconds specified in the retention_value. 

```go
memphis.Messages
```

When the retention type is set to MESSAGES, the station will only hold up to retention_value messages. The station will delete the oldest messsages to maintain a retention_value number of messages.

```go
memphis.Bytes
```

When the retention type is set to BYTES, the station will only hold up to retention_value BYTES. The oldest messages will be deleted in order to maintain at maximum retention_vlaue BYTES in the station.

```go
memphis.AckBased // for cloud users only
```

When the retention type is set to ACK_BASED, messages in the station will be deleted after they are acked by all subscribed consumer groups.

### Retention Values

The unit of the `retention value` changes depending on the `retention type` specified. 

All retention values are of type `int`. The following units are used based on the respective retention type:

`memphis.MaxMessageAgeSeconds` is represented **in seconds**, <br>
`memphis.Messages` is a **number of messages** <br> 
`memphis.Bytes` is a **number of bytes**, <br>
With `memphis.AckBased`, the `retentionValue` is ignored. 

### Storage Types
Memphis currently supports the following types of messages storage:<br>

```go
memphis.Disk
```

When storage is set to DISK, messages are stored on disk.

```go
memphis.Memory
```

When storage is set to MEMORY, messages are stored in the system memory. <br>

### Destroying a Station
Destroying a station will remove all its resources (including producers and consumers).<br>

```go
err := s.Destroy();
```

### Creating a new Schema

```go
err := conn.CreateSchema("<schema-name>", "<schema-type>", "<schema-file-path>")
```

### Enforcing a Schema on an Existing Station

```go
err := conn.EnforceSchema("<schema-name>", "<station-name>")
```

### Deprecated - Attaching Schema
use EnforceSchema instead
```go
err := conn.AttachSchema("<schema-name>", "<station-name>")
```

### Detaching a Schema from Station

```go
err := conn.DetachSchema("<station-name>")
```

### Produce and Consume Messages
The most common client operations are producing messages and consuming messages.<br><br>
Messages are published to a station and consumed from it<br>by creating a consumer and calling its Consume function with a message handler callback function.<br>Consumers are pull-based and consume all the messages in a station<br> unless you are using a consumers group,<br>in which case messages are spread across all members in this group.<br><br>
Memphis messages are payload agnostic. Payloads are byte slices, i.e []byte.<br><br>
In order to stop receiving messages, you have to call ```consumer.StopConsume()```.<br>The consumer will terminate regardless of whether there are messages in flight for the client.

### Creating a Producer

```go
// from a Conn
p0, err := c.CreateProducer(
	"<station-name>",
	"<producer-name>",
) 

// from a Station
p1, err := s.CreateProducer("<producer-name>")
```

### Producing a message
Without creating a producer (receiver function of the connection struct).
```go
c.Produce("station_name_c_produce", "producer_name_a", []byte("Hey There!"), []memphis.ProducerOpt{}, []memphis.ProduceOpt{})
```

Creating a producer first (receiver function of the producer struct). Creating a producer and calling produce on it will increase the performance of producing messages.
```go
p.Produce("<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>", memphis.AckWaitSec(15)) // defaults to 15 seconds
```
Note: 
When producing a message using avro format([]byte or map[string]interface{}), int types are converted to float64. Type conversion of `Golang float64` equals `Avro double`. So when creating an avro schema, it can't have int types. use double instead.
E.g.
```
myData :=  map[string]interface{}{
"username": "John",
"age": 30
}
```
```
{
	"type": "record",
	"namespace": "com.example",
	"name": "test_schema",
	"fields": [
		{ "name": "username", "type": "string" },
		{ "name": "age", "type": "double" }
	]
}
```
Note:
When producing to a station with more than one partition, the producer will produce messages in a Round Robin fashion between the different partitions.

### Add headers

```go
hdrs := memphis.Headers{}
hdrs.New()
err := hdrs.Add("key", "value")
p.Produce(
	"<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>",
    memphis.AckWaitSec(15),
	memphis.MsgHeaders(hdrs) // defaults to empty
)
```

### Async produce
For better performance. The client won't block requests while waiting for an acknowledgment.

```go
p.Produce(
	"<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>",
    memphis.AckWaitSec(15),
	memphis.AsyncProduce()
)
```

### Sync produce
For better reliability. The client will block requests and will wait for an acknowledgment.

```go
p.Produce(
	"<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>",
    memphis.AckWaitSec(15),
	memphis.SyncProduce()
)
```

### Message ID
Stations are idempotent by default for 2 minutes (can be configured), Idempotency achieved by adding a message id

```go
p.Produce(
	"<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>",
    memphis.AckWaitSec(15),
	memphis.MsgId("343")
)
```


### Produce using partition key
The partition key will be used to produce messages to a spacific partition.

```go
p.Produce(
	"<message in []byte or map[string]interface{}/[]byte or protoreflect.ProtoMessage or map[string]interface{}(schema validated station - protobuf)/struct with json tags or map[string]interface{} or interface{}(schema validated station - json schema) or []byte/string (schema validated station - graphql schema) or []byte or map[string]interface{} or struct with avro tags(schema validated station - avro schema)>",
    memphis.ProducerPartitionKey(<string>)
)
```

### Destroying a Producer

```go
p.Destroy();
```

### Creating a Consumer

```go
// creation from a Station
consumer0, err = s.CreateConsumer("<consumer-name>",
  memphis.ConsumerGroup("<consumer-group>"), // defaults to consumer name
  memphis.PullInterval(<pull interval time.Duration), // defaults to 1 second
  memphis.BatchSize(<batch-size> int), // defaults to 10
  memphis.BatchMaxWaitTime(<time.Duration>), // defaults to 5 seconds, has to be at least 1 ms
  memphis.MaxAckTime(<time.Duration>), // defaults to 30 sec
  memphis.MaxMsgDeliveries(<int>), // defaults to 10
  memphis.ConsumerErrorHandler(func(*Consumer, error){})
  memphis.StartConsumeFromSeq(<uint64>)// start consuming from a specific sequence. defaults to 1
  memphis.LastMessages(<int64>)// consume the last N messages, defaults to -1 (all messages in the station)
)
  
// creation from a Conn
consumer1, err = c.CreateConsumer("<station-name>", "<consumer-name>", ...) 
```
Note:
When consuming from a station with more than one partition, the consumer will consume messages in Round Robin fashion from the different partitions.

### Passing a context to a message handler

```go
ctx := context.Background()
ctx = context.WithValue(ctx, "key", "value")
consumer.SetContext(ctx)
```

### Processing Messages
First, create a callback function that receives a slice of pointers to ```memphis.Msg``` and an error.<br><br>
Then, pass this callback into ```consumer.Consume``` function.<br><br>
The consumer will try to fetch messages every ```pullInterval``` (that was given in Consumer's creation) and call the defined message handler.

```go
func handler(msgs []*memphis.Msg, err error, ctx context.Context) {
	if err != nil {
		m := msgs[0]
		fmt.Println(string(m.Data()))
		m.Ack()
	}
}

consumer.Consume(handler, 
				memphis.ConsumerPartitionKey(<string>) // use the partition key to consume from a spacific partition (if not specified consume in a Round Robin fashion)
)
```

### Fetch a single batch of messages
```go
msgs, err := conn.FetchMessages("<station-name>", "<consumer-name>",
  memphis.FetchBatchSize(<int>) // defaults to 10
  memphis.FetchConsumerGroup("<consumer-group>"), // defaults to consumer name
  memphis.FetchBatchMaxWaitTime(<time.Duration>), // defaults to 5 seconds, has to be at least 1 ms
  memphis.FetchMaxAckTime(<time.Duration>), // defaults to 30 sec
  memphis.FetchMaxMsgDeliveries(<int>), // defaults to 10
  memphis.FetchConsumerErrorHandler(func(*Consumer, error){})
  memphis.FetchStartConsumeFromSeq(<uint64>)// start consuming from a specific sequence. defaults to 1
  memphis.FetchLastMessages(<int64>)// consume the last N messages, defaults to -1 (all messages in the station))
  memphis.FetchPartitionKey(<string>)// use the partition key to consume from a spacific partition (if not specified consume in a Round Robin fashion)
```

### Fetch a single batch of messages after creating a consumer
`prefetch = true` will prefetch next batch of messages and save it in memory for future Fetch() request<br>
Note: Use a higher MaxAckTime as the messages will sit in a local cache for some time before processing
```go
msgs, err := consumer.Fetch(<batch-size> int,
							<prefetch> bool,
							memphis.ConsumerPartitionKey(<string>) // use the partition key to consume from a spacific partition (if not specified consume in a Round Robin fashion)
							)
```

### Acknowledging a Message
Acknowledging a message indicates to the Memphis server to not <br>re-send the same message again to the same consumer or consumers group.

```shell
message.Ack();
```

### Delay the message after a given duration
Delay the message and tell Memphis server to re-send the same message again to the same consumer group. <br>The message will be redelivered only in case `Consumer.MaxMsgDeliveries` is not reached yet.

```go
message.Delay(<time.Duration>);
```

### Get headers 
Get headers per message
```go
headers := msg.GetHeaders()
```

### Get message sequence number
Get message sequence number
```go
sequenceNumber, err := msg.GetSequenceNumber()
```
### Destroying a Consumer

```go
consumer.Destroy();
```

### Check if broker is connected

```go
conn.IsConnected()
```
