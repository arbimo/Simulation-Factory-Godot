import unittest

from .SimulationTestBase import SimulationTestBase
from ..clients.python_client.CompleteClient import CompleteClient

class NavigationTests(SimulationTestBase):

    def test_navigate_to(self):

        client = CompleteClient("localhost",10000)
        self.assertTrue(client.wait_for_server(10))

        try:
            action_id = client.ActionClientManager.run_command(['navigate_to','robot0', 15, 15])
            self.assertTrue(client.ActionClientManager.wait_result(action_id,10))

            final_position = client.StateClient.robot_coordinates('robot0')
            distance_squared = (final_position[0]-15)**2 + (final_position[1]-15)**2
            self.assertTrue(distance_squared<=0.1)
        finally:
            client.kill()

    def test_navigate_to_area(self):

        client = CompleteClient("localhost",10000)
        self.assertTrue(client.wait_for_server(10))

        try:
            self.assertTrue(client.StateClient.wait_for_message("Parking_area.instance", 10))
            target_parking_area = client.StateClient.parking_areas_list()[0]

            action_id = client.ActionClientManager.run_command(['navigate_to_area','robot0',target_parking_area])
            self.assertTrue(client.ActionClientManager.wait_result(action_id,10))
            self.assertTrue(client.StateClient.robot_in_station('robot0'))
            

            target_interact_area = client.StateClient.interact_areas_list()[0]

            action_id = client.ActionClientManager.run_command(['navigate_to_area','robot0',target_interact_area])
            self.assertTrue(client.ActionClientManager.wait_result(action_id,10))
            self.assertTrue(target_interact_area in client.StateClient.robot_in_interact_areas('robot0'))
        finally:
            client.kill()
            
if __name__ == '__main__':
    unittest.main()
