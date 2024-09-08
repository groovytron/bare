import pathlib


def get_fixture_path(fixture_folder: str) -> str:
    return (
        pathlib.Path(__file__).parent.resolve() / f"fixtures/{fixture_folder}"
    )
