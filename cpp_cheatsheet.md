# C++ Coding Test Cheatsheet

> Scoped to the allowed headers:
> `<iostream>` · `<stdio.h>` · `<stdlib.h>` · `<string.h>` · `<unistd.h>` · `<sys/types.h>` · `<sys/resource.h>` · `<algorithm>` · `<vector>`

## Table of Contents

1. [Read This First](#1-read-this-first)
2. [Input / Output](#2-input--output)
3. [std::vector](#3-stdvector)
4. [`<algorithm>`](#4-algorithm)
5. [C Strings (`<string.h>`)](#5-c-strings-stringh)
6. [`<stdlib.h>`](#6-stdlibh)
7. [`<unistd.h>` and `<sys/types.h>`](#7-unistdh-and-systypesh)
8. [`<sys/resource.h>`](#8-sysresourceh)
9. [Handy Patterns](#9-handy-patterns)
10. [Common Pitfalls](#10-common-pitfalls)
11. [Compile and Debug](#11-compile-and-debug)

---

## 1. Read This First

### Not available with your headers

| Missing | Consequence | Workaround |
|---|---|---|
| `<string>` | `std::string` often works via `<iostream>`, but don't rely on it | Use `char[]` + `<string.h>` if it fails to compile |
| `<map>`, `<set>`, `<queue>`, `<stack>` | No `std::map`, `std::set`, `std::priority_queue`, etc. | Sorted `vector` + `lower_bound`, or `std::push_heap`/`pop_heap` from `<algorithm>` |
| `<numeric>` | No `std::accumulate`, `std::iota` | Manual loops |
| `<cmath>` | No `sqrt`, `pow`, etc. guaranteed | `<stdlib.h>` gives `abs`; write your own helpers |
| `<sys/wait.h>` | No `wait`/`waitpid` | Cannot reliably reap children, so avoid or check the task |
| `<functional>` | `std::greater` usually comes in through `<algorithm>`, but not guaranteed | Use a lambda instead |

### Tips

- Use the `std::` prefix everywhere (or `using namespace std;` if the test allows it).
- Prefer `"\n"` over `std::endl` (no forced flush, much faster).
- Prefer `std::vector` over raw arrays unless told otherwise.

---

## 2. Input / Output

### C++ streams

```cpp
int n;
std::cin >> n;
std::cout << n << "\n";
```

### C style

```cpp
int a; double d; char s[100];
scanf("%d %lf %99s", &a, &d, s);
printf("%d %.2f %s\n", a, d, s);
```

### Reading a whole line

```cpp
fgets(s, sizeof s, stdin);        // keeps the trailing '\n'
std::getline(std::cin, str);      // needs std::string
```

### printf / scanf format specifiers

| Spec | Type | Spec | Type |
|---|---|---|---|
| `%d` | `int` | `%f` / `%lf` | `float` / `double` (`lf` for scanf) |
| `%ld` | `long` | `%c` | `char` |
| `%lld` | `long long` | `%s` | C string |
| `%u` | `unsigned` | `%x` | hex |
| `%zu` | `size_t` | `%p` | pointer |

---

## 3. std::vector

### Construction

```cpp
std::vector<int> v;                  // empty
std::vector<int> v(n);               // n zeros
std::vector<int> v(n, -1);           // n copies of -1
std::vector<int> v = {1, 2, 3};
std::vector<std::vector<int>> g(n, std::vector<int>(m, 0));   // n x m grid
```

### Operations

| Operation | Code | Cost |
|---|---|---|
| Append | `v.push_back(x)` | O(1) amortized |
| Remove last | `v.pop_back()` | O(1) |
| Size / empty | `v.size()`, `v.empty()` | O(1) |
| First / last | `v.front()`, `v.back()` | O(1) |
| Index | `v[i]` (unchecked), `v.at(i)` (bounds-checked) | O(1) |
| Insert | `v.insert(v.begin() + i, x)` | O(n) |
| Erase one | `v.erase(v.begin() + i)` | O(n) |
| Erase range `[a, b)` | `v.erase(v.begin() + a, v.begin() + b)` | O(n) |
| Resize | `v.resize(k)` | O(n) |
| Reserve capacity | `v.reserve(k)` | O(n) |
| Fill | `v.assign(n, val)` | O(n) |
| Clear | `v.clear()` | O(n) |
| Swap | `v.swap(other)` | O(1) |

### Iteration

```cpp
for (int x : v) { }                     // read-only copy
for (auto& x : v) x *= 2;               // modify in place
for (size_t i = 0; i < v.size(); i++) { }
```

> **Gotcha:** `v.size()` is unsigned. `i < v.size() - 1` underflows when `v` is empty. Use `(int)v.size() - 1`.

---

## 4. `<algorithm>`

```cpp
auto b = v.begin(), e = v.end();
```

### Sorting

```cpp
std::sort(b, e);                                    // ascending
std::sort(b, e, [](int x, int y){ return x > y; }); // descending
std::stable_sort(b, e);                             // keeps order of equals
std::reverse(b, e);
```

### Searching

```cpp
auto it = std::find(b, e, x);        // == e if not found
int idx = it - b;
std::count(b, e, x);
std::count_if(b, e, [](int a){ return a % 2 == 0; });
std::any_of(b, e, pred);   std::all_of(b, e, pred);   std::none_of(b, e, pred);
```

### Binary search (range must be sorted)

| Function | Returns |
|---|---|
| `std::binary_search(b, e, x)` | `bool`, does `x` exist? |
| `std::lower_bound(b, e, x)` | iterator to first element **>= x** |
| `std::upper_bound(b, e, x)` | iterator to first element **> x** |

```cpp
int idx   = std::lower_bound(v.begin(), v.end(), x) - v.begin();
int cnt_x = std::upper_bound(b, e, x) - std::lower_bound(b, e, x);
```

### Min / max

```cpp
std::min(a, b);   std::max(a, b);   std::swap(a, b);
std::min({a, b, c});                       // initializer list
*std::min_element(b, e);   *std::max_element(b, e);
```

### Modifying

```cpp
std::fill(b, e, 0);
std::rotate(b, b + k, e);                  // left-rotate by k

// Dedupe (sort first!)
v.erase(std::unique(v.begin(), v.end()), v.end());

// Remove all occurrences of x
v.erase(std::remove(v.begin(), v.end(), x), v.end());
```

### Permutations (start from sorted)

```cpp
std::sort(b, e);
do {
    // use v
} while (std::next_permutation(b, e));
```

### Heap (stand-in for priority_queue)

```cpp
std::make_heap(b, e);                      // max-heap
v.push_back(x);  std::push_heap(v.begin(), v.end());
std::pop_heap(v.begin(), v.end());  int top = v.back();  v.pop_back();
```

---

## 5. C Strings (`<string.h>`)

```cpp
char s[100] = "hello";
```

| Function | Purpose | Note |
|---|---|---|
| `strlen(s)` | Length (excludes `'\0'`) | O(n), don't call in a loop condition |
| `strcpy(dst, src)` | Copy | Unsafe if `dst` is too small |
| `strncpy(dst, src, n)` | Bounded copy | May **not** null-terminate; set `dst[n-1] = '\0'` |
| `strcat(dst, src)` | Append | Unsafe if too small |
| `strncat(dst, src, n)` | Bounded append | Always terminates |
| `strcmp(a, b)` | Compare | `0` equal, `<0` a<b, `>0` a>b |
| `strncmp(a, b, n)` | Compare first n chars | |
| `strchr(s, 'c')` | First occurrence | `NULL` if missing |
| `strrchr(s, 'c')` | Last occurrence | `NULL` if missing |
| `strstr(s, "sub")` | Substring search | `NULL` if missing |
| `strtok(s, " ,")` | Tokenize | Modifies `s`; next calls use `strtok(NULL, " ,")` |

### Memory functions

```cpp
memset(arr, 0, sizeof arr);        // only reliable for 0 or -1 on ints
memcpy(dst, src, n_bytes);         // no overlap allowed
memmove(dst, src, n_bytes);        // overlap OK
memcmp(a, b, n_bytes);
```

> **Gotchas**
> - `memset(arr, 1, ...)` sets every *byte* to 1, so each `int` becomes `16843009`.
> - Never compare C strings with `==`; use `strcmp`.

---

## 6. `<stdlib.h>`

### Conversion

```cpp
atoi(s);   atol(s);   atof(s);                 // no error detection
strtol(s, &end, 10);   strtod(s, &end);        // safer; check *end and errno
```

### Memory

```cpp
int* p = (int*)malloc(n * sizeof(int));
int* q = (int*)calloc(n, sizeof(int));         // zero-initialized
p = (int*)realloc(p, new_n * sizeof(int));
free(p);  p = NULL;

// C++ equivalents
int* a = new int[n];    delete[] a;            // new[] pairs with delete[]
int* x = new int(5);    delete x;
```

### Misc

```cpp
abs(x);  labs(x);  llabs(x);
srand(seed);  rand();  rand() % n;             // RAND_MAX >= 32767
exit(code);   abort();
```

### qsort / bsearch

```cpp
int cmp(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);                  // avoids subtraction overflow
}
qsort(arr, n, sizeof(int), cmp);
int* r = (int*)bsearch(&key, arr, n, sizeof(int), cmp);   // NULL if not found
```

---

## 7. `<unistd.h>` and `<sys/types.h>`

### Process info

```cpp
pid_t pid  = getpid();
pid_t ppid = getppid();
uid_t uid  = getuid();
```

### fork

```cpp
pid_t c = fork();
if (c < 0)        { /* fork failed */ }
else if (c == 0)  { /* child  */ _exit(0); }
else              { /* parent: c is the child's PID */ }
// wait()/waitpid() need <sys/wait.h>, which is not in your list
```

### exec family (replaces the process image)

```cpp
execl("/bin/ls", "ls", "-l", (char*)NULL);
execvp("ls", argv);            // argv must end with NULL
// code after a successful exec never runs; if it does, exec failed
```

### Pipes

```cpp
int fd[2];
pipe(fd);                      // fd[0] = read end, fd[1] = write end
write(fd[1], buf, len);
read(fd[0], buf, sizeof buf);
close(fd[0]);  close(fd[1]);   // close the ends you don't use
dup2(fd[1], STDOUT_FILENO);    // redirect stdout into the pipe
```

### Low-level I/O

```cpp
ssize_t n = read(STDIN_FILENO, buf, size);   // 0 = EOF, -1 = error
write(STDOUT_FILENO, buf, n);
```

### Sleep

```cpp
sleep(2);          // seconds
usleep(500000);    // microseconds
```

### Common types

`pid_t` · `uid_t` · `size_t` · `ssize_t` · `off_t`

---

## 8. `<sys/resource.h>`

### Resource usage

```cpp
struct rusage ru;
getrusage(RUSAGE_SELF, &ru);       // or RUSAGE_CHILDREN

ru.ru_utime.tv_sec;  ru.ru_utime.tv_usec;   // user CPU time
ru.ru_stime.tv_sec;  ru.ru_stime.tv_usec;   // system CPU time
ru.ru_maxrss;                               // peak memory (KB on Linux)
```

### Resource limits

```cpp
struct rlimit rl;
getrlimit(RLIMIT_STACK, &rl);      // rl.rlim_cur = soft, rl.rlim_max = hard
rl.rlim_cur = 64 * 1024 * 1024;
setrlimit(RLIMIT_STACK, &rl);
```

| Constant | Limits |
|---|---|
| `RLIMIT_CPU` | CPU seconds |
| `RLIMIT_AS` | Total address space |
| `RLIMIT_DATA` | Data segment size |
| `RLIMIT_STACK` | Stack size |
| `RLIMIT_NOFILE` | Open file descriptors |
| `RLIMIT_CORE` | Core dump size |

### Priority

```cpp
getpriority(PRIO_PROCESS, 0);
setpriority(PRIO_PROCESS, 0, 10);  // higher number = lower priority
```

---

## 9. Handy Patterns

### Overflow-safe constants

```cpp
long long big = 1LL * a * b;       // avoid int overflow
const int INF = 1e9;               // INF + INF still fits in int
const long long LINF = 1e18;
```

### Frequency array

```cpp
int freq[26] = {0};
for (char c : s) freq[c - 'a']++;
```

### Pairs

```cpp
std::vector<std::pair<int,int>> p;
p.push_back({1, 2});   p.emplace_back(1, 2);
std::sort(p.begin(), p.end());     // by first, then second
```

### Prefix sums

```cpp
std::vector<long long> pre(n + 1, 0);
for (int i = 0; i < n; i++) pre[i+1] = pre[i] + v[i];
// sum of v[l..r] = pre[r+1] - pre[l]
```

### Two pointers / sliding window

```cpp
int l = 0;
for (int r = 0; r < n; r++) {
    // add v[r] to the window
    while (/* window invalid */) {
        // remove v[l] from the window
        l++;
    }
    // update answer using window [l, r]
}
```

### Binary search on the answer (find first `true`)

```cpp
int lo = 0, hi = N;
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (ok(mid)) hi = mid;
    else         lo = mid + 1;
}
// answer is lo
```

### Complexity guide

| n | Target complexity |
|---|---|
| <= 10 | O(n!) |
| <= 20 | O(2^n) |
| <= 500 | O(n^3) |
| <= 5,000 | O(n^2) |
| <= 1e5 | O(n log n) |
| <= 1e6 to 1e7 | O(n) |

---

## 10. Common Pitfalls

- **Off-by-one with `lower_bound`:** it returns an iterator; subtract `v.begin()` for the index.
- **Iterator invalidation:** `push_back`, `insert`, and `erase` can invalidate iterators and references into a vector.
- **Uninitialized locals:** `int x;` holds garbage. Globals and `std::vector<int>(n)` are zeroed.
- **Large arrays:** make them global/static or use vectors; big locals can overflow the stack.
- **Integer division:** `-7 / 2 == -3` and `-7 % 2 == -1` (truncates toward zero).
- **`char` arithmetic:** `'a' + 1` is an `int`; cast if you need a `char`.
- **`cin` then `getline`:** call `std::cin.ignore()` after `cin >> n`.
- **Mixing C and C++ I/O:** after `sync_with_stdio(false)`, don't mix `scanf`/`printf` with `cin`/`cout`.
- **Missing `\0`:** C string buffers need room for the terminator.
- **Signed/unsigned comparison:** `int` vs `size_t` can silently give wrong results.

---

## 11. Compile and Debug

```bash
g++ -std=c++17 -Wall -Wextra -O2 -fsanitize=address,undefined file.cpp -o out
./out < input.txt
```

| Flag | Purpose |
|---|---|
| `-Wall -Wextra` | Enable useful warnings |
| `-fsanitize=address,undefined` | Catch out-of-bounds, leaks, UB at runtime |
| `-g` | Debug symbols (for `gdb`) |
| `-O2` | Optimize (use for timing checks) |

**Quick sanity checklist before submitting:**

1. Does it handle `n = 0` and `n = 1`?
2. Could any intermediate value overflow `int`?
3. Are all arrays and vectors indexed within bounds?
4. Is every `malloc`/`new` freed, and is every pipe end closed?
