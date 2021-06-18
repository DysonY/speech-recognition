from threading import Thread


def print_cube(n):
    print(f'Cube: {n**3}')


def print_square(n):
    print(f'Square: {n**2}')


if __name__ == '__main__':
    t1 = Thread(target=print_square, args=(10,))
    t2 = Thread(target=print_cube, args=(10,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
