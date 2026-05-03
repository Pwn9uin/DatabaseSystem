class Node:
    def __init__(self):
        self.keys = []
        self.rids = []
        self.child = []
        self.parent = None
        self.is_leaf = True

class BTree:
    def __init__(self, order):
        self.root = Node()
        self.order = order
    
    def insert(self, key, rid):
        leaf = self.find_leaf(key, self.root)
        
        if leaf is None: return
        if key in leaf.keys: return
        

        i = 0
        flag = False
        for i in range(len(leaf.keys)):
            if key < leaf.keys[i] : 
                flag = True
                break
        
        if not flag : i = len(leaf.keys)
        
        leaf.keys.insert(i, key)
        leaf.rids.insert(i, rid)

        self.check_split(leaf)

    def check_split(self, node):
        if len(node.keys) <= 2*self.order : return

        midle_key = node.keys[self.order]        
        midle_rid = node.rids[self.order]

        right_keys = node.keys[self.order+1:]
        right_rids = node.rids[self.order+1:]

        right_child = node.child[self.order+1:]


        right_node = Node()
        right_node.keys = right_keys
        right_node.rids = right_rids
        right_node.child = right_child
        right_node.parent = node.parent
        right_node.is_leaf = node.is_leaf

        for child in right_node.child:
            child.parent = right_node

        node.keys = node.keys[:self.order]
        node.rids = node.rids[:self.order]
        node.child = node.child[:self.order+1]


        if node == self.root:
            new_root = Node()
            new_root.child.append(node)
            new_root.child.append(right_node)
            new_root.keys = [midle_key]
            new_root.rids = [midle_rid]
            new_root.is_leaf = False

            node.parent = new_root
            right_node.parent = new_root

            self.root = new_root
            return

        parent = node.parent

        i = 0
        flag = False
        for i in range(len(parent.keys)):
            if midle_key < parent.keys[i]: 
                flag = True
                break
        
        if not flag: i = len(parent.keys)

        parent.keys.insert(i, midle_key)
        parent.rids.insert(i, midle_rid)
        parent.child.insert(i+1, right_node)

        self.check_split(parent)



    def find_leaf(self, key, node):
        if node.is_leaf : return node
        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return self.find_leaf(key, node.child[i])

        return self.find_leaf(key, node.child[len(node.keys)])
    

    def search(self, key):
        return self._search(key, self.root)

    def _search(self, key, node):
        if node.is_leaf : 
            for i in range(len(node.keys)):
                if key == node.keys[i] : return node.rids[i]
            return -1

        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return node.rids[i]
            elif key < node.keys[i]:
                return self._search(key, node.child[i])
        
        return self._search(key, node.child[len(node.keys)])

    def find_node(self, key, node):
        if node.is_leaf:
            if key in node.keys: return node
            return None

        for i in range(len(node.keys)):
            if key == node.keys[i]:
                return node
            elif key < node.keys[i]:
                return self.find_node(key, node.child[i])
        
        return self.find_node(key, node.child[len(node.keys)])

    def delete(self, key):
        node = self.find_node(key, self.root)
        if node is None : return -1

        if node.is_leaf :
            idx = node.keys.index(key)
            node.keys.pop(idx)
            node.rids.pop(idx)
            self.check_underflow(node)

        else :
            s_node = self.find_successor(node.child[node.keys.index(key)+1])
            s_key = s_node.keys[0]
            s_rid = s_node.rids[0]

            t_idx = node.keys.index(key)
            node.keys[t_idx] = s_key
            node.rids[t_idx] = s_rid

            s_node.keys.pop(0)
            s_node.rids.pop(0)

            self.check_underflow(s_node)



    def find_successor(self, node):
        if node.is_leaf : 
            return node
        else :
            return self.find_successor(node.child[0])
    
    def check_underflow(self, node):
        if len(node.keys) >= self.order : return
        if node == self.root:
            if len(node.keys) == 0 :
                self.root = node.child[0]
                self.root.parent = None
            return
        
        parent = node.parent
        idx = parent.child.index(node)

        if idx > 0 : 
            left = parent.child[idx-1]
        else :
            left = None
        
        if idx < len(parent.child)-1:
            right = parent.child[idx+1]
        else:
            right = None

        if left is not None and len(left.keys) > self.order :
            ex_key = parent.keys.pop(idx-1)
            ex_rid = parent.rids.pop(idx-1)

            node.keys.insert(0, ex_key)
            node.rids.insert(0, ex_rid)


            left_key = left.keys.pop(len(left.keys)-1)
            left_rid = left.rids.pop(len(left.rids)-1)

            if left.child:
                ex_child = left.child.pop()
                node.child.insert(0, ex_child)
                ex_child.parent = node
            
            parent.keys.insert(idx-1, left_key)
            parent.rids.insert(idx-1, left_rid)

        elif right is not None and len(right.keys) > self.order:
            ex_key = parent.keys.pop(idx)
            ex_rid = parent.rids.pop(idx)

            node.keys.append(ex_key)
            node.rids.append(ex_rid)

            right_key = right.keys.pop(0)
            right_rid = right.rids.pop(0)

            if right.child:
                ex_child = right.child.pop(0)
                node.child.append(ex_child)
                ex_child.parent = node
            
            parent.keys.insert(idx, right_key)
            parent.rids.insert(idx, right_rid)

        else: # Merge
            if left is not None:
                node_keys = node.keys
                node_rids = node.rids
                
                parent_key = parent.keys.pop(idx-1)
                parent_rid = parent.rids.pop(idx-1)

                left.keys.append(parent_key)
                left.rids.append(parent_rid)

                left.keys = left.keys + node_keys
                left.rids = left.rids + node_rids

                for child in node.child:
                    child.parent = left

                left.child = left.child + node.child


            else:
                node_keys = node.keys
                node_rids = node.rids
                
                parent_key = parent.keys.pop(idx)
                parent_rid = parent.rids.pop(idx)

                right.keys = node_keys + [parent_key] + right.keys
                right.rids = node_rids + [parent_rid] + right.rids

                for child in node.child:
                    child.parent = right

                right.child = node.child + right.child

            parent.child.pop(idx)
        
            self.check_underflow(parent)

class BPlusNode:
    def __init__(self):
        self.keys = []
        self.rids = []
        self.child = []
        self.parent = None

        self.is_leaf = True
        self.next = None


class BPlusTree:
    def __init__(self, order):
        self.root = BPlusNode()
        self.order = order
    
    def search(self, key):
        return self._search(key, self.root)

    def _search(self, key, node):
        if node.is_leaf : 
            if key in node.keys: 
                return node.rids[node.keys.index(key)]
            else:
                return -1
        
        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return self._search(key, node.child[i])
            elif key == node.keys[i]:
                return self._search(key, node.child[i+1])
        
        return self._search(key, node.child[len(node.keys)])
    
    def find_leaf(self, key, node):
        if node.is_leaf :
            return node
        
        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return self.find_leaf(key, node.child[i])
            elif key == node.keys[i]:
                return self.find_leaf(key, node.child[i+1])
        
        return self.find_leaf(key, node.child[len(node.keys)])

    def leaf_split(self, node):
        if len(node.keys) <= self.order*2: return

        if node.is_leaf : #leaf_node : copy up
            midle_key = node.keys[self.order]
            
            right = BPlusNode()
            right.keys = node.keys[self.order:]
            right.rids = node.rids[self.order:]
            right.next = node.next
            right.is_leaf = True

            node.keys = node.keys[:self.order]
            node.rids = node.rids[:self.order]
            node.next = right

            if node == self.root:
                new_root = BPlusNode()
                new_root.is_leaf = False
                new_root.keys = [midle_key]
                new_root.child = [node, right]
                node.parent = new_root
                right.parent = new_root
                self.root = new_root
                return


            parent = node.parent
            idx = parent.child.index(node)
            parent.keys.insert(idx, midle_key)
            right.parent = parent
            parent.child.insert(idx+1, right)

            self.leaf_split(parent)

        else : # else push up
            midle_key = node.keys[self.order]

            right = BPlusNode()
            right.keys = node.keys[self.order+1:]
            right.is_leaf = False

            right.child = node.child[self.order+1:]
            for i in range(len(right.child)):
                right.child[i].parent = right

            node.keys = node.keys[:self.order]
            node.child = node.child[:self.order+1]

            if node == self.root:
                new_root = BPlusNode()
                new_root.is_leaf = False
                new_root.keys = [midle_key]
                new_root.child = [node, right]
                node.parent = new_root
                right.parent = new_root
                self.root = new_root
                return

            
            parent = node.parent
            idx = parent.child.index(node)
            parent.keys.insert(idx, midle_key)
            parent.child.insert(idx+1, right)
            right.parent = node.parent

            self.leaf_split(parent)


    def insert(self, key, rid):
        leaf = self.find_leaf(key, self.root)
        if key in leaf.keys : return
        
        i = 0
        flag = False
        for i in range(len(leaf.keys)):
            if key < leaf.keys[i] : 
                flag = True
                break
        
        if not flag : i = len(leaf.keys)
        
        leaf.keys.insert(i, key)
        leaf.rids.insert(i, rid)

        self.leaf_split(leaf)


    def check_underflow(self, node):
        if len(node.keys) >= self.order: return
        if node == self.root:
            if len(node.keys) == 0:
                self.root = node.child[0]
                self.root.parent = None
            return

        parent = node.parent
        idx = parent.child.index(node)

        if idx > 0:
            left = parent.child[idx-1]
        else: 
            left = None
        
        if idx < len(parent.child)-1:
            right = parent.child[idx+1]
        else:
            right = None

        if node.is_leaf : 
            if left is not None and len(left.keys) > self.order:
                ex_key = left.keys.pop()
                ex_rid = left.rids.pop()

                parent.keys[idx-1] = ex_key

                node.keys.insert(0, ex_key)
                node.rids.insert(0, ex_rid)

            elif right is not None and len(right.keys) > self.order:
                ex_key = right.keys.pop(0)
                ex_rid = right.rids.pop(0)

                parent.keys[idx] = right.keys[0]

                node.keys.append(ex_key)
                node.rids.append(ex_rid)

            else:
                if left is not None:
                    left.keys = left.keys + node.keys
                    left.rids = left.rids + node.rids
                    left.next = node.next

                    parent.child.pop(idx)
                    parent.keys.pop(idx-1)
                    self.check_underflow(parent)

                elif right is not None:
                    node.keys = node.keys + right.keys
                    node.rids = node.rids + right.rids
                    node.next = right.next

                    parent.child.pop(idx+1)
                    parent.keys.pop(idx)

                    self.check_underflow(parent)
        else : # internal node
            if left is not None and len(left.keys) > self.order :
                ex_key = parent.keys.pop(idx-1)

                node.keys.insert(0, ex_key)

                left_key = left.keys.pop(len(left.keys)-1)

                if left.child:
                    ex_child = left.child.pop()
                    node.child.insert(0, ex_child)
                    ex_child.parent = node
                
                parent.keys.insert(idx-1, left_key)

            elif right is not None and len(right.keys) > self.order:
                ex_key = parent.keys.pop(idx)

                node.keys.append(ex_key)

                right_key = right.keys.pop(0)

                if right.child:
                    ex_child = right.child.pop(0)
                    node.child.append(ex_child)
                    ex_child.parent = node
                
                parent.keys.insert(idx, right_key)
            
            else:
                if left is not None:
                    node_keys = node.keys
                    
                    parent_key = parent.keys.pop(idx-1)
                    left.keys = left.keys + [parent_key] + node_keys
                    
                    for child in node.child:
                        child.parent = left
                    parent.child.pop(idx)
                    left.child = left.child + node.child


                else:
                    node_keys = node.keys
                    
                    parent_key = parent.keys.pop(idx)
                    right.keys = node_keys + [parent_key] + right.keys

                    for child in node.child:
                        child.parent = right

                    parent.child.pop(idx+1)
                    right.child = node.child + right.child

                self.check_underflow(parent)




    def delete(self, key):
        leaf = self.find_leaf(key, self.root)
        if key not in leaf.keys : return -1

        idx = leaf.keys.index(key)
        leaf.keys.pop(idx)
        leaf.rids.pop(idx)

        self.check_underflow(leaf)

    def range_query(self, start, end):
        node = self.find_leaf(start, self.root)
        results = []
        while node is not None:
            for i in range(len(node.keys)):
                if node.keys[i] > end :
                    return results
                elif node.keys[i] >= start:
                    results.append(node.rids[i])
            node = node.next

        return results