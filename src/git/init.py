class LocalGitClient:
    """A local git client that can clone repos.

    Setting up git authentication can have side effects, like writing credentials to
    files or caching them in an agent. The goal is to manage the unmanaged (external)
    resources and guarantee correct usage on the type level.

    Notice how `credentials` and `repo` are `str`, and therefore in the same bag.
    Confusing stuff.
    """

    def __init__(
        self,
        credentials: str,  # 🤮
    ) -> None:
        print("Initializing local git client...")
        self.credentials = credentials

        self.setup_local_authentication()

    def clone(self, repo: str) -> None:
        print("Cloning repo...")

    def setup_local_authentication(self) -> None:
        """Might write to `~/.git-credentials` (bad!!)

        https://git-scm.com/docs/git-credential-store#FILES
        """
        print("Setting up local authentication...")


client_manager = LocalGitClient(credentials="foo")
client_manager.clone(repo="bar")

# Now what? Plaintext credentials still there!
# Need to clean up after ourselves, **automatically*.
# Relying on `__del__` aka GC is not an option (not explicit, not deterministic).


class LocalGitClientWithManagement(LocalGitClient):
    def __enter__(self) -> LocalGitClient:
        print("Entering context...")

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print("Exiting context...")
        self.cleanup_local_authentication()

    def cleanup_local_authentication(self) -> None:
        """Remove left-over garbage."""

        print("Cleaning up local authentication...")


# Better!
with LocalGitClientWithManagement(credentials="foo") as client_manager:
    client_manager.clone(repo="bar")

# Cleanup runs when exiting the block, done!
# But... what if we forget to use `with`? 🤔

client_manager = LocalGitClientWithManagement(credentials="foo")
client_manager.clone(repo="bar")  # Usage **without** `with` is still possible!

# Let's make it impossible on the type level.


class LocalGitClientManager:
    class __LocalGitClient:
        """The actual local git client that can clone repos.

        It is managed from the outside. It cannot even manage itself. What an idiot.

        Double underscore makes this "private", so it truly cannot be imported from the
        outside. A bit of a hack though and potentially not idiomatic.
        """

        def __init__(
            self,
            credentials: str,
        ) -> None:
            print("Initializing local git client...")
            self.credentials = credentials

        def clone(self, repo: str) -> None:
            print("Cloning repo...")

    def __init__(
        self,
        credentials: str,
    ) -> None:
        print("Initializing local git client manager...")
        self.credentials = credentials

    def __enter__(self) -> __LocalGitClient:
        print("Entering context...")

        # Run setup...

        return self.__LocalGitClient(credentials=self.credentials)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        print("Exiting context...")

        # Run cleanup...


# Now it's impossible to misuse (without some serious determination to break things):
#
# - the *actual* client cannot be created from the outside
#
# - the *only* way to create it is through the context manager, but if we `enter`,
#   `exit` is *guaranteed* to run as well
#
# Full management of both setup and guaranteed teardown is achieved, with full type
# safety!

client_manager = LocalGitClientManager(credentials="foo")

# Impossible: not only on the type level, but also at runtime
try:
    bad_client = LocalGitClientManager.__LocalGitClient(credentials="foo")
except AttributeError:
    pass

with client_manager as actual_client:
    actual_client.clone(repo="bar")

# Cleanup runs when exiting the block, done. Notice: **not a single `if` statement**,
# like `if self.is_authenticated`. Such an attribute/property/field/whatever your
# language calls it is *state*. In this case, it would be a `bool`. However, with
# typestate, it... doesn't exist. Poof. The compiler guarantees correctness here.
