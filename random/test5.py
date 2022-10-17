
def example():
    for i in range(10):
        yield i
    
    return 'Done'


x=example()

try:
    while True:
        print(next(x))
except StopIteration as e:
    print(e.value)



