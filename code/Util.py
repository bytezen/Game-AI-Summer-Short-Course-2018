from pygame.math import Vector2

def truncate_ip(vec,limit):
    if vec.length_squared() > (limit * limit):
        vec.normalize_ip()
        vec.scale_to_length(limit)
    else:
        vec


if __name__ == '__main__':
    foo = Vector2(3,4)
    print(foo,foo.length())
    truncate_ip(foo, 2)
    print(foo, foo.length())
