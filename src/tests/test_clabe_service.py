# import json
# import unittest

# from fastapi.testclient import TestClient

# from .. import __version__
# from ..main import app
# from .factories import ExampleModelFactory

# # # INITIALIZE DEBUGPY FOR VSCODE DEBUG --OPTIONAL ONLY FOR DEV
# # import debugpy


# class TestExample(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         # # INITIALIZE DEBUGPY FOR VSCODE DEBUG --OPTIONAL ONLY FOR DEV
#         # import debugpy

#         # debugpy.listen(("0.0.0.0", 3002))
#         # debugpy.wait_for_client()
#         # print("Attached!")

#         cls.client = TestClient(app)

#     def test_version(self):
#         assert __version__ == "0.1.0"

#     def test_read_health(self):
#         response = self.client.get("/api/v1/health")
#         expected_response = {"status": "ok"}
#         assert json.loads(response.text) == expected_response
#         assert response.status_code == 200

#     def test_read_example(self):
#         response = self.client.post("/api/v1/example")
#         expected_response = None
#         assert json.loads(response.text) == expected_response
#         assert response.status_code == 200

#     def test_read_example_no_parameters(self):
#         response = self.client.get("/api/v1/example")
#         expected_response = {
#             "detail": [
#                 {
#                     "loc": ["query", "example"],
#                     "msg": "field required",
#                     "type": "value_error.missing",
#                 }
#             ]
#         }
#         assert json.loads(response.text) == expected_response
#         assert response.status_code == 422
