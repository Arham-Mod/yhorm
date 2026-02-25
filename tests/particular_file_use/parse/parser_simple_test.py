def outer():
    print("hello")
    inner()

def inner():
    print("inside")
    outer()
