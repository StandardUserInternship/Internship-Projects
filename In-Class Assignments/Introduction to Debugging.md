# Introduction to Debugging
### Something is wrong with the following Python code, try to figure what the issue is and fix it.

    # Broken FizzBuzz
    for i in range(100):
        out = ''
        if i // 3 == 0:
            out += 'Fizz'
        elif i // 5 == 0:
            out += 'Buzz'
        else:
            out = i
        print(out)
