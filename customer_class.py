class Customer():
    def __init__(self, id, transaction, arrival):
        self.id = id
        self.transaction= transaction
        self.arrival= arrival
    def __str__(self):
        return f"Customer {self.id}"