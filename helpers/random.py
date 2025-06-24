import random
class numeros:
    def numero():
            num = ''
            for _ in range(5):
                num += str(random.randrange(0, 9))
            return num