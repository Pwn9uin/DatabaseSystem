# Assignment 1

## Environment

- Tested OS : macOS
- Python version : 3.14.0
- Required package: pandas

## Files

- `src/node.py`: implementation of B-tree, B+-tree, and B*-tree
- `src/exp.py`: experiment script
- `src/student.csv`: input dataset

## Setup

```bash
# Clone the repository
git clone https://github.com/Pwn9uin/DatabaseSystem.git
cd DatabaseSystem

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas
```

## Run experiment code

```bash
cd src
python3 ./exp.py
```

## Result Example
The exact execution time may vary depending on the machine, but the split
counts, utilization values, query results, and integrity results should be
consistent.

```bash
============= Exp1 (d=3) =============
Btree insert time avg : 187.507ms
B+tree insert time avg : 216.942ms
B*tree insert time avg : 202.178ms
Btree split count : 24452
B+tree split count : 28730
B*tree split count : 20169
Btree utilization : 68.141%
B+tree utilization : 57.995%
B*tree utilization : 82.606%

============= Exp1 (d=5) =============
Btree insert time avg : 168.629ms
B+tree insert time avg : 190.360ms
B*tree insert time avg : 198.032ms
Btree split count : 14610
B+tree split count : 16111
B*tree split count : 11878
Btree utilization : 68.418%
B+tree utilization : 62.046%
B*tree utilization : 84.147%

============= Exp1 (d=10) =============
Btree insert time avg : 158.197ms
B+tree insert time avg : 195.356ms
B*tree insert time avg : 196.022ms
Btree split count : 7250
B+tree split count : 7651
B*tree split count : 5879
Btree utilization : 68.918%
B+tree utilization : 65.308%
B*tree utilization : 84.991%

============= Exp2 (d=5) =============
Btree avg search time : 0.001622ms
B+tree avg search time : 0.001560ms
B*tree avg search time : 0.001612ms

============= Exp3 (d=5) =============
Btree range query time : 20.070ms  , avg gpa : 3.278, avg height : 174.058
B+tree range query time : 4.892ms , avg gpa : 3.278, avg height : 174.058
B*tree range query time : 20.146ms , avg gpa : 3.278, avg height : 174.058

============= Exp4 (d=5) =============

 ---- delete 2000 ----
Btree delete time : 4.215ms, integrity test : True
B+tree delete time : 3.623ms, integrity test : True
B*tree delete time : 3.911ms, integrity test : True

 ---- delete 10 percent ----
Btree delete time : 18.730ms, integrity test : True
B+tree delete time : 17.579ms, integrity test : True
B*tree delete time : 17.133ms, integrity test : True

 ---- delete 20 percent ----
Btree delete time : 40.476ms, integrity test : True
B+tree delete time : 35.326ms, integrity test : True
B*tree delete time : 39.630ms, integrity test : True
```