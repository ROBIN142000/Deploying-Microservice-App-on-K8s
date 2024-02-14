import csv, os

def csv_or_not(username):
    if not os.path.isfile(f"CSVs/{username}.csv"):
        with open(f"CSVs/{username}.csv", 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Id", "Task", "Time"])

def initialize_tasklist(username):
    list = []
    id = 0

    with open(f"CSVs/{username}.csv") as csv_file:
        reader = csv.reader(csv_file)
        for iD, task, time in reader:
            id+=1
            list.append(
                [iD, task, time]
            )
    return list

def compile_csv(username, list):
    with open(f"CSVs/{username}.csv", 'w', newline='') as tasklist:
            writer = csv.writer(tasklist)
            for i in range(0, len(list)):
                writer.writerow([f"{list[i][0]}", f"{list[i][1]}", f"{list[i][2]}"])

def add_task(task_row, username):
    tasklist = initialize_tasklist(username)        
    tasklist.append([len(tasklist), task_row[0], task_row[1]])
    compile_csv(username, tasklist)

def edit(username, task, time, id):
    tasklist = initialize_tasklist(username)
    tasklist[int(id)] = [id, task, time]
    compile_csv(username, tasklist)
    return tasklist

def delete_task(username, id):
    tasklist = initialize_tasklist(username)
    tasklist.pop(int(id))
    for iteration in range(int(id), len(tasklist)):
        new_id = int(tasklist[iteration][0]) - 1
        tasklist[iteration][0] = new_id
        id = new_id
    
    compile_csv(username, tasklist)

def clear_list(username):
    tasklist = initialize_tasklist(username)
    del tasklist[1:len(tasklist)]
    compile_csv(username, tasklist)