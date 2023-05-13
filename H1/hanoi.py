from typing import List
from stack import Stack

op_counter: int = 0
num_discs: int = 20
tower_a: Stack[int] = Stack()
tower_b: Stack[int] = Stack()
tower_c: Stack[int] = Stack()

for i in range(num_discs, 0, -1):
    tower_a.push(i)

def hanoi_validator(contents: List[int]) -> None:
    for (under, up) in zip(contents, contents[1:]):
        assert under > up, "Smaller discs cannot be under larger discs!"

def print_state(ctr: int = None):
    if ctr is not None:
        print(f"State after {ctr} operations")
    print(f"Start:     {tower_a}")
    print(f"End:       {tower_b}")
    print(f"Temporary: {tower_c}")

def hanoi(begin: Stack[int], end: Stack[int], temporary: Stack[int], n: int) -> None:
    global op_counter
    if n == 1:
        op_counter += 2
        end.push(begin.pop(), hanoi_validator)   # we're almost done - push the remaining (largest) disc to its final destination!
    else:
        hanoi(begin, temporary, end, n-1)
        hanoi(begin, end, temporary, 1)
        hanoi(temporary, end, begin, n-1)
    if not(op_counter % 500000):
        print_state(op_counter)


if __name__ == '__main__':
    print('=== START ===')
    print_state()
    hanoi(tower_a, tower_b, tower_c, num_discs)
    print('=== DONE ===')
    print_state()
    print(f"Number of operations required: {op_counter}")
