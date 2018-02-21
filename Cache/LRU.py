class LRUCache:
    
    class Node:
        def __init__(self,key,value):
            """
            :type key: int
            :type value: int
            """
            self.key = key
            self.value = value
            self.back, self.next = None,None
        
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.cap = capacity
        self.n = 0
        self.head, self.tail = None,None
        self.m1 = {}

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.m1:
            return -1        
        self.promote(key)        
        return self.m1[key].value
    
    def promote(self,key):     
        """
        :type key: int
        """
        node = self.m1[key]
        self.rem(node)
        self.add(node)
    
    def rem(self,node):
        """
        :type node: Node
        """
        if self.tail == self.head:
            self.tail, self.head = None,None
        elif self.tail == node:
            self.tail = self.tail.back
            self.tail.next = None
        elif self.head == node:
            self.head = self.head.next
            self.head.back = None
        else:
            before, after = node.back, node.next
            before.next = after
            after.back = before
        del self.m1[node.key]              
        
    def add(self,node):
        """
        :type node: Node
        """
        if not self.tail:
            self.tail, self.head = node,node
        else:
            self.tail.next = node
            node.back = self.tail
            node.next = None
            self.tail = node 
        self.m1[node.key] = node
        
    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if not self.cap:
            return
        if key not in self.m1:
            if self.n<self.cap:
                self.n += 1
                node = self.Node(key,value)                
                self.add(node)
            else:
                self.rem(self.head)
                self.n += 1
                node = self.Node(key,value)                
                self.add(node)
        else:
            self.promote(key)
            self.m1[key].value = value                  

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)