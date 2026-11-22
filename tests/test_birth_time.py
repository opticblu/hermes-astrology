"""Date-only charts must not infer angles, houses or a precise lunar position."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import astro_engine as ae

CHICAGO = {"year": 2000, "month": 6, "day": 15, "lat": 41.8781,
           "lng": -87.6298, "tz": "America/Chicago"}


class TestBirthTime(unittest.TestCase):
    def test_time_inference_and_explicit_override(self):
        for clock in ({}, {"hour": None}, {"time_known": True}, {"time_known": True, "hour": None},
                      {"hour": 0, "time_known": False}, {"time": "14:30", "time_known": False}):
            with self.subTest(clock=clock):
                chart = ae.calculate_full_profile({**CHICAGO, "advanced": True, **clock})
                self.assertFalse(chart["time_info"]["time_known"])
                self.assertNotIn("ascendant", chart["summary"]["big_three"])
                self.assertNotIn("birth_utc", chart["_meta"])
                self.assertIsNone(chart["_meta"]["house_system"])
                self.assertNotIn("upagrahas", chart)
                self.assertNotIn("lagna", chart["charts"]["vedic"])
                self.assertNotIn("hour", chart["charts"]["bazi"]["four_pillars"])
                for system in ("western", "vedic"):
                    detail = chart["charts"][system]
                    self.assertNotIn("houses", detail)
                    self.assertNotIn("ascendant", detail)
                    self.assertIsNone(detail["house_system"])
                    for planet in detail["planets"].values():
                        self.assertTrue(set(planet) <= {"sign", "possible_signs"})
        with self.assertRaisesRegex(ValueError, "time_known must be a boolean"):
            ae.calculate_full_profile({**CHICAGO, "hour": 5, "time_known": "false"})
        for clock in ({"hour": 0}, {"time": "00:00"}, {"hour": 12, "time_known": True}):
            chart = ae.calculate_full_profile({**CHICAGO, **clock})
            self.assertTrue(chart["time_info"]["time_known"])
            self.assertIn("ascendant", chart["summary"]["big_three"])
            self.assertIn("house", chart["charts"]["western"]["planets"]["Sun"])

    def test_moon_changes_on_local_dst_date(self):
        civil = {**CHICAGO, "year": 2024, "month": 3, "day": 10}
        chart = ae.calculate_full_profile(civil)
        self.assertEqual(chart["summary"]["big_three"], {"sun": "Pisces", "moon_possible_signs": ["Pisces", "Aries"]})
        western = chart["charts"]["western"]
        self.assertEqual(western["planets"]["Moon"], {"possible_signs": ["Pisces", "Aries"]})
        self.assertEqual(chart["charts"]["vedic"]["janma_rashi"], {"possible_signs": ["Aquarius", "Pisces"]})
        utc = ae.calculate_full_profile({**civil, "tz": "UTC"})
        self.assertEqual(utc["charts"]["western"]["planets"]["Moon"], {"sign": "Pisces"})

    def test_different_traditions_can_disagree_on_an_ingress(self):
        chart = ae.calculate_full_profile({**CHICAGO, "day": 16})
        self.assertEqual(chart["summary"]["big_three"]["moon"], "Sagittarius")
        self.assertEqual(chart["charts"]["vedic"]["planets"]["Moon"],
                         {"possible_signs": ["Scorpio", "Sagittarius"]})

    def test_unknown_partner_or_primary_never_gets_house_overlays(self):
        person_a = {**CHICAGO, "day": 14}
        person_b = {**CHICAGO, "year": 1999, "hour": 9}
        for a, b, unknown_side in [(person_a, person_b, "personA"), (person_b, person_a, "personB")]:
            request = {**a, "mode": "synastry", "partner": b}
            result = ae.calculate_full_profile(request)
            self.assertNotIn("house_overlays", result)
            self.assertNotIn("ibn_ezra_lots", result)
            self.assertNotIn("rising", result[unknown_side]["big_three"])
            self.assertIn("moon_possible_signs", result[unknown_side]["big_three"])
            for aspect in result["synastry"]["inter_aspects"]:
                self.assertNotEqual(aspect[f"{unknown_side}_planet"], "Moon")
            for mode in ("davison", "composite", "guna_milan"):
                self.assertIn("error", ae.calculate_full_profile({**request, "mode": mode}))

    def test_derived_modes_and_events(self):
        self.assertIn("error", ae.calculate_full_profile({**CHICAGO, "mode": "profections"}))
        transit = ae.calculate_full_profile({**CHICAGO, "mode": "transit", "transit_date": "2024-03-10"})
        self.assertNotIn("rising", transit["natal_brief"])
        self.assertNotIn("sade_sati", transit["transits"])
        for aspect in transit["transits"]["aspects_to_natal"]:
            self.assertNotEqual(aspect["to_natal"], "Moon")
        event = ae.calculate_full_profile({**CHICAGO, "mode": "event"})["event_chart"]
        self.assertNotIn("lagna", event["vedic"])
        self.assertNotIn("houses", event["western"])


if __name__ == "__main__":
    unittest.main()
