'''
The concept of this project.
Every time frame, all workcells are checked for idle condition (projected next production time is in the past).
At that same time frame, idle workcell will be assigned with "job" and the projected next production time will be updated.
Each time one workcell is assigned the "job" and completes the execution, one block will be mined.
The assignment might be from sequential transfer of workpiece or redistributed transfer based on distribution algorithm.
This means that at for every time frame, multiple workcells might complete their own execution and each mines a block,
resulting in multiple blocks being mined.

The direction from blockchain base to CPS is termed download and process.
'''