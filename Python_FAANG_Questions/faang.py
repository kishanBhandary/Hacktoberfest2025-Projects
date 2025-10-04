"""
advanced_python_interview_qs.py

Top Advanced Python Interview Questions (Asked in Companies)
Each question: short explanation + example code (where relevant) + inline comments explaining the code.

Author: Mohit Kourav

"""


"""
FAANG Python Interview Prep Guide

This Python interview guide contains 30 advanced questions with clear explanations
and practical code examples, covering topics from Python internals, memory management,
concurrency, decorators, context managers, to FAANG-style coding problems like
LRU Cache, palindrome substring, and tree serialization.

Each question is explained step by step, followed by a working code snippet with
inline comments and output demonstrations, making it easy to understand and apply.

This resource is highly valuable for preparing for interviews at top tech companies,
helping you gain deep insights into Python’s behavior, optimize your code, and
confidently tackle challenging coding problems commonly asked in FAANG interviews.
"""



# ------------------------------
# 🧩 Language & Internals
# ------------------------------

def q_gil_explanation():
    """
    Q: How does Python’s Global Interpreter Lock (GIL) work?
       Why is it needed, and how does it affect multithreading?

    Explanation (concise, interview-ready):
    - The GIL is a mutex in CPython that protects access to Python objects,
      ensuring that only one native thread executes Python bytecode at a time.
    - It's needed because CPython's memory management (reference counting)
      is not thread-safe by itself — the GIL simplifies implementation.
    - Effect: Threads in Python cannot run CPU-bound bytecode in parallel.
      For I/O-bound tasks, threads switch during blocking syscalls and
      can still provide concurrency. For CPU-bound work use multiprocessing
      (separate processes, each with its own Python interpreter & memory).
    - Workarounds / tools:
        * multiprocessing (process parallelism)
        * C extensions (release GIL in C code for heavy compute)
        * PyPy / JIT (different tradeoffs)
        * Use native libraries (numpy) which do heavy work in C

    Short example: a CPU-bound threaded increment will not scale with threads.
    """
    import threading, time

    def busy_loop(iters):
        x = 0
        for _ in range(iters):
            x += 1
        return x

    # Don't run heavy loops here by default — this is just explanatory.
    print("GIL: CPU-bound threading doesn't speed up in CPython (use multiprocessing).")


def q_python_implementations():
    """
    Q: Difference between CPython, Jython, IronPython, and PyPy?

    - CPython: Reference implementation, written in C. Produces .pyc bytecode executed by CPython VM.
    - PyPy: Alternative interpreter with a JIT compiler; often faster for long-running pure Python workloads.
    - Jython: Runs on JVM, integrates with Java; no C-extensions support.
    - IronPython: Runs on .NET CLR, integrates with .NET languages.

    Use-cases:
    - Use CPython for wide ecosystem (C extensions).
    - Use PyPy when pure Python performance is needed and C extensions are not critical.
    - Use Jython/IronPython when tight Java/.NET integration is required.
    """
    pass


def q_execution_flow():
    """
    Q: What happens behind the scenes when you execute `python myscript.py`?

    Steps (high level):
    1. The interpreter starts and initializes runtime (GC, import system).
    2. Source file is read. If a compiled bytecode (.pyc) is present and up-to-date,
       it may be used; otherwise Python compiles source to bytecode.
    3. Bytecode is executed by CPython's evaluation loop (ceval.c) — FETCH, DECODE, EXECUTE.
    4. Modules imported are loaded, executed once, and cached in sys.modules.
    5. Memory management uses reference counting + cyclic GC to reclaim cycles.
    6. On exit, cleanup/atexit handlers run.

    Note: Tools like -O, -OO, and PYTHONPATH affect behavior.
    """
    pass


def q_memory_and_gc():
    """
    Q: How are Python objects stored in memory?
       Explain reference counting + garbage collection + memory pools.

    Key ideas:
    - CPython uses reference counting: each PyObject has a refcount; when it drops to 0,
      object memory is deallocated immediately.
    - Reference counting alone can't reclaim cyclic references; CPython adds a cyclic
      garbage collector (gc module) that periodically finds groups of objects that
      reference each other but are unreachable from roots.
    - For speed, CPython uses memory allocators / pools (obmalloc) for small objects to
      reduce fragmentation and speed allocation.
    - Practical implications: circular references with __del__ can leak; explicit
      break cycles or use weakref; refcount creates deterministic destruction for many objects.

    Example:
    """
    import gc
    a = []
    b = [a]
    a.append(b)  # creates a cycle
    # Breaking cycles manually:
    a.clear(); b.clear()
    # Or rely on gc.collect()
    gc.collect()


def q_is_vs_eq():
    """
    Q: What is the difference between `is` and `==` in Python?
       Why can `is` give surprising results for small integers or strings?

    Explanation:
    - `is` tests object identity (are two references pointing to the same object).
    - `==` tests value equality by invoking __eq__ (or falling back).
    - CPython interns some small integers (commonly -5..256) and some short strings,
      so `a is b` may be True for small ints or interned strings even if they were
      created separately. Don't use `is` to compare values; use `==`.

    Example:
    """
    a = 256; b = 256
    print("256 is 256 ->", a is b)  # often True (interned)
    a = 257; b = 257
    print("257 is 257 ->", a is b)  # often False
    x = "hello"; y = "hello"
    print("'hello' is 'hello' ->", x is y)  # often True (interned)
    x = "".join(["he", "llo"])
    print("'hello' created at runtime is 'hello' literal ->", x == "hello", x is "hello")


def q_mro_c3_linearization():
    """
    Q: Explain Python’s method resolution order (MRO) in multiple inheritance (C3).

    Explanation:
    - Python uses C3 linearization to compute a deterministic MRO for classes with multiple
      inheritance. It preserves local precedence order and monotonicity.
    - MRO decides the order in which base classes are searched for attributes/methods.
    - Use ClassName.mro() or inspect.getmro(ClassName) to view the MRO.

    Example:
    """
    class A: pass
    class B(A): pass
    class C(A): pass
    class D(B, C): pass
    print("MRO for D:", [c.__name__ for c in D.mro()])  # D, B, C, A, object







# ------------------------------
# ⚡ Performance & Optimization
# ------------------------------

def q_optimize_slow_program():
    """
    Q: How would you optimize a slow Python program?

    Checklist (interview-style):
    1. Profile: use cProfile / line_profiler to find hotspots.
    2. Algorithmic improvements: better algorithms/data-structures.
    3. Use built-ins / vectorized libs: list comprehensions, itertools, numpy for numeric ops.
    4. Reduce Python-level overhead: avoid repeated attribute lookups, local variables faster.
    5. Use caching/memoization where applicable (functools.lru_cache).
    6. For CPU-bound code: use multiprocessing or write C extension (Cython, pybind11).
    7. For I/O-bound: use asyncio or threads.
    8. Consider using PyPy or specialized libraries.

    Practical micro-optimizations:
    - store frequently used attributes to local variables
    - prefer 'for x in iterable' over index-based loops when possible
    """
    pass


def q_slots_demo():
    """
    Q: What are __slots__ in Python? How do they improve memory efficiency?

    Explanation:
    - By default, instances have __dict__ where attributes are stored (per-instance dict).
    - Defining __slots__ in a class replaces per-instance dict with a fixed set of
      attribute descriptors stored in a compact structure, saving memory and slightly
      speeding attribute access.
    - Limitations: instances cannot have arbitrary new attributes (only those in slots),
      cannot be weakly referenced by default unless '__weakref__' included.

    Example:
    """
    class NoSlots:
        def __init__(self, x, y):
            self.x = x; self.y = y

    class WithSlots:
        __slots__ = ("x", "y")
        def __init__(self, x, y):
            self.x = x; self.y = y

    a = NoSlots(1, 2)
    b = WithSlots(1, 2)
    print("NoSlots has __dict__:", hasattr(a, "__dict__"))
    print("WithSlots has __dict__:", hasattr(b, "__dict__"))


def q_copy_performance():
    """
    Q: Difference between deepcopy and shallow copy in performance-critical scenarios?

    - Shallow copy (copy.copy) copies references at top level; nested mutable objects
      are shared. It's cheap (shallow).
    - Deep copy (copy.deepcopy) recursively copies contents; can be expensive and slow.
    - For performance-critical code avoid deepcopy; prefer careful data layout,
      immutable structures, or manual copying where needed.
    """
    import copy
    a = [[1,2], [3,4]]
    sh = copy.copy(a)   # shallow
    dp = copy.deepcopy(a)  # deep
    print("shallow share nested:", sh[0] is a[0])
    print("deep copy nested different:", dp[0] is a[0])


def q_lazy_evaluation():
    """
    Q: How does lazy evaluation happen in Python (generators, iterators, yield)?

    - Generators produce items on demand using yield. They avoid building the whole
      result in memory and are lazy.
    - Iterators implement __iter__ and __next__ which produce items one-by-one.
    - Use cases: streaming large data, pipelines, memory efficiency.

    Example: generator expression vs list comprehension
    """
    gen = (i*i for i in range(5))  # lazy
    lst = [i*i for i in range(5)]  # eager
    print("generator yields:", next(gen))


def q_list_complexities():
    """
    Q: Why are Python’s lists more like dynamic arrays?
       Complexity of insertions/deletions at head vs tail?

    - Python list is a dynamic array (contiguous memory). Append/pop at end -> amortized O(1).
    - Insert/delete at head -> O(n) because all elements must be shifted.
    - Use collections.deque for O(1) append/pop at both ends, at cost of random access O(n).
    """
    from collections import deque
    d = deque()
    d.appendleft(1); d.append(2)
    print("deque example:", d)













# ------------------------------
# 🕸 Concurrency & Parallelism
# ------------------------------

def q_threading_vs_asyncio():
    """
    Q: Difference between multithreading, multiprocessing, and asyncio?

    - Multithreading: multiple threads in same process; in CPython GIL limits parallel
      Python-bytecode execution; good for I/O-bound tasks.
    - Multiprocessing: multiple processes, each with its own Python interpreter & memory;
      true parallelism for CPU-bound tasks; higher memory & IPC overhead.
    - asyncio: single-threaded cooperative concurrency using event loop; efficient
      for many concurrent I/O-bound coroutines (low memory footprint).
    """
    pass


def q_when_use_asyncio():
    """
    Q: In which scenario would you use asyncio over threading?

    - Use asyncio when you have many concurrent I/O-bound tasks (e.g., many sockets,
      http requests) and want low memory footprint and scalable concurrency.
    - Avoid when you need blocking third-party libraries unless you wrap them in executors.
    """
    pass


def q_multiprocessing_and_gil():
    """
    Q: How does Python’s multiprocessing bypass the GIL?

    - multiprocessing launches separate processes. Each process has its own interpreter
      and its own GIL. Because each process runs independently, CPU-bound tasks can run
      in parallel across CPUs/cores.
    - Communication uses IPC mechanisms (Pipes, Queues, SharedMemory, managers).
    """
    pass


def q_executor_difference():
    """
    Q: Difference between ThreadPoolExecutor and ProcessPoolExecutor?

    - ThreadPoolExecutor: uses threads (good for I/O-bound tasks).
    - ProcessPoolExecutor: uses processes (good for CPU-bound tasks).
    - Both expose similar APIs (submit, map). Beware of pickling overhead with processes.
    """
    pass












# ------------------------------
# 🏗️ Design & Advanced Features
# ------------------------------

def q_decorators_with_args():
    """
    Q: What are decorators and how do they work internally? Write a decorator that takes args.

    Explanation:
    - A decorator is a callable that takes a function and returns another callable.
    - Syntactic sugar: @decorator above function definition.
    - A decorator with arguments returns a decorator, which in turn returns a wrapper.

    Example: logging decorator with a message argument.
    """
    from functools import wraps

    def logger(msg):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"[{msg}] Calling {func.__name__}")
                res = func(*args, **kwargs)
                print(f"[{msg}] {func.__name__} returned {res}")
                return res
            return wrapper
        return decorator

    @logger("TRACE")
    def add(a, b):
        return a + b

    print("Decorator demo result:", add(2, 3))


def q_descriptors_demo():
    """
    Q: What are descriptors? Explain __get__, __set__, __delete__.

    Explanation:
    - A descriptor is an object attribute with binding behavior, implemented via methods:
      __get__(self, obj, objtype), __set__(self, obj, value), __delete__(self, obj).
    - Common descriptor use: properties, methods, staticmethod, classmethod.
    """

    class PositiveNumber:
        def __init__(self):
            self._name = "_val"

        def __get__(self, instance, owner):
            return instance.__dict__.get(self._name, 0)

        def __set__(self, instance, value):
            if value < 0:
                raise ValueError("value must be >= 0")
            instance.__dict__[self._name] = value

    class Account:
        balance = PositiveNumber()

        def __init__(self, bal=0):
            self.balance = bal

    a = Account(100)
    print("Balance via descriptor:", a.balance)
    try:
        a.balance = -10
    except ValueError as e:
        print("Descriptor prevents negative:", e)


def q_context_managers():
    """
    Q: How do context managers work? Explain __enter__/__exit__ and provide a custom example.

    - A context manager implements __enter__ and __exit__.
    - The 'with' statement calls __enter__(), assigns returned value (if any), and on exit,
      calls __exit__(exc_type, exc, tb) which can suppress exceptions by returning True.
    """

    class Timer:
        def __enter__(self):
            import time
            self.start = time.time()
            return self

        def __exit__(self, exc_type, exc, tb):
            import time
            self.end = time.time()
            print("Elapsed:", self.end - self.start)

    with Timer():
        sum(range(100000))


def q_weakref_usecase():
    """
    Q: What are weak references and why use them?

    - weakref.ref(obj) holds a reference that does not increase refcount.
    - Useful for caches or mappings where you don't want to keep objects alive
      solely because they are cached.
    """
    import weakref

    class Foo:
        pass

    f = Foo()
    r = weakref.ref(f)
    print("Weakref alive:", r() is not None)
    del f
    print("After deletion, weakref:", r())  # None


def q_monkey_patch_example():
    """
    Q: Explain monkey patching with an example.

    - Monkey patching is modifying modules/classes/functions at runtime.
    - Useful for tests or quick fixes, but can be dangerous in production.
    """
    import math
    original_sqrt = math.sqrt

    def fake_sqrt(x):
        return 42

    math.sqrt = fake_sqrt
    print("math.sqrt(9) after monkey patch:", math.sqrt(9))
    # restore
    math.sqrt = original_sqrt











# ------------------------------
# 🔐 System / Low-Level
# ------------------------------

def q_pass_by_object_reference():
    """
    Q: Why is Python considered pass-by-object-reference? Prove with an example.

    - In Python, arguments are references to objects (object references are passed by value).
    - Mutating a passed-in mutable object alters the caller's object; reassigning the parameter
      name in the function does not affect caller.

    Example:
    """
    def mutate(lst):
        lst.append(10)   # affects caller (mutation)

    def reassign(lst):
        lst = [0, 1]     # does NOT affect caller (rebinds local name)

    data = [1, 2, 3]
    mutate(data)
    print("After mutate (mutation visible):", data)
    reassign(data)
    print("After reassign (no change):", data)


def q_dict_hashing_and_immutable_keys():
    """
    Q: How does hashing work in Python dictionaries? Why must keys be immutable?

    - dict uses a hash table; keys are hashed via __hash__ and stored in slots.
    - For correctness, hash(key) must be immutable over the key's lifetime (so dict can find it).
    - Mutable keys like list are unhashable (TypeError).
    """
    d = {}
    d[(1,2)] = "ok"
    print("Tuple key hashed:", d[(1,2)])
    try:
        d[[1,2]] = "bad"
    except TypeError as e:
        print("List is unhashable:", e)


def q_string_interning():
    """
    Q: Explain interning of strings and its effect on memory.

    - Python interns (caches) some strings (identifiers, short strings, literals).
    - Interning reduces memory duplication and speeds up equality checks via 'is' sometimes.
    - Use sys.intern() to intern strings explicitly (useful in large-scale text processing).
    """
    import sys
    a = sys.intern("some_long_string_value")
    b = sys.intern("some_long_string_value")
    print("Interned strings identical by 'is':", a is b)


def q_closures_and_freevars():
    """
    Q: How does Python implement closures? What are free variables?

    - A closure captures variables from enclosing scopes; 'free variables' are those that are
      referenced in inner functions but not defined there.
    - Python stores them in function.__closure__ as cell objects.
    """
    def outer(x):
        def inner(y):
            return x + y
        return inner

    f = outer(10)
    print("closure call:", f(5))
    print("closure freevars:", f.__closure__[0].cell_contents)


def q_new_vs_init():
    """
    Q: What happens if you override __new__ vs __init__?

    - __new__(cls, ...) is responsible for creating and returning a new instance (it's a static method).
      It is called before __init__. Override __new__ to customize instance creation (immutable types).
    - __init__(self, ...) initializes the already-created instance.
    - Example: immutable objects (like tuple) customization needs __new__.
    """
    class MyInt(int):
        def __new__(cls, value):
            print("Allocating new MyInt")
            return super().__new__(cls, abs(value))  # always positive

    x = MyInt(-5)
    print("MyInt value:", x)









# ------------------------------
# 🧑‍💻 FAANG-Style Coding in Python
# ------------------------------

# 1) Implement an LRU Cache without using OrderedDict
class LRUNode:
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCacheManual:
    """
    LRUCache implemented using:
    - hashmap: key -> node
    - doubly linked list: head <-> ... <-> tail, most recent at tail
    - capacity eviction: remove head.next when full

    Methods:
    - get(key) -> value or -1
    - put(key, value)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = {}  # key -> node
        # dummy head & tail
        self.head = LRUNode()
        self.tail = LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        # remove node from list
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add_to_tail(self, node):
        # add node right before tail (most recent)
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def get(self, key):
        node = self.map.get(key)
        if not node:
            return -1
        # move to tail (most recent)
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_to_tail(node)
        else:
            if len(self.map) >= self.capacity:
                # evict least recently used (head.next)
                lru = self.head.next
                self._remove(lru)
                del self.map[lru.key]
            node = LRUNode(key, value)
            self.map[key] = node
            self._add_to_tail(node)


# 2) Longest Palindromic Substring O(n^2) (center expansion)
def longest_palindrome_center(s: str) -> str:
    """
    Expand-around-center algorithm:
    - For each index i, expand odd-length (i,i) and even-length (i,i+1).
    - Track longest.
    Complexity: O(n^2) time, O(1) extra space.
    """
    if not s:
        return ""
    start, end = 0, 0
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return l + 1, r - 1

    for i in range(len(s)):
        l1, r1 = expand(i, i)
        l2, r2 = expand(i, i+1)
        if r1 - l1 > end - start:
            start, end = l1, r1
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start:end+1]


# 3) Serialize and deserialize a binary tree (preorder with null marker)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def serialize(root: TreeNode) -> str:
    """Serialize tree to string using preorder and '#' as null sentinel."""
    vals = []
    def helper(node):
        if node is None:
            vals.append("#")
            return
        vals.append(str(node.val))
        helper(node.left)
        helper(node.right)
    helper(root)
    return ",".join(vals)

def deserialize(data: str) -> TreeNode:
    """Deserialize string back to tree (expects preorder with '#')."""
    vals = iter(data.split(","))
    def helper():
        val = next(vals)
        if val == "#":
            return None
        node = TreeNode(int(val))
        node.left = helper()
        node.right = helper()
        return node
    return helper()


# 4) Detect a deadlock in a multithreaded Python program (example + detection approach)
def deadlock_example_and_detection():
    """
    Demonstration of a simple deadlock and a strategy to detect it:
    - Two threads each try to acquire locks in opposite order -> deadlock.
    - Automatic detection: monitor thread states and lock ownership graph,
      detect cycles in resource allocation graph.
    - Simpler runtime detection: use timeouts when acquiring locks (try_acquire with timeout),
      and on timeout, log and recover.
    Note: actual detection requires OS-level or instrumentation; here we illustrate one approach.
    """
    import threading, time

    lock_a = threading.Lock()
    lock_b = threading.Lock()

    def t1():
        with lock_a:
            time.sleep(0.1)
            acquired = lock_b.acquire(timeout=1)
            if not acquired:
                print("t1: could not acquire lock_b -> possible deadlock")
                return
            lock_b.release()

    def t2():
        with lock_b:
            time.sleep(0.1)
            acquired = lock_a.acquire(timeout=1)
            if not acquired:
                print("t2: could not acquire lock_a -> possible deadlock")
                return
            lock_a.release()

    th1 = threading.Thread(target=t1)
    th2 = threading.Thread(target=t2)
    th1.start(); th2.start()
    th1.join(); th2.join()
    print("Deadlock demo complete (timeouts used to detect).")


# 5) Design a rate limiter (token bucket) — simple thread-safe implementation
import time
import threading

class TokenBucketRateLimiter:
    """
    Token bucket implementation:
    - capacity: maximum tokens in bucket
    - fill_rate: tokens per second added
    - tokens float for precision
    Thread-safe via a lock.
    """
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self._tokens = capacity
        self._last = time.time()
        self._lock = threading.Lock()

    def _add_tokens(self):
        now = time.time()
        elapsed = now - self._last
        self._last = now
        self._tokens = min(self.capacity, self._tokens + elapsed * self.fill_rate)

    def allow_request(self, tokens: float = 1.0) -> bool:
        with self._lock:
            self._add_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False








# ------------------------------
# Main demo runner (small)
# ------------------------------
if __name__ == "__main__":
    print("=== Advanced Python Interview Qs — Demo Run ===\n")

    # Language & internals demos
    q_is_vs_eq()
    q_mro_c3_linearization()
    q_memory_and_gc()

    # Performance demos
    q_slots_demo()
    q_copy_performance()
    q_lazy_evaluation()

    # Concurrency demos
    print("\n--- Concurrency demos ---")
    asyncio_demo = None
    try:
        # run asyncio example (safe)
        import asyncio
        async def _demo():
            async def t(n):
                await asyncio.sleep(0.01)
                return n
            res = await asyncio.gather(t(1), t(2))
            print("asyncio demo result:", res)
        asyncio.run(_demo())
    except Exception as e:
        print("asyncio demo skipped:", e)

    # Decorators and descriptors
    q_decorators_with_args()
    q_descriptors_demo()
    q_context_managers()
    q_weakref_usecase()
    q_monkey_patch_example()

    # System level
    q_pass_by_object_reference()
    q_dict_hashing_and_immutable_keys()
    q_string_interning()
    q_closures_and_freevars()
    q_new_vs_init()

    # Coding problems tests
    print("\n--- LRU Cache Manual test ---")
    cache = LRUCacheManual(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print("get(1):", cache.get(1))  # 1
    cache.put(3, 3)  # evicts key 2
    print("get(2):", cache.get(2))  # -1

    print("\n--- Longest Palindrome Demo ---")
    print(longest_palindrome_center("babad"))

    print("\n--- Serialize/Deserialize Tree Demo ---")
    tree = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), None))
    s = serialize(tree)
    print("Serialized:", s)
    root2 = deserialize(s)
    print("Deserialized root val:", root2.val)

    print("\n--- Deadlock detection demo (uses timeouts) ---")
    deadlock_example_and_detection()

    print("\n--- Rate limiter demo ---")
    limiter = TokenBucketRateLimiter(5, 1.0)  # 5 tokens max, 1 token/sec
    for i in range(7):
        print(f"request {i} allowed:", limiter.allow_request())
        time.sleep(0.2)

    print("\nDemo complete.")



