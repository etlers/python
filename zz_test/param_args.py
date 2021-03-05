"""
    *args
        - 파라미터를 몇개를 받을지 모르는 경우 사용한다. "args"는 튜플 형태로 전달된다.

    **kwargs
        - 파라미터 명을 같이 보낼 수 있다. "kwargs"는 딕셔너리 형태로 전달된다.
"""

def print_args(*args): 
    print(args)
    
    for p in args: 
        print(p)

def print_kwargs(**kwargs): 
    print(kwargs)
    print(kwargs.keys())
    print(kwargs.values())
    for name, value in kwargs.items(): 
        print("%s : %s" % (name, value))


print_args('a', 'b', 'c', 'd')
print_kwargs(first = 'a', second = 'b', third = 'c', fourth = 'd')
