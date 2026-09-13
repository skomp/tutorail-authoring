# Design

## Behavioural contract {#contract}

The limiter receives a client key and answers whether one request is allowed.

## Sharding {#sharding}

The shard count `K` fixes how many partitions the store keeps. This binding is
loaded for the TUTOR, never for the learner, so it introduces nothing.
