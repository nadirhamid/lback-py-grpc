class ShardedIterator(object):
    def __init__( self, count, total ):
        self.count = count
        self.total = total
    def get_count(self):
        return self.count
    def get_total(self):
        return self.total
    def increment_count(self):
        self.count += 1
