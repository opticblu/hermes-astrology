"""Profile isolation at the two shared server entry points."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


class TestHTTPBirthData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from fastapi.testclient import TestClient
        except ImportError as error:
            raise unittest.SkipTest("FastAPI and its test client are optional") from error

        temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temp.cleanup)
        cls.legacy = Path(temp.name) / ".astro_profiles.json"
        cls.old_data = '{"legacy-user": {"year": 1985}}'
        cls.legacy.write_text(cls.old_data)

        env = patch.dict(os.environ, {"ASTRO_PROFILE_DIR": temp.name, "ASTRO_API_KEY": ""})
        env.start()
        cls.addClassCleanup(env.stop)
        from api import app
        cls.client = TestClient(app)
        cls.addClassCleanup(cls.client.close)

    def test_legacy_profile_routes_are_unavailable(self):
        self.assertEqual(self.client.post("/profile", json={
            "name": "legacy-user", "year": 2000, "month": 1, "day": 3
        }).status_code, 404)
        self.assertEqual(self.client.get("/profile/legacy-user").status_code, 404)
        self.assertEqual(self.client.delete("/profile/legacy-user").status_code, 404)
        self.assertEqual(self.legacy.read_text(), self.old_data)

    def test_session_id_cannot_recover_birth_details(self):
        query = {
            "session_id": "group-chat",
            "messages": [{"role": "user", "content": "birth chart"}],
        }
        birth = {"year": 2000, "month": 1, "day": 3, "systems": ["western"]}
        reading = self.client.post("/interact", json={**query, "profile": birth})
        self.assertEqual(reading.status_code, 200)
        self.assertTrue(reading.json()["results"][0]["ok"])
        self.assertEqual(reading.json()["session_id"], "group-chat")

        missing_birth = self.client.post("/interact", json=query)
        self.assertEqual(missing_birth.status_code, 422)
        self.assertIn(["body", "profile"], [err["loc"] for err in missing_birth.json()["detail"]])


class TestMCPBirthData(unittest.IsolatedAsyncioTestCase):
    async def test_tool_catalog_has_charts_without_profile_access(self):
        try:
            from mcp.server.fastmcp import FastMCP
        except ImportError as error:
            self.skipTest("MCP v1 is optional")
        from mcp_server import mcp
        names = {tool.name for tool in await mcp.list_tools()}
        self.assertIn("get_astrology_chart", names)
        self.assertTrue({"save_profile", "get_profile"}.isdisjoint(names))
