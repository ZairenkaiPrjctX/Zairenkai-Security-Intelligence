import unittest

from zsi.report import normalize_osv, validate_report


class ReportTests(unittest.TestCase):
    def test_osv_finding_maps_to_affected_without_invented_severity(self):
        report = normalize_osv({"results": [{"source": {"path": "requirements.txt"}, "packages": [{"package": {"name": "demo", "version": "1.0", "ecosystem": "PyPI"}, "vulnerabilities": [{"id": "GHSA-test", "aliases": ["CVE-2099-0001"], "affected": [{"ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.2"}]}]}], "references": [{"url": "https://example.test/advisory"}]}]}]}]}, "sample", "abc123", "2026-01-01T00:00:00Z")
        finding = report["findings"][0]
        self.assertEqual(finding["status"], "AFFECTED")
        self.assertEqual(finding["severity"], "UNKNOWN")
        self.assertEqual(finding["fixed_versions"], ["1.2"])
        self.assertEqual(finding["affected_ranges"][0]["events"][-1], {"fixed": "1.2"})
        self.assertEqual(validate_report(report), [])

    def test_empty_scanner_result_is_not_clean_claim(self):
        report = normalize_osv({"results": []}, "sample", "abc123", "2026-01-01T00:00:00Z")
        self.assertEqual(report["findings"], [])
        self.assertIn("No finding is not proof of safety.", report["limitations"])
        self.assertEqual(report["coverage"]["status"], "PARTIAL")

    def test_rejects_unsupported_fixed_assertion(self):
        report = normalize_osv({"results": []}, "sample", "abc123", "2026-01-01T00:00:00Z")
        report["findings"] = [{"status": "FIXED"}]
        self.assertTrue(any("unsupported" in error for error in validate_report(report)))


if __name__ == "__main__":
    unittest.main()
