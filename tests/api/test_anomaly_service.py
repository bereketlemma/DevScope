"""Tests for the API service."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from services.anomaly_service import AnomalyService


class TestAnomalyZScore:
    """Tests for z-score severity classification."""

    def test_severity_medium(self):
        assert AnomalyService._classify_severity_zscore(2.5) == "MEDIUM"

    def test_severity_high(self):
        assert AnomalyService._classify_severity_zscore(3.5) == "HIGH"

    def test_severity_critical(self):
        assert AnomalyService._classify_severity_zscore(4.5) == "CRITICAL"

    def test_severity_boundary_high(self):
        assert AnomalyService._classify_severity_zscore(3.0) == "HIGH"

    def test_severity_boundary_critical(self):
        assert AnomalyService._classify_severity_zscore(4.0) == "CRITICAL"


class TestAnomalyVertexSeverity:
    """Tests for Vertex AI confidence-based severity."""

    def test_vertex_medium(self):
        assert AnomalyService._classify_severity(0.85) == "MEDIUM"

    def test_vertex_high(self):
        assert AnomalyService._classify_severity(0.92) == "HIGH"

    def test_vertex_critical(self):
        assert AnomalyService._classify_severity(0.97) == "CRITICAL"
