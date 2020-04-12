class gaParams:
	def __init__(self, f: str, 
		chromosoms_number: int, generations_number: int, 
		mutation: bool ,optimizer: str):

		self.f = f
		self.chromosoms_number = chromosoms_number
		self.generations_number = generations_number
		self.mutation = mutation
		self.optimizer = optimizer
