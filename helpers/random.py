import random
class numbers_random:
    def number():
            number = ''
            for _ in range(5):
                number += str(random.randrange(0, 9))
            return number