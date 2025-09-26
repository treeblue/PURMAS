## Python Utility for Resource Managment and Scheduling


# src/main.py
Runs a controller in the terminal, can interact using different commands.
Type "help" to show commands

# src/worker.py
Runs a worker in the terminal, gets sent messages from the controller.

# src/config.txt
Holds a configuration file just with controller and worker IP addresses, eg:

```
    Controller: {IP of controller node}
    Node: {Name of worker node} {IP of worker node}
```

Deviations of this format could result in unexpected behaviour