def generator():
    for i in range(3):        
        yield i

gen = generator()

print(next(gen))
print(next(gen))
print(next(gen))
#next(gen)    # StopInteration Error