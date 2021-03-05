class Decorator:

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        print('전처리')
        print(self.function(*args, **kwargs))
        print('후처리')

@Decorator
def example():
    return '클래스'
    
example()