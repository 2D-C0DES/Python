class vector:
    def __init__(self,l) -> None:
        self.l = l

    def __len__(self):
        return len(self.l)

a = vector([3,4,5])


print(f"the length of the vector is: {len(a)}")
