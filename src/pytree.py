from typing import Iterator
from pathlib import Path


class PyTree:
    """
    Implementation of unix command `tree` (modified version of this SO answer:
    https://stackoverflow.com/a/59109706/5400084).
    """

    # Tree components:
    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "

    @classmethod
    def from_path(
        cls, root_dir_path: Path, max_depth: int = -1, ignore_files: bool = False,
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

        # Start with yielding the root
        yield root_dir_path.name

        def inner(current_level: Path, prefix: str = "", depth=-1) -> None:
            """Yield current level's contents."""
            nonlocal files, directories
            if depth == 0:
                return

            # Collect current directory's files & subdirectories and associated symbol
            contents = (
                [content for content in current_level.iterdir() if content.is_dir()]
                if ignore_files
                else list(current_level.iterdir())
            )
            pointers = (len(contents) - 1) * [cls.tee] + [cls.last]

            for pointer, content in zip(pointers, contents):
                # Recursively collect contents of subdirectories
                if content.is_dir():
                    yield prefix + pointer + content.name
                    directories += 1
                    extension = cls.branch if pointer == cls.tee else cls.space
                    yield from inner(
                        content, prefix=prefix + extension, depth=depth - 1
                    )
                # Yield files if not limiting to directories
                elif not ignore_files:
                    yield prefix + pointer + content.name
                    files += 1

        # Recursively yield results from each subdirectory
        yield from inner(root_dir_path, depth=max_depth)

        # Yield counts
        yield f"Total directories: {directories}"
        yield f"Total files: {files}" if not ignore_files else ""


if __name__ == "__main__":
    """Simple demonstration."""
    my_path = Path("/Users/franktcao/local/workspace/pytree")
    my_tree = PyTree().from_path(root_dir_path=my_path, max_depth=2, ignore_files=False)
    print("\n".join(my_tree))
