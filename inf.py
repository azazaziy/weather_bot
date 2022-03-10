for i in range(5):
    if i % 2 == 0:
        continue
    print(i)


x, y, z = (0, 1, 2, 3, 4, 5, 6, 7, 8)[1::3]
print(y)

x = int(input("Введите натуральное число: "))
n = ""
r = 2

while x > 0:
    y = str(x % r)
    n = y + n
    x = int(x / r)
    r = r + 1

print(n)
print(type(1/2))
x = ['I', 'like', 'to', 'study', 'at', 'ITMO']
print(x[4::-2])
