# IntelligentCPS - Cognitive Engine
This is a project of NUS Control & Mechatronics Lab under guidance of Prof. Chui Chee Kong. This project contains a Block Chain that carries out validation of manufacturing inspection when the manufacturing operation is made up of sequential steps. This repository is meant for simulations of the project.

> Note:
> * Information on the research group can be found in http://blog.nus.edu.sg/mpecck/.

## 1. IntelligentCPS Components
This project is under the umbrella of the IntelligentCPS project. The processes and resources are encapsulated in the following manner.
![iCPS Components](assets/cps_components.png)
1. The component ```step``` refers to the lowest level of instruction for the process.
2. The component ``` task``` refers to the highest level of instruction for the process. For example, "Fabricate product A" is a task.
3. The component ``` objective``` refers to the instruction that is between ```step``` and ```task```. This can be broken down into multiple layers. Among them, the lowest layer is ```objective_layer_1```.
4. Executors of a job execution depends on the resources within the assigned location.

> Note:
> * A job ties multiple ```task``` components in an unordered manner as a single job submission.
> * An executor is a resource assigned to execute a step.
> * Execution is done at the lowest level, which is at the step layer.

### Step Conditions
There are six conditions that govern the process control of the executable steps, which determines the step sequence based on the states detected and the steps completed.
If a blocker step can be executed, then the step with this condition cannot be carried out.
```
condition: isBlockedByStep
blocker_step: The set of steps that should not be executable at that time in order for the step to be executable.
```
If a blocker state is detected, then the step with this condition cannot be carried out.
```
condition: isBlockedByState
blocker_state: The set of states that should not be detected in order for the step to be executable.
```
If all the prerequisite steps defined in this condition has been completed successfully, then only the step with this condition can be carried out.
```
condition: hasPrerequisiteStep
prerequisite_step: The set of steps that should be completed in order for the step to be executable.
```
If all the prerequisite states defined in this condition are detected at that time, then only the step with this condition can be carried out.
```
condition: hasPrerequisiteState
prerequisite_state: The set of states that should be detected in order for the step to be executable.
```
If the ```hasPrerequisiteState``` set is detected, and if all the correct states defined in this condition for that ```hasPrerequisiteState``` set are detected at that time, then only the step with this condition has been completed successfully.
```
condition: isAchievedBy
hasPrerequisiteState: The condition set where all the prerequisite states defined in it are detected at that time.
correct_state: The set of states that should be detected in order for the step to be completed successfully.
```
If the ```hasPrerequisiteState``` set is detected, and if all the correct states defined in this condition but any one of the wrong state defined in this condition for that ```hasPrerequisiteState``` set are detected at that time , then only the step with this condition has failed.
```
condition: isFailedByState
hasPrerequisiteState: The condition set where all the prerequisite states defined in it are detected at that time.
correct_state: The set of states that should be detected in order for the step to be completed successfully.
wrong_state: Any state element in this set if detected could cause the step to fail.
```

> Note: Please modify the contents below to suit this project.

## 2. Features
1. This CE generates an OWL ontology based on the conditions defined for each step.
2. The HermiT reasoner is used twice in a single cycle of the process control. The first reasoning infers the next step(s) that are executable. The second reasoning infers the status of completion for step(s), objective(s) and task.
3. Instances of step, resource and location are created during the process control for new knowledge and reasoning.
4. List of steps for each task that is possible to be executed is output to the ```state-buffer```.
5. The order of steps taken, number of success and failures of each step, and details of the step execution can be traced.

### Input
Input required for the CE includes:
1. Process ontology in excel format.
2. RestAPI POST to instantiate the CE.
3. RestAPI POST to report state details to the CE.

### Output
Output of the CE includes:
1. List of steps that can be executed based on the current states and conditions.
2. Status of the step, objectives, task and job.

## 3. Pre-Installation Check
1. This project was developed using [Pycharm IDE](https://www.jetbrains.com/pycharm/download/#section=windows) in [Python 3.6 x64 bit](https://www.python.org/downloads/release/python-366/) environment.
2. The lists of python packages required (with version number included) are documented in requirements.txt.
3. MongoDB is required to act as a buffer for data transfer and as a database for process status updates. To install on your system, follow the instructions provided on [MongoDB website](https://docs.mongodb.com/manual/installation/). [MongoDB Compass](https://www.mongodb.com/download-center/compass) is a GUI for the database.
4. Optional: [Protégé](https://protege.stanford.edu/) or [WebProtégé](https://webprotege.stanford.edu/) is the GUI to view the OWL ontology.
5. Optional: [Postman](https://www.getpostman.com/downloads/) can be used to test RestAPI development.

## 4. Installation in Windows
1. Clone this repository using [Git](https://git-scm.com/) or download this repository.
2. Create new new virtual environment for the project.
3. Install packages into the virtual environment from requirements.txt.
4. Duplicate the ```config_template.py``` file and rename the duplicate ```config.py```. This will serve as the config file for the application.
5. Edit the values in ```config.py``` accordingly.

## 5. Directory Structure
Ensure that all folders exists and are arranged as the basic suggested skeleton shown below. If different nomenclature is prefered, please edit the file access in the code before running it.

```cmd
.
+--- CognitiveEngine
¦   +--- blueprints
¦   ¦   +--- job_execution
¦   ¦   ¦   +--- templates
¦   ¦   ¦   +--- routes.py
¦   +--- data
¦   ¦   +--- **/*.csv
¦   ¦   +--- **/*.owl
¦   ¦   +--- **/*.sqlite3
¦   ¦   +--- **/*.sqlite-journal
¦   +--- functions
¦   ¦   +--- csv_functions.py
¦   ¦   +--- excel_functions.py
¦   ¦   +--- general_functions.py
¦   ¦   +--- mongo_functions.py
¦   ¦   +--- onto_functions.py
¦   +--- modules
¦   ¦   +--- cognitive_engine.py
¦   ¦   +--- status_collector.py
¦   +--- ontology
¦        +--- ProcessControlTemplate.owl
¦        +--- process_ontology_excel_template.xlsx
¦        +--- **/*.xlsx
+--- README.md
+--- run.py
+--- venv (library root)
+--- .gitignore
```

## 6. Data Structure
### Database
MongoDB uses NoSQL data structure, where each database could hold multiple collections. If ```_id``` is not assigned, an ObjectId is automatically generated and assigned as ```_id``` to the newly created document entry. Ensure that the following database and collections are created. If different nomenclature is prefered, please edit the file access in the ```mongo_functions``` before running it.
> Note:
> * ```object``` in NoSQL is equivalent to ```dict``` in python.
> * ```array``` in NoSQL is equivalent to ```list``` in python.

The broadcast-buffer collection has the following functions for this CE:
1. To check for conflict between outputs of step items before being broadcast.
2. To act as a buffer to collect the executable step items before being taken by a sink system (for example: IntelligentCPS) to be broadcast.

```
database: job-history
collection: broadcast-buffer
NoSQL data structure:
	job_id						# string
	blocker_list				# array of string
	output_list 				# array of string
	to_be_broadcast				# array of objects
		task_ObjectId			# string
		step_list				# array of int
```

The ```state-buffer``` collection has the following functions for this CE:
1. To act as a buffer to store states reported by various source systems through RestAPI (for example: IntelligentCPS-CT) before being retrived for process control reasoning.
```
database: job-history
collection: state-buffer
NoSQL data structure:
	task_ObjectId 				# string
	state_buffer				# array of object
	can_be_collected_flag		# bool
```

The ```job-task``` collection has the following functions for this CE:
1. To store task details and task status that are updated by the CE.
```
database: job-history
collection: job-task
NoSQL data structure:
	job_id 						# string
	var							# string
	datetime_start				# string
	datetime_end				# string
	status						# string
	...							(More objective layers)
	objective_layer_1			# array of object
		index					# int32
		var						# string
		datetime_start			# string
		datetime_end			# string
		status					# string
	step						# array of object
		index					# int32
		var						# string
		location_id				# string
		datetime_start			# string
		datetime_end			# string
		status					# string
		exec					# array of object
			index				# int32
			...					(Data used in IntelligentCPS and IntelligentCPS-CT projects)
			status				# string
	job_submission_timestamp	# string
	is_deleted					# bool
```

The ```user_id``` collection has the following functions for this CE:
1. To store information to tie multiple tasks as a single job that is submitted for operation.
```
database: job-history
collection: user_id
NoSQL data structure: {
	job_id						# string
	status						# string
	task_ObjectId				# array of string
```
> Note:
> * Collection name ```user_id``` follows the actual user_id defined arbitrarily that depends on the input to the CE.

### RestAPI
RestAPI uses JSON data structure.
The ```\job-execute\instantiate-ce``` route is used to instantiate the cognitive engine.
```
route-address: \job-execute\instantiate-ce
methods: POST
JSON data input:
	user_id						# str
	job_id						# str
	task_ObjectId				# str
	task_var					# str
```

The ```\job-execute\report-status``` and to receive states for process control reasoning. If multiple states are included, append to the ```state``` list.
```
route-address: \job-execute\report-status
methods: POST
JSON data input:
	task_ObjectId				# str
	user_id						# str
	step_index					# int
	exec_index					# int
	exec_id						# str
	exec_type					# str
	location_id					# str
	workcell_id					# str
	datetime_start				# str
	datetime_end				# str
	state						# list of dict
		value					# str
		superclass				# str
		type					# str
```

### Process Ontology
Duplicate ```process_ontology_excel_template.xlsx``` in the ```ontology``` folder and rename it. It is suggested to rename it using the task name ```task_var.xlsx```. Description of each column has been detailed in the comment of each header. If different nomenclature of the headers is prefered, please edit the file access in the ```exel_functions``` before running it.
> Note:
> * The condition sets should not be named but should be numbered.
> * The state, step, objective should be named.

### Generated OWL File
OWL ontology will be generated using the template ```ProcessControlTemplate.owl``` and the process ontology excel file that was prepared by the user under the suggested name of ```task_var.xlsx```, where both files are stored in stored in ```ontology``` folder.
The OWL ontology is generated and managed by a python module named [owlready2](https://owlready2.readthedocs.io/en/latest/). The generated OWL file is stored in ```data``` folder. Data that can be retrieved from the OWL file is shown in the diagram below.
