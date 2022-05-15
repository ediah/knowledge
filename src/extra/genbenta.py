from random import randint
from itertools import combinations
import numpy as np
import time

def fwht(v):
    n = len(v) // 2
    left = v[:n] + v[n:]
    right = v[:n] - v[n:]
    if n == 1:
        return [*left, *right]
    else:
        return np.array([*fwht(left), *fwht(right)])

def nl(v):
    d = np.zeros((len(v),))
    d[0] = 1
    walsh = d * len(v) - 2 * fwht(v)
    return (len(v) - np.abs(walsh).max()) // 2

def combnum(n, k):
    def fact(x):
        return x * fact(x - 1) if x > 1 else 1
    
    return fact(n) // (fact(k) * fact(n - k))

def genanf(s, cord, num):
    anf = ''
    for powers in combinations(''.join([str(i) for i in range(0, s)]), cord):
        if randint(0, 1) == 1:
            for i in powers:
                anf += f'x[{i}] * '
            anf = anf[:-3] + ' ^ '
            num -= 1
        if num == 0:
            break
    return anf[:-3]

def vectorize(s, f):
    args = [list(('{0:0' + str(s) + 'b}').format(i)) for i in range(2 ** s)]
    args = [list(map(int, args[i])) for i in range(2 ** s)]
    
    v = []
    for x in args:
        v += [eval(f)]
    return np.array(v)

def genbenta(s, maxiter = 10 ** 6):
    assert s % 2 == 0, 'Число аргументов должно быть чётным.'
    objective = 2 ** (s - 1) - 2 ** (s // 2 - 1)

    cmin = [randint(0, combnum(s, i)) for i in range(0, s // 2 + 1)]
    cmax = [randint(cmin[i], combnum(s, i)) for i in range(0, s // 2 + 1)]
    
    print('Генерирую с параметрами:')
    print(f'\tcmin = {cmin}\n\tcmax = {cmax}')
    
    start = time.time()
    for i in range(maxiter):
        cord = [randint(cmin[i], cmax[i]) for i in range(0, s // 2 + 1)]
        
        # Запрет бент-функций, являющихся линейными преобразованиями
        # других бент-функций
        cord[0] = 0
        cord[1] = 0
        ##
        
        anfparts = [genanf(s, i, cord[i]) for i in range(0, s // 2 + 1)]
        anf = ' ^ '.join(filter(lambda x: x != '', anfparts))

        v = vectorize(s, anf)
        
        if nl(v) == objective:
            print('Найдена бент-функция! Её векторное представление:')
            print(f'\t({"".join(list(map(str, v)))})')
            print(f'У меня ушло на это {round(time.time() - start, 2)} с.')
            return list(map(str, v))
    
    print(f'Не удалось сгенерировать бент-функцию за {maxiter} итераций.')
        
def gensbox(cin, cout):
    sparts = []
    
    for i in range(cout):
        # Заглушка на случай неудачной генерации
        while (part := genbenta(cin)) == None:
            part = genbenta(cin)
        
        sparts += [part]
    
    num = np.apply_along_axis(lambda x: int(''.join(x), 2), 1, np.array(sparts).T)
    per = [[f'{i:06b}'[0] + f'{i:06b}'[-1], f'{i:06b}'[1:-1]] for i in range(64)]
    
    dtype = [('row', int), ('column', int), ('val', int)]
    newt = np.array([(int(x[0], 2), int(x[1], 2), y) for x, y in zip(per, num)], dtype=dtype)
    sbox = np.sort(newt, order=['row', 'column']).reshape((4, 16))['val']
    
    for row in range(4):
        print(row, '&', ' & '.join(map(str, sbox[row])), '\\\\')
    
gensbox(6, 4)
