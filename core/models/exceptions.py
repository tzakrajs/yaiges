class AlreadyExists(RuntimeError):
    def __init__(self,*args,**kwargs):
        RuntimeError.__init__(self,*args,**kwargs)
