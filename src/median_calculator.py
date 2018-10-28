from collections import deque
from sortedcontainers import SortedList


def median_window(phi, w_length):
    """Smooths a function 'phi' replacing each point with the median of the next 'w_length' points"""
    output = []

    queue = deque(phi[0:w_length], w_length)
    sorted_list = SortedList(phi[0:w_length])

    for phi_idx in range(w_length, len(phi)):
        left_idx = (w_length - 1) // 2
        right_idx = w_length // 2
        current_median = (sorted_list[left_idx] + sorted_list[right_idx]) / 2
        output.append(current_median)

        value_to_remove = queue.popleft()
        sorted_list.remove(value_to_remove)

        queue.append(phi[phi_idx])
        sorted_list.add(phi[phi_idx])

    return output
