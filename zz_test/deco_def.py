def decorator(func):
    def wrapper(*args, **kwargs):
       
        print('전처리')   
        print(func(*args, **kwargs))
        print('후처리')
        
    return wrapper

@decorator
def example():
    return '함수'

example()