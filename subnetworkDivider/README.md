# Network divider

It's a simple program for divide network to subnetworks with particular hosts count.
Dividing implemented the most economical partitioning.

Example:

`./main.py 192.168.0.0/24 2 2 2`

Result:

```
Network size: 2		192.168.0.0/30
Network size: 2		192.168.0.4/30
Network size: 2		192.168.0.8/30
```
