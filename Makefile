# Just a sample for demo purposes

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
