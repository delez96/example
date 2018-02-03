from cx_Freeze import setup, Executable
setup(
    name = "matrix",
    version = "0.1",
    description = "Blackjack",
    executables = [Executable("matrix.py")]
)