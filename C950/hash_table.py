class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Converts a key into an index for our hash table.
    def _hash(self, key):
        return key % self.size
    
    # Inserts a new item into the hash table.
    def insert(self, key, value):
        hash_key = self._hash(key)

        # Gets our bucket via hash key.
        bucket = self.table[hash_key]
        
        # Update key value pair if it's already in our bucket.
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # If key is not in our bucket add the key with value.
        bucket.append((key, value))
    
    # Looks up a key and returns its value if it's found.
    def lookup(self, key):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]
        
        for k, v in bucket:
            if k == key:
                return v
        return None