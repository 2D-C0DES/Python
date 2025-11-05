class Animal:
    pass


class Pets(Animal):
    pass

class Dogs(Pets):

    @staticmethod
    def bark():
        print("Bhau Bhau.....!!!!")


a = Dogs()

a.bark()

