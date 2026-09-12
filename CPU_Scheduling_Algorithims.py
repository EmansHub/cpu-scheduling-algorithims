"""
# OPERATING SYSTEMS PROJECT

- Main body
- Class process
- ⁠Function1: FCFS
- ⁠Function2: SJF non-preemptive
- ⁠Function3: SJF preemptive
- ⁠Function4: RR
"""

"""class processes"""

class Process:
  def __init__ (self,pid,burst,arrival=0):
    self.pid = pid
    self.burst = burst
    self.arrival = arrival

    self.remaining = burst 
    self.start = None
    self.completion = None #time process finished
    self.waiting = None
    self.turnaround = None #time taken from arrival until process is finished

  def calculate_metrics(self):
    self.turnaround = self.completion - self.arrival
    self.waiting = self.turnaround - self.burst

  #to double check the values
  def __str__ (self):
    return "process id: "+ str(self.pid) +", bursttime: "+ str(self.burst)+ ", arrival: "+str(self.arrival)
  


"""Resetting process variables"""

def reset(processes):
    for p in processes:
        p.remaining = p.burst
        p.completion = None
        p.start = None

"""Sorting function"""

def sort_key(p):
    return (p.arrival, p.burst)

"""Gantt Chart Printer"""

def print_gantt_chart(processes):
    chart = ""
    timeline = ""
    for p in processes:
        chart += f"|  P{p.pid}  "
        timeline += f"{p.start:<6}" #align to left within a field which is 6 characters wide 
    timeline += f"{processes[-1].completion:<6}" #starting from last process in list 
    chart += "|"
    print("Gantt Chart:")
    print(chart)
    print(timeline)

"""Process Table Printer (with averages)"""

def print_process_table(processes):
    import pandas as pd
    data = {
        "PID": [p.pid for p in processes],
        "Arrival": [p.arrival for p in processes],
        "Burst": [p.burst for p in processes],
        #"Start": [p.start for p in processes],
        #"Completion": [p.completion for p in processes],
        "Waiting": [p.waiting for p in processes],
        "Turnaround": [p.turnaround for p in processes],
    }
    df = pd.DataFrame(data)

    print(df)
    print("\nAverage Turnaround Time:", str(round(df["Turnaround"].mean(), 2)) + " ms")
    print("Average Waiting Time:", str(round(df["Waiting"].mean(), 2)) + " ms")




"""First Come First Serve (FCFS)"""

def fcfs(processes):
    #sort processes by arrival time
    processes.sort(key=lambda p: p.arrival)
    current_time = 0 

    for p in processes:
      #wait for process to arrive if needed
        if current_time < p.arrival:
            current_time = p.arrival
            #set start and completion times
        p.start = current_time
        p.completion = current_time + p.burst
        p.calculate_metrics()
        #move time forward
        current_time = p.completion

    print("\n=== FCFS Scheduling ===")
    print_gantt_chart(processes)
    print_process_table(processes)

"""Shortest Job First (SJF) non-preemptive"""

def sjf_non_preemptive(processes):
    reset(processes)
    #sort processes by arrival time first, then by burst time
    processes.sort(key=lambda p: (p.arrival, p.burst))
    completed = 0 #number of completed processes
    ready_queue = [] #list of processes ready to be scheduled
    current = None #currently running process
    time = 0 #current simulation time

    # Gantt chart components
    gc_p = "|  " #process execution order
    gc_t = str(time) + "      " #timestamps for gantt chart

#run until all processes are completed
    while completed < len(processes):
        # Add processes that have arrived and are not done
        for p in processes:
            if p.arrival <= time and p.completion is None and p not in ready_queue:
                ready_queue.append(p)

#if no process is ready, increment time and retry
        if not ready_queue:
            time += 1
            continue

        # Sort by burst time, then arrival
        ready_queue.sort(key=lambda p: (p.burst, p.arrival))
        current = ready_queue.pop(0)

        # Set start and completion times
        if current.start is None:
            current.start = time
        current.completion = time + current.burst
        current.remaining = 0
        current.calculate_metrics()

        # Update Gantt chart
        gc_p += f"P{current.pid}  |  "
        gc_t += f"{time}     "

#advance time and mark process as completed
        time = current.completion
        completed += 1

#final timestamp for gantt chart
    gc_t += f"{time}"

    #display results
    print("\n=== SJF Non-Preemptive Scheduling ===")
    print("Gantt Chart:")
    print(gc_p)
    print(gc_t)
    print_process_table(processes)

"""Shortest Job First (SJF) preemptive"""

def sjf_preemptive(processes):
  reset(processes)
  processes.sort(key=sort_key)
  completed = 0
  ready_queue = []
  current = None
  prev = None
  time = 0

  gc_p="|  "
  gc_t=str(time)+"      "

  while completed < len(processes): #runs until all processes are done

    #Adding processes to ready_queue
    for p in processes:
      #add whichever arrived, not completed, not in queue
      if p.arrival <= time and p.completion is None and p not in ready_queue:
        ready_queue.append(p)

    if not ready_queue:
      time += 1
      continue

    #Find the process with shortest remaining time in the ready queue
    current = ready_queue[0]
    for p in ready_queue:
      if p.remaining < current.remaining:
        current = p
      if p.remaining == current.remaining:
        if p.arrival > current.arrival:
          current = p

    if current.start is None:
      current.start = time

    #Updating gantt chart
    if time == 0:
      gc_p += f"P{current.pid}  |   "
      prev = current

    if current != prev:
      gc_p += f"P{current.pid}  |   "
      gc_t += f"{time}      "
      prev = current

    #Running current process for 1 time unit
    current.remaining -= 1
    time += 1


    #check if finished and remove from queue
    if current.remaining == 0:
      current.completion = time
      current.calculate_metrics() #calculate turnaround and waiting time
      ready_queue.remove(current)
      completed += 1
      current = None

  gc_t += f"{time}"
  print("\n=== SJF Preemptive Scheduling ===")
  print("Gantt Chart:")
  print(gc_p)
  print(gc_t)
  print()
  print_process_table(processes)

"""Round Robin Gantt Chart Printer"""

def print_gantt_chart_rr(timeline):
    chart = "" #This will hold the process blocks like
    time_str = "" #This will hold the timeline below the chart
    current_time = 0 #Tracks the current time
    for pid, start, end in timeline:

      #If there is a gap between the last end time and the next start time, do:
        if start > current_time:

            chart += "| Idle  " #Add idle block to Gantt chart
            time_str += str(current_time).ljust(7)
            #.ljust(7) : left justify a width of 7 characters to look neater .
            current_time = start # Update current time to the start of next process
            
        chart += f"| P{pid} ".ljust(7) #Add current process block to Gantt chart
        time_str += str(start).ljust(7) #Add the start time of this process
        current_time = end #Update current time to the end of current process
    time_str += str(current_time).ljust(7) # Add the final time value
    chart += "|" #Close the Gantt chart with a final bar
    print("Gantt Chart:")
    print(chart)
    print(time_str)

"""Round Robin (RR)"""

def round_robin(processes, quantum):
    from collections import deque

    reset(processes)

    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival)

    n = len(processes)
    queue = deque()
    time = 0
    completed = 0
    visited = [False] * n
    timeline = []

    while completed < n:
        # Add processes that have arrived to the queue
        for i in range(n):
            p = processes[i]
            if not visited[i] and p.arrival <= time:
                queue.append(p)
                visited[i] = True

        if not queue:
            time += 1
            continue

        current = queue.popleft()

        if current.start is None:
           current.start = time

        exec_time = min(current.remaining, quantum)
        start_time = time
        time += exec_time
        end_time = time
        timeline.append((current.pid, start_time, end_time))


        current.remaining -= exec_time

        # Check for newly arrived processes during execution
        for i in range(n):
            p = processes[i]
            if not visited[i] and p.arrival <= time:
                queue.append(p)
                visited[i] = True

        if current.remaining > 0:
            queue.append(current)  # Re-queue if not finished
        else:
            current.completion = time
            current.calculate_metrics()
            completed += 1


    print("\n=== Round Robin Scheduling (Quantum = {}) ===".format(quantum))
    print_gantt_chart_rr(timeline)
    print_process_table(processes)


"""Main function"""
while True:
    try:
        n = int(input("Enter number of processes: "))
        q = int(input("Enter quantum time: "))
        processes = []

        for p in range(n):
            try:
                burst = int(input("Enter burst time for process P" + str(p + 1) + ": "))
                process = Process(p + 1, burst)
                processes.append(process)
            except ValueError:
                print("Invalid burst time. Starting over.\n")
                break
        else:
            arrive = input("Do you have arrival time? (Y/N): ")
            if arrive.upper() == 'Y':
                for p in range(n):
                    try:
                        arr = int(input("Enter arrival time for process P" + str(p + 1) + ": "))
                        processes[p].arrival = arr
                    except ValueError:
                        print("Invalid arrival time. Starting over.\n")
                        break
                else:
                    fcfs(processes)
                    sjf_non_preemptive(processes)
                    sjf_preemptive(processes)
                    round_robin(processes, q)
            else:
                fcfs(processes)
                sjf_non_preemptive(processes)
                sjf_preemptive(processes)
                round_robin(processes, q)

        cont = input("Do you want to continue? (Y/N): ")
        if cont.upper() == 'N':
            break

    except ValueError:
        print("Invalid input. Please enter a number.\n")
