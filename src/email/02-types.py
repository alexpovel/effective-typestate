from dataclasses import dataclass


@dataclass
class EmailAddress:
    inner: str


@dataclass
class VerifiedEmailAddress(EmailAddress):
    pass


@dataclass
class User:
    email: EmailAddress


@dataclass
class VerifiedUser:
    email: VerifiedEmailAddress

    def send_newsletter(self) -> None:
        # We just... send?! 🤯 So obvious we might inline the function.
        pass


user = User(email=EmailAddress(inner="person@example.com"))
user.send_newsletter()  # LiTeRaLlY iMpOsSiBlE
