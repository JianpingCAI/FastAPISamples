import subprocess
from typing import List, Tuple, Optional, Dict
import os
import threading
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class JobResult:
    def __init__(
        self, job: "Job", stdout: str, stderr: str, success: bool, execution_time: str
    ):
        """
        Represents the result of a job execution.

        :param job: The job that was executed.
        :param stdout: The standard output of the job.
        :param stderr: The standard error of the job.
        :param success: Boolean indicating whether the job was successful.
        :param execution_time: Timestamp of when the job was executed.
        """
        self.job = job
        self.stdout = stdout
        self.stderr = stderr
        self.success = success
        self.execution_time = execution_time


class Job:
    def __init__(
        self, name: str, command: str, environment: Optional[Dict[str, str]] = None
    ):
        """
        Represents a job that executes a specific command.

        :param name: The name of the job.
        :param command: The command to be executed.
        :param environment: Optional dictionary of environment variables for the job.
        """
        self.name: str = name
        self.command: str = command
        self.environment: Optional[Dict[str, str]] = environment or dict(os.environ)
        self.result: Optional[JobResult] = None  # Holds the result of the job execution


class EnvironmentSetupJob(Job):
    def __init__(self, name: str, setup_script: str, args: Optional[List[str]] = None):
        """
        Special job for setting up the environment with optional arguments.

        :param name: The name of the job.
        :param setup_script: The script that sets up the environment.
        :param args: A list of arguments to pass to the setup script.
        """
        command = setup_script
        if args:
            command += " " + " ".join(args)
        super().__init__(name, command)


class Stage:
    def __init__(self, name: str, parallel: bool = False):
        """
        Represents a stage in the pipeline, which contains multiple jobs.

        :param name: The name of the stage.
        :param parallel: Whether the jobs in this stage should be executed in parallel.
        """
        self.name: str = name
        self.jobs: List[Job] = []
        self.parallel: bool = parallel
        self.results: List[JobResult] = []  # Stores results of jobs within the stage

    def add_job(self, job: Job):
        """
        Adds a job to the stage.

        :param job: The job to add.
        """
        self.jobs.append(job)


class Pipeline:
    def __init__(self):
        """
        Represents a pipeline consisting of multiple stages.
        """
        self.stages: List[Stage] = []
        self.stage_dependencies: Dict[str, List[str]] = (
            {}
        )  # Maps stage names to their dependencies

    def add_stage(self, stage: Stage, dependencies: Optional[List[str]] = None):
        """
        Adds a stage to the pipeline.

        :param stage: The stage to add.
        :param dependencies: List of stage names that must complete before this stage can run.
        """
        self.stages.append(stage)
        if dependencies:
            self.stage_dependencies[stage.name] = dependencies
        else:
            self.stage_dependencies[stage.name] = []


class PipelineExecutor:
    def __init__(self, pipeline: Pipeline):
        """
        Initializes the PipelineExecutor, which manages the execution of a given pipeline.

        :param pipeline: The pipeline to be executed.
        """
        self.pipeline = pipeline
        self.results: List[JobResult] = []  # Stores results of all jobs in the pipeline

    def execute_stage(self, stage: Stage):
        """
        Executes a single stage, either sequentially or in parallel.
        """
        logging.info(f"Executing Stage: {stage.name}")
        if stage.parallel:
            threads = []
            for job in stage.jobs:
                thread = threading.Thread(target=self.execute_job, args=(job, stage))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
        else:
            for job in stage.jobs:
                self.execute_job(job, stage)

    def execute_job(self, job: Job, stage: Stage):
        """
        Executes a single job and stores the result.
        """
        logging.info(f"  Executing Job: {job.name}")
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        process = subprocess.Popen(
            job.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=job.environment if job.environment else os.environ.copy(),
        )
        # Log output in real-time
        stdout, stderr = "", ""
        for stdout_line in iter(process.stdout.readline, ""):
            logging.info(f"  [STDOUT] {stdout_line.strip()}")
            stdout += stdout_line
        for stderr_line in iter(process.stderr.readline, ""):
            logging.error(f"  [STDERR] {stderr_line.strip()}")
            stderr += stderr_line
        process.stdout.close()
        process.stderr.close()
        return_code = process.wait()
        success = return_code == 0
        if success:
            logging.info(f"  Job '{job.name}' completed successfully")
        else:
            logging.error(f"  Job '{job.name}' failed with return code {return_code}")
            self.send_failure_notification(job, stdout, stderr)

        # Create and store the job result
        job_result = JobResult(
            job=job,
            stdout=stdout.strip(),
            stderr=stderr.strip(),
            success=success,
            execution_time=start_time,
        )
        job.result = job_result
        stage.results.append(job_result)
        self.results.append(job_result)

    def send_failure_notification(self, job: Job, stdout: str, stderr: str):
        """
        Sends an email notification when a job fails.

        :param job: The job that failed.
        :param stdout: The standard output of the job.
        :param stderr: The standard error of the job.
        """
        sender_email = "your_email@example.com"
        recipient_email = "recipient_email@example.com"
        subject = f"Job Failure Notification: {job.name}"
        body = f"""
        The job '{job.name}' has failed.

        Command: {job.command}

        Standard Output:
        {stdout}

        Standard Error:
        {stderr}
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login(sender_email, "your_password")
                server.sendmail(sender_email, recipient_email, msg.as_string())
                logging.info(f"Failure notification sent for job '{job.name}'")
        except Exception as e:
            logging.error(f"Failed to send notification for job '{job.name}': {e}")

    def execute(self):
        """
        Executes each stage in the pipeline, respecting dependencies.
        """
        executed_stages = set()

        while len(executed_stages) < len(self.pipeline.stages):
            for stage in self.pipeline.stages:
                if stage.name in executed_stages:
                    continue

                # Check if all dependencies have been executed
                dependencies = self.pipeline.stage_dependencies.get(stage.name, [])
                if all(dep in executed_stages for dep in dependencies):
                    self.execute_stage(stage)
                    executed_stages.add(stage.name)

    def get_pipeline_results(self) -> List[Dict[str, str]]:
        """
        Returns the results of the entire pipeline for frontend UI.

        :return: List of dictionaries representing job results.
        """
        results = []
        for result in self.results:
            results.append(
                {
                    "job_name": result.job.name,
                    "command": result.job.command,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "success": "Yes" if result.success else "No",
                    "execution_time": result.execution_time,
                }
            )
        return results


class TestAction:
    def __init__(
        self,
        name: str,
        script_path: str,
        script_type: str = "python",
        args: Optional[List[str]] = None,
    ):
        """
        Represents an individual action within a test case.

        :param name: The name of the action.
        :param script_path: The path to the script to be executed.
        :param script_type: The type of script ('python', 'bash', or other).
        :param args: Optional list of arguments to be passed to the script.
        """
        self.name: str = name
        self.script_path: str = script_path
        self.script_type: str = script_type
        self.args: Optional[List[str]] = args


class TestCase:
    def __init__(self, name: str, actions: List[TestAction]):
        """
        Represents a test case containing multiple actions.

        :param name: The name of the test case.
        :param actions: List of actions within the test case.
        """
        self.name: str = name
        self.actions: List[TestAction] = actions


class TestSuite:
    def __init__(self, name: str, cases: List[TestCase]):
        """
        Represents a test suite containing multiple test cases.

        :param name: The name of the test suite.
        :param cases: List of test cases within the test suite.
        """
        self.name: str = name
        self.cases: List[TestCase] = cases

    def to_pipeline(self) -> Pipeline:
        """
        Converts the TestSuite object into a Pipeline with stages and jobs.

        :return: A Pipeline object representing the test suite.
        """
        pipeline = Pipeline()

        for test_case in self.cases:
            stage = Stage(name=test_case.name, parallel=False)

            for action in test_case.actions:
                if action.script_type == "python":
                    command = f"python {action.script_path}"
                elif action.script_type == "bash":
                    command = f"bash {action.script_path}"
                else:
                    command = action.script_path

                if action.args:
                    command += " " + " ".join(action.args)
                job = Job(name=action.name, command=command)
                stage.add_job(job)

            pipeline.add_stage(stage)

        return pipeline


# Example usage
if __name__ == "__main__":
    # Create test actions
    action1 = TestAction(
        name="List Directory", script_path="list_dir.sh", script_type="bash"
    )
    action2 = TestAction(
        name="Print Working Directory", script_path="print_pwd.py", script_type="python"
    )
    action3 = TestAction(
        name="Echo Hello",
        script_path="echo_hello.sh",
        script_type="bash",
        args=["Hello"],
    )

    # Create test cases
    test_case1 = TestCase(name="Test Case 1", actions=[action1, action2])
    test_case2 = TestCase(name="Test Case 2", actions=[action3])

    # Create a test suite
    test_suite = TestSuite(name="Sample Test Suite", cases=[test_case1, test_case2])

    # Convert the test suite to a pipeline
    pipeline = test_suite.to_pipeline()

    # Execute the pipeline
    executor = PipelineExecutor(pipeline)
    executor.execute()

    # Get pipeline results
    results = executor.get_pipeline_results()
    for result in results:
        print(result)
