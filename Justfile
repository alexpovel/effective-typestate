set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# ==============================================================================
# Core
# ==============================================================================

# Lists all available recipes.
[private]
default:
    @just --list

alias p := present

mode := 'html'

# Compiles and opens the presentation of the given name.
[windows]
present file='presentation.md': install-npx && notify-presenter
    cd {{justfile_directory()}} \
    && npx --yes @marp-team/marp-cli@latest {{file}} --output {{without_extension(file) + '.' + mode}} \
    && Invoke-Item {{without_extension(file) + '.' + mode}}

# Compiles and opens the presentation of the given name in Firefox.
[unix]
present file='presentation.md': install-npx install-firefox && notify-presenter
    cd {{justfile_directory()}} \
    && npx --yes @marp-team/marp-cli@latest {{file}} --output {{without_extension(file) + '.' + mode}} \
    && (firefox {{without_extension(file) + '.' + mode}} 2>/dev/null &)

# Notifies the presenter that the presentation is ready.
[private]
notify-presenter:
    @echo 'Presentation up and ready, enjoy!'

# Installs npx via Node.js using Chocolatey, if it is not already installed.
[windows]
install-npx: ensure-choco
    Get-Command -Name 'npx' 2>$null || choco install --yes nodejs

# Installs npx via Node.js.
[unix]
install-npx: ensure-apt
    @command -v npx || (sudo apt-get update && sudo apt-get install --yes nodejs)

# Installs Firefox.
[unix]
install-firefox: ensure-apt
    @command -v firefox || (sudo apt-get update && sudo apt-get install --yes firefox-esr)

# Ensures `apt` is available, aborting with a friendly error message if not.
[unix]
[private]
ensure-apt:
    @command -v apt-get || (echo 'Sorry, this Justfile requires `apt`.' && exit 1)

# Ensures `choco` is available, aborting with a friendly error message if not.
[windows]
[private]
ensure-choco:
    @try { \
        Get-Command -Name 'choco' -ErrorAction Stop; \
    } catch { \
        Write-Output 'Sorry, this Justfile requires `choco`.'; \
        exit 1; \
    }
