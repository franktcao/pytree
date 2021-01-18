import os
from pathlib import Path
from textwrap import dedent

import pytest

from src.pytree import PyTree


@pytest.fixture
def test_path() -> Path:
    """Return test path (work around for running pytest from repo's root)."""
    cur_path = Path(os.getcwd())
    if os.path.basename(cur_path) == "tests":
        return cur_path
    else:
        return cur_path / "tests"


class TestPyTreeFromPath:
    @staticmethod
    def test_defaults(test_path: Path) -> None:
        """Assert expected contents are displayed as tree using default params."""
        # === Arrange
        path_to_test = test_path / Path("example_root/")
        expected = dedent(
            """\
            example_root
            ├── sub_1
            │   ├── sub_1_1
            │   └── sub_1_2
            │       └── some_file.txt
            └── sub_2
                └── some_other_file.txt
            
            Total directories: 4
            Total files: 2
            """
        )

        # === Act
        actual = "\n".join(PyTree.from_path(path_to_test))

        # === Assert
        assert actual == expected

    @staticmethod
    def test_ignore_files(test_path: Path) -> None:
        """Assert expected contents are displayed as tree when ignoring files."""
        # === Arrange
        path_to_test = test_path / Path("example_root/")
        expected = dedent(
            """\
            example_root
            ├── sub_1
            │   ├── sub_1_1
            │   └── sub_1_2
            └── sub_2
            
            Total directories: 4
            """
        )

        # === Act
        result = PyTree.from_path(path_to_test, ignore_files=True)
        actual = "\n".join(result)

        # === Assert
        assert actual == expected

    @staticmethod
    def test_max_depth(test_path: Path) -> None:
        """Assert expected contents are displayed as tree when limiting depth."""
        # === Arrange
        path_to_test = test_path / Path("example_root/")
        expected = dedent(
            """\
            example_root
            ├── sub_1
            └── sub_2
    
            Total directories: 2
            Total files: 0
            """
        )

        # === Act
        result = PyTree.from_path(path_to_test, max_depth=1)
        actual = "\n".join(result)

        # === Assert
        assert actual == expected
