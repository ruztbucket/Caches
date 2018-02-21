class LFUCache:
    class Node:
        def __init__(self,key):
            """
            :type key: int
            """
            self.key = key
            self.back = None
            self.next = None
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.m1,self.m2,self.m3 = {},{},{}
        self.n = 0
        self.cap = capacity
        self.minF = 0        
        
    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.m1:
            return -1
        self.promote(key)
        return self.m1[key][0]
    def promote(self,key):
        """
        :type key: int        
        """
        oldF = self.m1[key][1]
        self.m1[key][1] = oldF+1
        allGone = self.m2Del(oldF,self.m3[key])
        if allGone and self.minF==oldF:
            self.minF = oldF+1
        self.m2Add(key)
        
    def m2Del(self,oldF,node):       
        """
        :type oldF: int
        :type node: Node
        :rtype Boolean
        """
        _list = self.m2[oldF]
        if _list[0] is _list[1]:
            _list[0],_list[0] = None,None
            return True
        elif _list[0] is node:
            _list[0] = _list[0].next
            _list[0].back = None
            return False
        elif _list[1] is node:
            _list[1] = _list[1].back
            _list[1].next = None
            return False
        else:
            before = node.back
            after = node.next
            before.next = after
            after.back = before
            return False
            
    def evict(self):        
        key = self.m2[self.minF][0].key
        self.m2Del(self.minF,self.m3[key])
        del self.m1[key]
        del self.m3[key]
        
    def m2Add(self,key):
        """
        :type key: int
        """
        freq = self.m1[key][1]
        if freq not in self.m2:
            self.m2[freq] = [None,None]
        _list = self.m2[freq]
        if _list[0] is None:
            _list[0] = self.Node(key)
            _list[1] = _list[0]
        else:
            _list[1].next = self.Node(key)
            _list[1].next.back = _list[1]
            _list[1] = _list[1].next        
        self.m3[key] = _list[1]        
    
    def freshAdd(self,key,value):
        """
        :type key: int
        :type value: int
        """
        self.m1[key] = [value,1]
        self.minF = 1
        self.n = self.n+1
        self.m2Add(key)        
        
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
                self.freshAdd(key,value)        
            else:
                self.evict()
                self.freshAdd(key,value)
        else:
            self.m1[key][0] = value
            self.promote(key)
                


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)