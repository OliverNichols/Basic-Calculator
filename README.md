## Calculator

This is a simple project used as a public built-in calculator for other projects.

### Example usage
```
import parser
result = parser.parse(script, ID)
```
Note: The `script` passed should be `str`, and `ID` may be any hashable identifier for a user (may be ignored for global use). Passing `ID` to the parser allows users to assign values to variables without overlap. 

If you need to get the value set for anyone's variables, use:
```
parser.env[ID].get(variable_name) # assuming user with ID has used the parser at all
```

### Functionality
A combination of any of the below may be used in the given script - all white space is ignored.

Base operations:
``` py
num + num
num - num
num * num
num / num
num ** num
num ( num ) # same as "num * num"
num e int # same as "num * 10 ** int"
```

Base comparators:
``` py
num == num
num != num
num < num
num <= num
num > num
num >= num
```

Built-in mathematical functions:
``` py
sqrt ( num )
exp ( num ) # exponent 
log ( num ) # natural log
```

Setters and getters:
``` py
var_name = num
var_name # returns the value stored in var_name
```