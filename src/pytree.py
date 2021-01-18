from pathlib import Path
from typing import Iterator

import attr
import os


@attr.s(auto_attribs=True, frozen=True)
class TreeSymbols:
    """Four character components to draw tree diagram."""

    void = "    "
    skip = "│   "
    item = "├── "
    last = "└── "


class PyTree:
    """
    Implementation of unix command `tree` (modified version of this SO answer:
    https://stackoverflow.com/a/59109706/5400084).
    """

    @classmethod
    def from_path(
        cls,
        root_dir_path: Path,
        max_depth: int = -1,
        ignore_files: bool = False,
    ) -> Iterator[str]:
        """
        Recursively generate an ascii directory tree structure line by line for a given
        path.

        :param root_dir_path:
            Path to get directory tree structure for
        :param max_depth:
            Maximum depth in the directory to traverse
        :param ignore_files:
            Indicate whether or not to ignore files (list directories only)
        :return:
            Line-by-line tree directory structure
        """
        files = 0
        directories = 0

        def inner(current_level: Path, prefix: str = "", depth=-1) -> None:
            """
            Yield current level's contents.

            :param current_level:
                Current level to collect contents
            :param prefix:
                Characters to append to the beginning of each item
            :param depth:
                Counter to keep track of recursion depth
            """
            nonlocal files, directories
            if depth == 0:
                return

            # Collect current directory's files & subdirectories and associated symbol
            contents = (
                [content for content in current_level.iterdir() if content.is_dir()]
                if ignore_files
                else list(current_level.iterdir())
            )
            pointers = (len(contents) - 1) * [TreeSymbols.item] + [TreeSymbols.last]

            for pointer, content in zip(pointers, sorted(contents)):
                # Recursively collect contents of subdirectories
                if content.is_dir():
                    yield prefix + pointer + content.name
                    directories += 1
                    extension = (
                        TreeSymbols.skip
                        if pointer == TreeSymbols.item
                        else TreeSymbols.void
                    )
                    yield from inner(
                        content, prefix=prefix + extension, depth=depth - 1
                    )
                # Yield files if not limiting to directories
                elif not ignore_files:
                    yield prefix + pointer + content.name
                    files += 1

        # Start with yielding the root
        yield root_dir_path.name

        # Recursively yield results from each subdirectory
        yield from inner(root_dir_path, depth=max_depth)

        # Yield counts
        yield ""
        yield f"Total directories: {directories}"
        if not ignore_files:
            yield f"Total files: {files}"
        yield ""


# Not covered: Simple example to run
if __name__ == "__main__":  # pragma: no cover
    """Simple demonstration."""
    my_path = Path(os.getcwd()).parent
    my_tree = PyTree().from_path(root_dir_path=my_path, max_depth=3, ignore_files=False)
    print("\n".join(my_tree))
