
class Subroutine(object):
    """
    Subroutines are modular algorithms that have
    internal states and iteract with the main alglrithm
    through input of prices/time and output of decisions
    init -> update (price/time) * N ->  output (terminate, buy/sell)
    importantly, a subroutine traces one instrument
    """
    def __init__(self, inst, unit,**kwargs):
        self.inst=inst
        self.unit=unit
        self.init(**kwargs)

    def init(self,**kwargs):
        for k, v in kwargs.items():
            setattr(self,k,v)
        return

    def update(self, instUpdate=False):
        pass

    def output(self):
        """
        none -> terminated
        positive amount -> buy
        negative amount -> sell
        """
        return None
