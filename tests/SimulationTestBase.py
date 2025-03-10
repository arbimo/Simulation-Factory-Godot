import unittest
import subprocess
import os

from ..clients.python_client.CompleteClient import CompleteClient

class SimulationTestBase(unittest.TestCase):
    #contains the functions executed at the beginning and end of each test, taking care of starting the simulation and connecting the client

    def setUp(self):
        self.client = CompleteClient("localhost",10000)
        
        self.sim = subprocess.Popen([os.environ["GODOT_PATH"], "--main-pack", " Simulation-Factory-Godot/simu/simulation.pck",
            "--scenario", os.environ["GITHUB_WORKSPACE"] + "/simu/scenarios/new_scenario.json",
            "--environment", os.environ["GITHUB_WORKSPACE"] + "/simu/environments/new_environment.json"])

        self.assertTrue(self.client.wait_for_server(timeout=10))

    def tearDown(self):
        self.client.kill()
        self.sim.kill()
        self.sim.wait()

