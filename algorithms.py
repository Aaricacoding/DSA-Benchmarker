"""
algorithms.py — clean implementations of every benchmarked algorithm.
No library sorting used except for reference comparison.
"""

import heapq
from collections import deque


# ── Sorting ────────────────────────────────────────────────────────────────

def bubble_sort(arr: list) -> list:
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(arr: list) -> list:
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: list) -> list:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def quick_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def heap_sort(arr: list) -> list:
    a = arr[:]
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]


def timsort_builtin(arr: list) -> list:
    return sorted(arr)


# ── Searching ─────────────────────────────────────────────────────────────

def linear_search(data: tuple) -> int:
    arr, target = data
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1


def binary_search(data: tuple) -> int:
    arr, target = data
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def jump_search(data: tuple) -> int:
    import math
    arr, target = data
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return -1


def interpolation_search(data: tuple) -> int:
    arr, target = data
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[lo] == arr[hi]:
            return lo if arr[lo] == target else -1
        pos = lo + ((target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo]))
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


# ── Graph traversal ────────────────────────────────────────────────────────

def _make_adj(edges: list[tuple[int, int]], n: int) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def bfs(graph_data: tuple) -> list[int]:
    adj, start, n = graph_data
    visited = [False] * n
    order = []
    q = deque([start])
    visited[start] = True
    while q:
        node = q.popleft()
        order.append(node)
        for nb in adj[node]:
            if not visited[nb]:
                visited[nb] = True
                q.append(nb)
    return order


def dfs(graph_data: tuple) -> list[int]:
    adj, start, n = graph_data
    visited = [False] * n
    order = []

    def _dfs(v: int):
        visited[v] = True
        order.append(v)
        for nb in adj[v]:
            if not visited[nb]:
                _dfs(nb)

    _dfs(start)
    return order


def dfs_iterative(graph_data: tuple) -> list[int]:
    adj, start, n = graph_data
    visited = [False] * n
    order = []
    stack = [start]
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            order.append(v)
            for nb in reversed(adj[v]):
                if not visited[nb]:
                    stack.append(nb)
    return order
