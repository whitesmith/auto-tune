# Benchmarks

Script(s) to run benchmarks.

**Requires:** `python >= 3.2`

**Note:** Currently only classification datasets from `sklearn` are available, and it is only comparable to `sklearn.model_selection.GridSearchCV`. More will be added in the future.

### How to use

* Install requirements

```bash
pip install -r requirements/requirements.txt
```

* Run script

```bash
python src/benchmark.py
```

* See script usage

```bash
python src/benchmark.py --help
```

* See and run the bash script for an example

```bash
sh benchmark.sh wine
```

### How to run when developing auto-tune

* Instal requirements

```bash
pip install -r requirements/requirements.txt
```

* Install auto-tune locally for development

```bash
pip install -e /full/path/to/auto-tune/directory
```

* Use script normally, changes to auto-tune code will be refleceted when running the benchmark
