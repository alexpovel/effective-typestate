from dataclasses import dataclass


@dataclass
class EmailAddress:
    inner: str
    is_verified: bool


@dataclass
class User:
    email: EmailAddress

    def send_newsletter(self) -> None:
        # Much control flow...
        #
        # much to go wrong...
        #
        # potentially lots of nesting and therefore scopes introduced...
        #
        # many code paths to test... growing exponentially...
        #
        # not wow.
        if self.email.is_verified:  # 🤮
            # Extra ugly in Python: "hidden" control flow
            raise ValueError("Cannot send newsletter to unverified email")  # 🤮

        send()


def send() -> None:
    pass
