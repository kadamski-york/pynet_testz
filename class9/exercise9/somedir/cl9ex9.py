#!/usr/bin/env python

import mytest

def main():
    mytest.func1()
    mytest.func2()
    mytest.func3()

    x = mytest.MyClass('Steacie','010','342')
    x.hello()
    x.not_hello()

if __name__ == "__main__":
    main()
