class Filter:
    def __init__(self, fromBlock, toBlock, provider, subscriber,terminator, endpoint, id):
        self.fromBlock = fromBlock
        self.toBlock = toBlock
        self.provider = provider
        self.subscriber = subscriber
        self.terminator = terminator
        self.endpoint = endpoint
        self.id = id
    