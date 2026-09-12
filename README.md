# CPU Scheduling Algorithms

A Python implementation of common **CPU scheduling algorithms** developed as an Operating Systems course project.

The program simulates different scheduling strategies, displays a Gantt chart for each algorithm, and calculates the average waiting time and turnaround time.

## Implemented Algorithms

* **First Come First Serve (FCFS)**
* **Shortest Job First (SJF) — Non-Preemptive**
* **Shortest Job First (SJF) — Preemptive**
* **Round Robin (RR)** with a user-defined time quantum

## Features

* Accepts multiple processes and their burst times
* Optionally supports process arrival times
* Allows the user to specify the Round Robin time quantum
* Generates Gantt charts showing process execution
* Calculates:

  * Waiting time
  * Turnaround time
  * Average waiting time
  * Average turnaround time

## Requirements

* Python 3
* pandas

Install pandas with:

```bash
pip install pandas
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/emanshub/cpu-scheduling-algorithms.git
```

Navigate to the project folder:

```bash
cd cpu-scheduling-algorithms
```

Run the program:

```bash
python cpu_scheduling.py
```

The program will prompt you to enter the number of processes, their burst times, whether they have arrival times, and the Round Robin quantum.

## Example

The program produces output similar to:

```text
=== FCFS Scheduling ===
Gantt Chart:
|  P1  |  P2  |  P3  |

PID  Arrival  Burst  Waiting  Turnaround
1       0       5       0          5
2       0       3       5          8
3       0       2       8         10
```

The results are displayed separately for each scheduling algorithm.

## Course Project

This project was developed as part of an **Operating Systems** course project.

### Team

* Eman Al Matar
* Majd Aljamed
* Lama Altamimi
