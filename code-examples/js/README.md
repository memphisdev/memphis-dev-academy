<div align="center">
  
  ![Banner- Memphis dev streaming ](https://github.com/memphisdev/memphis.js/assets/70286779/e9899about:blank#blockedcdd-c78a-41d5-afb5-e5e053a540f0)

  
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
  <a href="https://memphis.dev/docs/">Docs</a> - <a href="https://twitter.com/Memphis_Dev">Twitter</a> - <a href="https://www.youtube.com/channel/UCVdMDLCSxXOqtgrBaRUHKKg">YouTube</a>
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

## Installation

```sh
$ npm install memphis-dev
```

Notice: you may receive an error about the "murmurhash3" package, to solve it please install g++
```sh
$ sudo yum install -y /usr/bin/g++
```

## Importing

For Javascript, you can choose to use the import or required keyword. This library exports a singleton instance of `memphis` with which you can consume and produce messages.

```js
const { memphis } = require('memphis-dev');
```

For Typescript, use the import keyword. You can import `Memphis` to aid for typechecking assistance.

```js
import { memphis, Memphis } from 'memphis-dev';
```

To leverage Nestjs dependency injection feature

```js
import { Module } from '@nestjs/common';
import { Memphis, MemphisModule, MemphisService } from 'memphis-dev';
```

### Connecting to Memphis

First, we need to connect with Memphis by using `memphis.connect`.

```js
/* Javascript and typescript project */
await memphis.connect({
            host: "<memphis-host>",
            port: <port>, // defaults to 6666
            username: "<username>", // (root/application type user)
            accountId: <accountId> //You can find it on the profile page in the Memphis UI. This field should be sent only on the cloud version of Memphis, otherwise it will be ignored
            connectionToken: "<broker-token>", // you will get it on application type user creation
            password: "<string>", // depends on how Memphis deployed - default is connection token-based authentication
            reconnect: true, // defaults to true
            maxReconnect: 10, // defaults to 10
            reconnectIntervalMs: 1500, // defaults to 1500
            timeoutMs: 15000, // defaults to 15000
            // for TLS connection:
            keyFile: '<key-client.pem>',
            certFile: '<cert-client.pem>',
            caFile: '<rootCA.pem>'
            suppressLogs: false // defaults to false - indicates whether to suppress logs or not
      });
```

Nest injection

```js
@Module({
    imports: [MemphisModule.register()],
})

class ConsumerModule {
    constructor(private memphis: MemphisService) {}

    startConnection() {
        (async function () {
            let memphisConnection: Memphis;

            try {
               memphisConnection = await this.memphis.connect({
                    host: "<memphis-host>",
                    username: "<application type username>",
                    connectionToken: "<broker-token>",
                });
            } catch (ex) {
                console.log(ex);
                memphisConnection.close();
            }
        })();
    }
}
```

Once connected, the entire functionalities offered by Memphis are available.

### Disconnecting from Memphis

To disconnect from Memphis, call `close()` on the memphis object.

```js
memphisConnection.close();
```

### Creating a Station
**Unexist stations will be created automatically through the SDK on the first producer/consumer connection with default values.**<br><br>
_If a station already exists nothing happens, the new configuration will not be applied_

```js
const station = await memphis.station({
    name: '<station-name>',
    schemaName: '<schema-name>',
    retentionType: memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS, // defaults to memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS
    retentionValue: 604800, // defaults to 604800
    storageType: memphis.storageTypes.DISK, // defaults to memphis.storageTypes.DISK
    replicas: 1, // defaults to 1
    idempotencyWindowMs: 0, // defaults to 120000
    sendPoisonMsgToDls: true, // defaults to true
    sendSchemaFailedMsgToDls: true, // defaults to true
    tieredStorageEnabled: false, // defaults to false
    partitionsNumber: 1, // defaults to 1
    dlsStation:'<station-name>' // defaults to "" (no DLS station) - If selected DLS events will be sent to selected station as well
});
```

Creating a station with Nestjs dependency injection

```js
@Module({
    imports: [MemphisModule.register()],
})

class stationModule {
    constructor(private memphis: MemphisService) { }

    createStation() {
        (async function () {
                  const station = await this.memphis.station({
                        name: "<station-name>",
                        schemaName: "<schema-name>",
                        retentionType: memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS, // defaults to memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS
                        retentionValue: 604800, // defaults to 604800
                        storageType: memphis.storageTypes.DISK, // defaults to memphis.storageTypes.DISK
                        replicas: 1, // defaults to 1
                        idempotencyWindowMs: 0, // defaults to 120000
                        sendPoisonMsgToDls: true, // defaults to true
                        sendSchemaFailedMsgToDls: true, // defaults to true
                        tieredStorageEnabled: false, // defaults to false
                        dlsStation:'<station-name>' // defaults to "" (no DLS station) - If selected DLS events will be sent to selected station as well
                  });
        })();
    }
}
```

### Retention types

Memphis currently supports the following types of retention:

```js
memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS;
```

Means that every message persists for the value set in retention value field (in seconds)

```js
memphis.retentionTypes.MESSAGES;
```

Means that after max amount of saved messages (set in retention value), the oldest messages will be deleted

```js
memphis.retentionTypes.BYTES;
```

Means that after max amount of saved bytes (set in retention value), the oldest messages will be deleted

```js
memphis.retentionTypes.ACK_BASED; // for cloud users only
```

Means that after a message is getting acked by all interested consumer groups it will be deleted from the Station.

### Retention Values

The unit of the `retention value` changes depending on the `retention type` specified. 

All retention values are of type `int`. The following units are used based on the respective retention type:

`memphis.retentionTypes.MAX_MESSAGE_AGE_SECONDS` is **in seconds**, <br>
`memphis.retentionTypes.MESSAGES` is a **number of messages**, <br>
`memphis.retentionTypes.BYTES` is a **number of bytes** <br>
With `memphis.retentionTypes.ACK_BASED`, the `retentionValue` is ignored.

### Storage types

Memphis currently supports the following types of messages storage:

```js
memphis.storageTypes.DISK;
```

When storage is set to DISK, messages are stored on disk.

```js
memphis.storageTypes.MEMORY;
```

When storage is set to MEMORY, messages are stored in the system memory.

### Destroying a Station

Destroying a station will remove all its resources (producers/consumers)

```js
await station.destroy();
```

### Creating a new schema 

```js
await memphisConnection.createSchema({schemaName: "<schema-name>", schemaType: "<schema-type>", schemaFilePath: "<schema-file-path>" });
```

### Enforcing a schema on an existing Station

```js
await memphisConnection.enforceSchema({ name: '<schema-name>', stationName: '<station-name>' });
```

### Deprecated - Use enforceSchema instead

```js
await memphisConnection.attachSchema({ name: '<schema-name>', stationName: '<station-name>' });
```

### Detaching a schema from Station

```js
await memphisConnection.detachSchema({ stationName: '<station-name>' });
```

### Produce and Consume messages

The most common client operations are `produce` to send messages and `consume` to
receive messages.

Messages are published to a station and consumed from it by creating a consumer.
Consumers are pull based and consume all the messages in a station unless you are using a consumers group, in this case messages are spread across all members in this group.

Memphis messages are payload agnostic. Payloads are `Uint8Arrays`.

In order to stop getting messages, you have to call `consumer.destroy()`. Destroy will terminate regardless
of whether there are messages in flight for the client.

### Creating a Producer

```js
const producer = await memphisConnection.producer({
    stationName: '<station-name>',
    producerName: '<producer-name>',
});
```

Creating producers with nestjs dependecy injection

```js
@Module({
    imports: [MemphisModule.register()],
})

class ProducerModule {
    constructor(private memphis: MemphisService) { }

    createProducer() {
        (async function () {
                const producer = await memphisConnection.producer({
                    stationName: "<station-name>",
                    producerName: "<producer-name>"
                });
        })();
    }
}
```

### Producing a message

Without creating a producer.
In cases where extra performance is needed, the recommended way is to create a producer first
and produce messages by using the produce function of it

```js
await memphisConnection.produce({
        stationName: '<station-name>',
        producerName: '<producer-name>',
        message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema) or Uint8Arrays/object (schema validated station - avro schema)
        ackWaitSec: 15, // defaults to 15
        asyncProduce: true // defaults to true. For better performance. The client won't block requests while waiting for an acknowledgment.
        headers: headers, // defults to empty
        msgId: 'id', // defaults to null
        producerPartitionKey: "key" // produce to specific partition.defaults to null
});
```

Creating a producer first

```js
await producer.produce({
    message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema) or Uint8Arrays/object (schema validated station - avro schema)
    ackWaitSec: 15, // defaults to 15,
    producerPartitionKey: "key" // produce to specific partition.defaults to null
});
```

Note:
When producing to a station with more than one partition, the producer will produce messages in a Round Robin fashion between the different partitions.

### Add Headers

```js
const headers = memphis.headers();
headers.add('<key>', '<value>');
await producer.produce({
    message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema)
    headers: headers // defults to empty
});
```

or

```js
const headers = { key: 'value' };
await producer.produce({
    message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema) or Uint8Arrays/object (schema validated station - avro schema)
    headers: headers
});
```

### Async produce

For better performance. The client won't block requests while waiting for an acknowledgment. Defaults to true.

```js
await producer.produce({
    message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema) or Uint8Arrays/object (schema validated station - avro schema)
    ackWaitSec: 15, // defaults to 15
    asyncProduce: true, // defaults to true. For better performance. The client won't block requests while waiting for an acknowledgment
    producerPartitionKey: "key" // produce to specific partition.defaults to null
});
```

### Message ID

Stations are idempotent by default for 2 minutes (can be configured). Idempotency is achieved by adding a message-id

```js
await producer.produce({
    message: 'Uint8Arrays/object/string/DocumentNode graphql', // Uint8Arrays/object (schema validated station - protobuf) or Uint8Arrays/object (schema validated station - json schema) or Uint8Arrays/string/DocumentNode graphql (schema validated station - graphql schema) or Uint8Arrays/object (schema validated station - avro schema)
    ackWaitSec: 15, // defaults to 15
    msgId: 'id' // defaults to null
});
```

### Destroying a Producer

```js
await producer.destroy();
```

### Creating a Consumer

```js
const consumer = await memphisConnection.consumer({
    stationName: '<station-name>',
    consumerName: '<consumer-name>',
    consumerGroup: '<group-name>', // defaults to the consumer name.
    pullIntervalMs: 1000, // defaults to 1000
    batchSize: 10, // defaults to 10
    batchMaxTimeToWaitMs: 5000, // defaults to 5000
    maxAckTimeMs: 30000, // defaults to 30000
    maxMsgDeliveries: 10, // defaults to 10
    startConsumeFromSequence: 1, // start consuming from a specific sequence. defaults to 1
    lastMessages: -1, // consume the last N messages, defaults to -1 (all messages in the station)
    consumerPartitionKey: "key", // consume by specific partition key. Defaults to null
});
```

Note:
When consuming from a station with more than one partition, the consumer will consume messages in Round Robin fashion from the different partitions.

### Passing context to message handlers

```js
consumer.setContext({ key: 'value' });
```

### Processing messages

```js
consumer.on('message', (message, context) => {
    // processing
    console.log(message.getData());
    message.ack();
});
```

### Fetch a single batch of messages

```js
const msgs = await memphis.fetchMessages({
    stationName: '<station-name>',
    consumerName: '<consumer-name>',
    consumerGroup: '<group-name>', // defaults to the consumer name.
    batchSize: 10, // defaults to 10
    batchMaxTimeToWaitMs: 5000, // defaults to 5000
    maxAckTimeMs: 30000, // defaults to 30000
    maxMsgDeliveries: 10, // defaults to 10
    startConsumeFromSequence: 1, // start consuming from a specific sequence. defaults to 1
    lastMessages: -1, // consume the last N messages, defaults to -1 (all messages in the station)
    consumerPartitionKey: "key", // consume by specific partition key. Defaults to null
});
```

### Fetch a single batch of messages after creating a consumer

```js
const msgs = await consumer.fetch({
    batchSize: 10, // defaults to 10
    consumerPartitionKey: "key", // consume by specific partition key. Defaults to null
});
```

To set up a connection in nestjs

```js
import { MemphisServer } from 'memphis-dev'

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      strategy: new MemphisServer({
        host: '<memphis-host>',
        username: '<application type username>',
        connectionToken: '<broker-token>'
      }),
    },
  );

  await app.listen();
}
bootstrap();
```

To consume messages in NestJS

```js
export class Controller {
    import { MemphisConsume, Message } from 'memphis-dev';

    @MemphisConsume({
        stationName: '<station-name>',
        consumerName: '<consumer-name>',
        consumerGroup: ''
    })
    async messageHandler(message: Message) {
        console.log(message.getData().toString());
        message.ack();
    }
}
```

### Acknowledge a message

Acknowledge a message indicates the Memphis server to not re-send the same message again to the same consumer/consumers group

```js
message.ack();
```

### Delay and resend the message after a given duration

Delay the message and tell the Memphis server to re-send the same message again to the same consumer group. The message will be redelivered only in case `Consumer.maxMsgDeliveries` is not reached yet.

```js
message.delay(delayInMilliseconds);
```

### Get message payload

As Uint8Array

```js
msg = message.getData();
```

As Json

```js
msg = message.getDataAsJson();
```

### Get headers

Get headers per message

```js
headers = message.getHeaders();
```

### Get message sequence number

Get message sequence number

```js
sequenceNumber = message.getSequenceNumber();
```

### Catching async errors

```js
consumer.on('error', (error) => {
    // error handling
});
```

### Stopping a Consumer 

Stopping a consumer simply stops it from consuming messages in the code. 

Let's say you don't want listeners of a consumer to receive messages anymore (even if messages are still being produced to its station), stop the consumer and that's it.

```js
await consumer.stop();
```

### Destroying a Consumer

This is different from stopping a consumer. Destroying a consumer destroys it from the station and the broker itself. It won't exist again.

```js
await consumer.destroy();
```

### Check if the broker is connected

```js
memphisConnection.isConnected();
```
