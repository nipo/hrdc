
class Stream(object):
    """
    A report descriptor item stream
    """
    
    def append(self, item):
        """
        Append the item to the report descriptor item stream
        """
        raise RuntimeError("unimplemented")

    def close(self):
        """
        Mark item stream as done
        """
        ...
