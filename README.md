# Lachlan Smith, Joshua, Lachie

## Usage

This repository can be run using

```
python main.py
```

We've provided command line arguments to run the bin packing problem in various different ways.

To run a different instance of the problem use the `--instance` argument.

```
python main.py --instance 215
```

To run the preprocessor on the solver use the `--preprocess` argument.

```
python main.py -i 215 --preprocess
```

To run the problem with the heuristic provide the `--heuristic` argument.

```
python main.py -i 215 --preprocess --heuristic
```

To plot the solution provide the `--plot` argument (default **grid**).

```
python main.py -i 215 -p -h --plot
```

To plot the heuristic solution set `--plot` to **heuristic**

```
python main.py -i 215 -p -h --plot heuristic.
```

To plot the solver solution the same as heuristic set `--plot` to **box**

```
python main.py -i 215 -p -h --plot box
```

To extract the solution for plotting but not plot the solution provide the `--extract` argument.

```
python main.py -i 215 -p -h --extract
```

To see gurobi output instead of real-time cuts provide the `--verbose` argument.

```
python main.py -i 215 -p -h --verbose
```
