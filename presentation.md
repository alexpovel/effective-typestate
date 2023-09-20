---
marp: true
theme: gaia
math: true
---

<!-- _class: lead -->

# Type-State Pattern

A universal pattern for *less wrong*™ code

2023-09-20

Alex Povel

---

## 💡 Premise

* *type-state* is a code pattern
* it's about offloading to the type system as much as possible
  * [enforce order of operations](https://cliffle.com/blog/rust-typestate/#what-are-typestates)
* computers are excellent at logic
  * that's their whole deal...
  * so why not apply that power to the very instructions we give them?

---

## 🌟 About

* language-agnostic
* some sample use cases
* live demo
* discussion!
  * am still learning about this myself
* links look like [this](https://example.com)

---

## ⚙ Use Case 1: Unix processes

* can be in [one of the following states](https://pages.cs.wisc.edu/~remzi/OSTEP/):

  ```mermaid
  stateDiagram
      Running --> Ready: Descheduled
      Ready --> Running: Schedule
      Running --> Waiting: I/O initiate
      Waiting --> Ready: I/O complete
  ```

* *states*... 🤔

---

<!-- _class: lead -->

## 👨‍💻 Use Case 1: Demo

---

## ⚙ Use Case 1: Summary

* whole `class`es of errors disappear
* some are still possible:

  ```python
  class WaitingProcess(Process):
    @classmethod
    def from_initiating_io(cls, process: ReadyProcess) -> t.Self:
        return cls(id=process.id)
  ```

  * however, only need the be caught once; unlikely to occur again after, compiler helps us
* unit testing partly obsolete
* first-class tooling and IDE support

---

## 🎒 Interlude: types are bags

* a type represents a set of values
  * using `u32` & only 3 needed? 4 billion other ways to get it wrong
  * strings are the worst offenders, don't get me started 😠
    * "infinite cardinality"
    * **no type-level structure** (encoding is opaque)
* one type == one bag
  * do you keep your 🧦 in the same drawer as your 🍴?
    * no: literally `typestate_irl` 👍
    * yes: get help

---

## 📨 Use Case 2: [Email verification](https://dusted.codes/the-type-system-is-a-programmers-best-friend)

* imagine running a newsletter
* sending email to *unverified* addresses is 🙅‍♂️
  * spam
  * costs
* can typestate help? (spoiler: yes)

---

<!-- _class: lead -->
## 👨‍💻 Use Case 2: Demo

---

## 📨 Use Case 2: Summary

* again, some **impossible states become impossible to represent**
* structured programming is great and all, but can be [m`if`used](https://thedailywtf.com/articles/coding-like-the-tour-de-france):

    ```python
    try lick_elbow():
        if not is_elbow_licked():
            for elbow in elbows:
                if elbow.is_lickable():
                    lick(elbow) if is_monday() else make_breakfast()
            raise ElbowNotLickedError
    # ... 🙂🔫
    ```

* maps to database neatly, e.g. [one type per table](https://learn.microsoft.com/en-us/ef/core/modeling/inheritance#table-per-type-configuration) in ORM
  * shard by verification; all unverified to slow storage?

---

## 🎒 Interlude: types are bags pt. 2

* `VerifiedEmailAddress` is a tidy bag
* can just reach into it without looking
  * *all* possible *values* of `VerifiedEmailAddress` are *valid*, not just *some* of the entire bag
  * after grabbing from the bag, don't need to sort (`if`)
* it being found in that bag *guarantees* certain properties
  * enforce in constructor,
  * getters/setters/properties/...

---

## 🧹 Use Case 3: Guaranteed setup & cleanup

* use externally managed resource, with guaranteed cleanup
  * [context manager](https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers) (Python), [RAII](https://en.wikipedia.org/wiki/Resource_acquisition_is_initialization) (C++, Rust), [`defer`](https://go.dev/tour/flowcontrol/12) (Go), [`using`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/using) (C#)
* what about guaranteed *setup* as well, without possibility for misuse on the type level?

---

<!-- _class: lead -->
## 👨‍💻 Use Case 3: Demo

---

## 💂‍♀️ Interlude: guard clauses

<!-- * [guard clauses](https://en.wikipedia.org/wiki/Guard_(computer_science)) cause this: -->

```python
def without_guard(x: int, y: str):  # 🤢
    if x > 420:
        if is_valid_token(y):
            # ...

def with_guard(x: int, y: str):  # 🤔
    if x <= 420 or not is_valid_token(y):  # Better...
        return
    # ...

def no_guard_needed_if_we_never_enter_garbage(z: CoolStuff):  # 😎
    z.x  # guaranteed to be > 420
    z.y  # guaranteed to be valid token
    # ...
```

---

## ✍ In summary, typestate

![bg right:30%](https://t2.genius.com/unsafe/432x767/https%3A%2F%2Fimages.genius.com%2F2b790e48bcd9779bce4dc5bc74a01118.563x1000x1.png)

* ... can lead to *less wrong*™ code
  * eradicates conditionals
  * pushes upkeep of invariants to the type system: human stoopid, compiler smart
  * absolutely no money-back guarantee tho
* ... makes **impossible states impossible to represent**
<!-- * ... works in most languages (OOP, FP, ...) -->

https://github.com/alexpovel/effective-typestate


---

## 📚 Further reading

* [The Typestate Pattern in Rust](https://web.archive.org/web/20230415021514/http://cliffle.com/blog/rust-typestate/)
* [The type system is a programmer's best friend](https://web.archive.org/web/20230328111411/https://dusted.codes/the-type-system-is-a-programmers-best-friend)
* [How To Survive Your Project's First 100,000 Lines](https://web.archive.org/web/20230505040711/https://verdagon.dev/blog/first-100k-lines)
* [Writing Python like it's Rust](https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html)
* [Make invalid states unrepresentable](https://geeklaunch.io/blog/make-invalid-states-unrepresentable/)
* [Minor lessons from time at an aerospace company](https://news.ycombinator.com/item?id=36947865)
* [Ad-hoc polymorphism erodes type-safety](https://cs-syd.eu/posts/2023-08-25-ad-hoc-polymorphism-erodes-type-safety)
