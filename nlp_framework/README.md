Tagger - Gensim based Document Tagging Service

### Setup
* Install Python 2.7.x with "pip"
    C Dependencies: python-devel gcc-gfortran gcc44-gfortran libgfortran blas-devel lapack-devel
```bash
make env            ## installs all the dependencies
. .env/bin/activate ## activates python virtual env
make run-tagger     ## runs tagger app on port 8004
```

### Running Tests

```bash
make test
```

#### Running individual test

```bash
make test path/to/tests[file][:function]
```
