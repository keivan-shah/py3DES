# py3DES
A python3 implementation of the DES Algorithm.

The algorithm is writtern by referencing this awesome article: [The DES Algorithm Illustrated](http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm) by J. Orlin Grabbe.


## Usage
```
# The data passed can be a string of any length.
# The code adds some extra padding bits('0's) at the end to
# ensure blocks sizes of 64.

# encrypt with a string key. (string key length must be >4)
>>> des_encrypt(STRING, STRING_KEY)

# encrypt with a binary key.
# (key length must be 64 and it must contain only '0' and '1')
>>> des_encrypt(STRING, KEY, False)

# Similary the function to decrypt are named des_decrypt.

```
## Note

The code is written in `Python3` and will not work with previous versions of python.
