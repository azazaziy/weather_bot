from random import randint

def filling(n):
    temp = set()
    while len(temp) != n:
        temp.add(randint(1,n*2))
    return temp

def generating_mass(mass):
    generated_mass = []
    temp = []
    for n in mass:
        temp = [*filling(n)]
        generated_mass.append(temp)
    return generated_mass

def sorting(mass):
    i = 0
    for item in mass:
        item = item.sort(reverse = (1==i%2))
        i += 1
    return mass

def creating(n):
    mass = filling(n)
    temp = generating_mass(mass)
    answer = sorting(temp)
    return answer

def start():
    n = int(input("Введите целое число:\t"))
    answer = creating(n)
    print(answer)

if __name__ == "__main__":
    start()
