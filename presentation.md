---
marp: true
theme: gaia
---

<!-- _class: lead -->

# `just`, a command runner

.NET Hamburg User Group Meetup

2023-04-05

Alex Povel

---

## 💡 Premise

* GNU `make` turns source files into artifacts (binaries, ...)
* `make` and its `Makefile` are a convenient and popular entrypoint to [repositories](https://github.com/alexpovel/ancv/blob/main/Makefile), e.g.:
  - *how do I set up my local development environment?*
  - *how do I compile the source files?*
  - *how do I run tests?*
* however, as a *build system*, `make` revolves around **files**, whereas much of the above are merely **commands** (which often don't produce files)

---

## 🌟 New kid on the block

[`just`](https://github.com/casey/just): "🤖 Just a command runner"

1) write a `Justfile` defining your *recipes*
2) call with `just recipe-name [arg1 arg2 argn]`
3) your pre-defined code runs, and generally does so **cross-platform** (Linux, Windows, MacOS)

---

## ✅ Advantages over `make`

If you're familiar with `make`:

* no more `PHONY`
* cross-platform, can specify shell to use on Windows (default `sh`)
* recipes with arguments, which can have defaults
* listing of recipes and their description built-in
* run from any subdirectory
* arbitrary (interpreted) languages supported via shebang (`#!`)
<!-- - installation is *easy enough* (single binary; `make` often preinstalled though) -->

---

😵 [Documenting a `Makefile`](https://github.com/alexpovel/betterletter/blob/065e320cd0cf726777bb6caa9cbb3bcc2c500ad3/Makefile#L7-L26) has poor DX:

```make
# From https://news.ycombinator.com/item?id=30137254
define PRINT_HELP_PYSCRIPT # start of Python section
import re
import sys

output = []
for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        output.append("%-10s %s" % (target, help))
output.sort()
print('\n'.join(output))
endef
export PRINT_HELP_PYSCRIPT # End of python section

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

venv:  ## Installs the virtual environment.
	@poetry install
```

---

<!-- _class: lead -->

## 👨‍💻 Just a little live demo

Using this repository's [`Justfile`](./Justfile).

---

## ✍ In summary, `just` can...

![bg right:30%](https://t2.genius.com/unsafe/432x767/https%3A%2F%2Fimages.genius.com%2F2b790e48bcd9779bce4dc5bc74a01118.563x1000x1.png)

* be a **version-controlled** "summary of jobs" for your repository
  <!-- - documentation next to the code (instead of Confluence, ...) -->
* be an entrypoint for newcomers
  <!-- - onboarding scripts, setting up the necessary dev environment -->
* ease recurring tasks: disjoint shell histories become knowledge shared team-wide
* close the [*local ⇔ CI* gap](./.github/workflows/main.yml) (everything's `just the-same`)
* be a source of puns 😀

https://github.com/alexpovel/just-present
