class ShardedIterator(object):
    def __init__( self, count=None, total=None ):
        self.set_count( count )
        self.set_total( total )
    def get_count(self):
        return self.count
    def get_total(self):
        return self.total
    def get_count_as_string(self): 
        return self.to_string_value(self.count)
    def get_total_as_string(self): 
        return self.to_string_value(self.total)

    def set_count(self,count):
        self.count=count
    def set_total(self, total):
        self.total=total

    def increment_count(self):
        self.count += 1
    def to_string_value(self, value):
        if value is None:
           return value
        return str( value ) 
        
