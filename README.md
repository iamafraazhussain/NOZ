# NOZ

## Distributed indexing
Distributed indexing is a technique used to build and maintain an index of information across multiple computers or nodes, rather than on a single machine. In a distributed system, the index is partitioned and distributed among different nodes or machines, which allows the index to be built, maintained and searched more efficiently and effectively.

The working of distributed indexing involves the following steps:
- Partitioning: The first step in distributed indexing is to partition the data that needs to be indexed. This partitioning can be done based on any criteria such as geographical location, data type, or any other logical grouping.
- Indexing: Once the data is partitioned, each node in the system builds an index for its own partition of the data. This can be done using any indexing technique such as inverted indexing, hash-based indexing, or B-tree indexing.
- Merging: The indexes built by each node are then merged into a single global index. This can be done in different ways depending on the application and the indexing technique used.
- Distribution: The global index is then distributed back to each node in the system. Each node may receive a subset of the global index or a complete copy of the index.
- Query processing: When a query is issued, it is sent to all the nodes in the system. Each node processes the query using its local index and returns the results to the query coordinator. The coordinator then merges the results from all the nodes and returns the final result to the user.

The advantage of distributed indexing is that it allows for the efficient processing of large-scale data sets by distributing the work across multiple machines. This reduces the amount of time required to build and search the index, and also increases the scalability and fault-tolerance of the system.

#### Distributed indexing using Dynamic indexing
Dynamic indexing is a type of distributed indexing that allows for real-time indexing and querying of data as it is added or removed from the system. In dynamic indexing, documents are partitioned into smaller subsets, and each subset is indexed by a separate node in the network. As new documents are added or removed, the system automatically reorganizes the partitions and updates the indexes in real-time, allowing for immediate searchability of the newly added documents.
By using dynamic distributed indexing, it is possible to create a highly scalable and efficient system for indexing and searching large collections of documents. This approach allows for real-time updates and immediate searchability of new documents, making it ideal for applications such as search engines, e-commerce sites, and social media platforms.

###### Working of Dynamic indexing
- Partitioning: The documents are partitioned into smaller subsets, and each subset is assigned to a separate node in the network.
- Indexing: Each node indexes the documents in its subset, creating a local index for that subset.
- Merging: The local indexes are merged periodically to create a global index that includes all the documents in the collection.
- Querying: Queries are sent to the nodes in the network, and each node returns a list of documents that match the query. These results are combined to create a final list of matching documents.
- Updating: When new documents are added or removed from the collection, the system automatically reorganizes the partitions and updates the indexes in real-time.

#### Distributed indexing using Term-Partitioned indexing
Distributed indexing based on term-partitioned indexing is a technique used to distribute the indexing workload across multiple machines or nodes in a distributed system. In this approach, the index is partitioned into smaller subsets called term partitions. Each term partition is stored on a separate machine or node in the distributed system.
The basic idea behind term-partitioned indexing is to divide the document collection into smaller subsets and create a local index for each subset. A global index is then created by merging the local indexes of each subset. The local indexes are updated incrementally as new documents are added to the document collection. This approach provides scalability and improves the indexing and search performance of the system.

###### Working of Term-Partitioned indexing
- The document collection is divided into subsets based on some partitioning scheme. For example, a simple scheme could be to divide the documents based on their document ID or some other metadata.
- Each subset of documents is indexed separately using a local index. The local index is stored on a separate machine or node in the distributed system. The local index contains a subset of the terms in the document collection and the frequency of occurrence of each term in the subset of documents.
- Once all the local indexes are created, they are merged to create a global index. The global index contains all the terms in the document collection and the frequency of occurrence of each term in the entire document collection.
- The local indexes are updated incrementally as new documents are added to the document collection. When a new document is added, it is assigned to a subset based on the partitioning scheme used. The local index for the subset is updated with the terms and their frequency of occurrence in the new document. The global index is then updated by merging the updated local indexes.
- When a query is issued, it is broadcast to all the machines or nodes in the distributed system. Each machine or node searches its local index for the query terms and returns the relevant documents. The search results are then merged to provide a global set of search results.

By dividing the indexing workload into smaller subsets and distributing them across multiple machines or nodes, distributed indexing based on term-partitioned indexing provides a scalable solution for indexing and searching large document collections. It also provides fault tolerance and high availability, as the failure of a single machine or node does not affect the entire system.



