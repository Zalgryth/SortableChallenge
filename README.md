# Sortable Challenge

This is my entry for the Sortable Challenge.

It is a command-line tool for computing the results of a series of auctions. See the `samples` folder for sample input and config json files, as well as the expected output.

## Style

This project follows the standard PEP8 styling guide.

## Build + Run

To build and run, execute the following in a terminal:

```bash
$ docker build -t challenge .
$ docker run -i -v /path/to/challenge/config.json:/auction/config.json challenge < /path/to/challenge/input.json
```

## Unit tests

To run unit tests, execute the following command:

```bash
$ python -m unittest
```

For your convenience, you can get unit test results from the `challenge` Docker container (built in the `Build + Run` section). To do so, run the following command:

```bash
$ docker run challenge unittest
```
