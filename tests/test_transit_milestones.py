"""Regression tests for measured transit milestones, using a fictional chart."""
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import astro_engine as ae


class TestTransitMilestones(unittest.TestCase):
    birth = {"date": "2001-05-01", "time": "22:00", "utc_offset": -6,
             "lat": 32, "lng": -90, "systems": ["western"]}

    def test_uranus_opposition_uses_positions_and_target_date(self):
        birth_utc = datetime(2001, 5, 2, 4)
        natal = ae.body_longitudes(ae.julian_day(birth_utc))[0]["Uranus"]
        for year, active in ((2043, False), (2045, True)):
            target = datetime(year, 5, 1)
            current = ae.body_longitudes(ae.julian_day(target))[0]["Uranus"]
            for mode in ("natal", "transit"):
                with self.subTest(year=year, mode=mode):
                    profile = ae.calculate_full_profile({
                        **self.birth, "transit_date": target.date().isoformat(), "mode": mode})
                    phase = profile["life_phase"]
                    self.assertEqual(phase["as_of_utc"], target.isoformat() + "Z")
                    self.assertAlmostEqual(phase["current_age"], year - 2001, places=1)
                    hit = phase["cycle_aspects"]["Uranus Opposition"]
                    self.assertAlmostEqual(hit["natal_longitude_deg"], natal, places=4)
                    self.assertAlmostEqual(hit["transit_longitude_deg"], current, places=4)
                    separation = abs((current - natal + 180) % 360 - 180)
                    self.assertAlmostEqual(hit["separation_deg"], separation, places=4)
                    self.assertAlmostEqual(hit["orb_deg"], 180 - separation, places=4)
                    self.assertEqual(hit["active"], active)
                    self.assertEqual("Uranus Opposition" in phase["active_milestones"], active)
                    self.assertEqual(hit["active"], hit["orb_deg"] <= phase["orb_limit_deg"])

    def test_date_only_chart_separates_birth_date_and_observation_date(self):
        data = {**self.birth, "time_known": False}
        for _ in range(2):  # A second call with the same dict must behave identically.
            before = datetime.now(timezone.utc)
            phase = ae.calculate_full_profile(data)["life_phase"]
            observed = datetime.fromisoformat(phase["as_of_utc"].replace("Z", "+00:00"))
            self.assertLessEqual(before, observed)
            self.assertLessEqual(observed, datetime.now(timezone.utc))
        phase = ae.calculate_full_profile({**data, "as_of": "2010-05-06"})["life_phase"]
        self.assertEqual(phase["as_of_utc"], "2010-05-06T00:00:00Z")
        self.assertEqual(phase["current_age"], 9.0)

    def test_bad_observation_date_is_reported(self):
        with self.assertRaisesRegex(ValueError, "as_of"):
            ae.calculate_full_profile({**self.birth, "as_of": "not-a-date"})

    def test_initial_conjunction_is_not_a_completed_return(self):
        birth = datetime(2001, 5, 2, 4)
        phase = ae.life_phase(birth, birth)
        self.assertEqual(phase["active_milestones"], [])
        self.assertEqual(phase["cycle_aspects"]["Saturn Return"]["orb_deg"], 0)

    def test_detailed_transit_mode_shares_evaluation_time(self):
        details = ae.calculate_full_profile({
            **self.birth, "mode": "transit_natal_aspects", "as_of": "2045-05-01T06:15:00+02:00"
        })["transit_natal_aspects"]
        self.assertEqual(details["as_of_utc"], "2045-05-01T04:15:00Z")

    def test_detailed_opposition_signed_distance_and_orb(self):
        for longitude, speed, applying in ((157, 0.1, True), (157, -0.1, False),
                                            (163, 0.1, False), (163, -0.1, True),
                                            (156.99, 0.1, None)):
            with self.subTest(longitude=longitude, speed=speed):
                natal = ({"Uranus": 340}, {}, "test")
                transit = ({"Uranus": longitude}, {"Uranus": speed}, "test")
                with patch.object(ae, "body_longitudes", side_effect=[natal, transit]):
                    aspects = ae.transit_to_natal_aspects(0, 1)["transit_aspects"]
                if applying is None:
                    self.assertEqual(aspects, [])
                else:
                    self.assertEqual(aspects[0]["aspect"], "opposition")
                    self.assertEqual(aspects[0]["orb"], 3)
                    self.assertEqual(aspects[0]["applying"], applying)


if __name__ == "__main__":
    unittest.main()
