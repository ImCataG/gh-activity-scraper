# shapes is a set of tuples, each tuple is a shape. A shape is a matrix of 0s, 1s and ?s.
# if you want to search for other patters, edit this file. also make sure the code under shapes does what you want.
shapes = set([
(
'??0??', 
'?010?',
'01110',
'?000?',
),

(
'?0?',
'010',
'010',
'010',
'010',
'?0?',
),

(
'?00?',
'0110',
'0110',
'?00?',
),

(
'?0??',
'010?',
'010?',
'0110',
'?00?',
),

(
'??0?',
'?010',
'?010',
'0110',
'?00?',
),

(
'??00?',
'?0110',
'0110?',
'?00??',
),

(
'?00??',
'0110?',
'?0110',
'??00?',
),
])

# rotate all shapes 90 degrees 3 times, if not in set, add them to a second set
rotated_shapes = set()
for shape in shapes:
    rotated_shapes.add(shape)
    for _ in range(3):
        shape = tuple(''.join(row) for row in zip(*reversed(shape)))
        rotated_shapes.add(shape)

# merge the sets
shapes = shapes.union(rotated_shapes)

