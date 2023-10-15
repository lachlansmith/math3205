# Lachlan Smith, Joshua, Lachie

## Run

This repository can be run using

```
python main.py
```

To view all functionality we recommend running the below command

```
python main.py -i 215 -p -h -v
```

## Usage

We've provided command line arguments to run the bin packing problem in various different ways.

### Instances

To run a different instance of the problem use the `--instance` argument.

```
python main.py --instance 215
```

### Verbose

To see debug output that includes preprocess assignments and real-time feasibility cuts provide the `--verbose` argument.

```
python main.py -i 215 -p -h --verbose
```

To see gurobi output instead of real-time cuts set `--verbose` to **2**.

```
python main.py -i 215 -p -h --verbose 2
```

### Preprocess

To run the preprocessor on the solver use the `--preprocess` argument.

```
python main.py --instance 215 --verbose --preprocess
```

The preprocess argument can be made to run with more granular control,
set `--preprocess` to **010** to only assign large items to the solver, and
not incompatible or conflicting items, etc

```
python main.py --instance 215 --verbose --preprocess 010
```

### Heuristic

To run the problem with the heuristic provide the `--heuristic` argument.

```
python main.py --instance 0 --heuristic
```

### Plot

To plot the solution provide the `--plot` argument (default **grid**).

```
python main.py --instance 1 --plot
```

To plot the heuristic solution set `--plot` to **heuristic**

```
python main.py --instance 1 --heuristic --plot heuristic.
```

To plot the solver solution the same as heuristic set `--plot` to **box**

```
python main.py --instance 1 --plot box.
```

### Extract

To extract the solution for plotting but not plot the solution provide the `--extract` argument.

```
python main.py -i 215 -p -h --extract
```
