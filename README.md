# plox
My Python implementation for the [Lox](https://craftinginterpreters.com/the-lox-language.html) programming language.

## Requirements
The project requires Python 3.10 or higher.

## Getting Started
Clone the repository:
```
git clone https://github.com/kappq/plox.git
```
Move into the new directory:
```
cd plox
```

## Usage
Once you have cloned the repository and moved into the new directory, you can run the interpreter with:
```
python lox.py [script]
```
where `[script]` is the optional path to a `.lox` file. If the path isn't specified the interpreter will run in prompt mode.

## Additional Information
All the files are formatted with `black` and type checked with `mypy` in `--strict` mode.
