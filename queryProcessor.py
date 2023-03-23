import collections





class termPartitionedIndex:
    
    def __init__(self, numberOfDocuments):
        self.documents = []
        self.invertedIndex = [collections.defaultdict(set) for _ in range(numberOfDocuments)]
        self.numberOfDocuments = numberOfDocuments
    
    
    
    def addDocument(self, document):
        documentID = len(self.documents)
        self.documents.append(document)
        
        for term in document[1].split():
            partition = hash(term) % self.numberOfDocuments
            self.invertedIndex[partition][term].add(documentID)
    
    
    
    def search(self, query):
        relevantDocuments = set()
        
        for term in query.split():
            partition = hash(term) % self.numberOfDocuments
            relevantDocuments.update(self.invertedIndex[partition][term])

        relevanceScores = collections.Counter()
        for document in relevantDocuments:
            documentTerms = set(self.documents[document][1].split())
            relevanceScores[document] = len(documentTerms & set(query.split()))
        
        return [(self.documents[document], score) for document, score in relevanceScores.most_common()]





class dynamicIndex:
    
    def __init__(self):
        self.documents = []
        self.invertedIndex = collections.defaultdict(set)
    
    
    
    def addDocument(self, document):
        documentID = len(self.documents)
        self.documents.append(document)
        
        for term in document[0].split():
            self.invertedIndex[term].add(documentID)
    
    
    
    def search(self, query):
        relevantDocuments = set()
        
        for term in query.split():
            relevantDocuments.update(self.invertedIndex[term])
        
        relevanceScores = collections.Counter()
        for document in relevantDocuments:
            documentTerms = set(self.documents[document][0].split())
        
        return [(self.documents[document], score) for document, score in relevanceScores.most_common()]
