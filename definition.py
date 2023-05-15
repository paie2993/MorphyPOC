from dataclasses import dataclass


@dataclass
class Definition:
    base_form: str
    definitions: list

    def __str__(self):
        defs = "\n".join(self.definitions)
        return f"{self.base_form}\n{defs}\n"
