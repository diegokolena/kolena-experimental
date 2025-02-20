# Copyright 2021-2023 Kolena Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List
from typing import Tuple

import pytest

from kolena.workflow.annotation import LabeledBoundingBox
from kolena.workflow.annotation import ScoredLabeledBoundingBox
from kolena.workflow.plot import Curve
from kolena.workflow.plot import CurvePlot
from tests.integration._experimental.object_detection.test_evaluator_single_class_fixed import (
    assert_curve_plot_equal,
)
from tests.integration._experimental.object_detection.test_evaluator_single_class_fixed import (
    assert_test_case_metrics_equals_expected,
)
from tests.integration._experimental.object_detection.test_evaluator_single_class_fixed import TEST_DATA
from tests.integration.helper import fake_locator
from tests.integration.helper import with_test_prefix


object_detection = pytest.importorskip("kolena._experimental.object_detection", reason="requires kolena[metrics] extra")
ObjectDetectionEvaluator = object_detection.ObjectDetectionEvaluator
TestSample = object_detection.TestSample
TestCase = object_detection.TestCase
ThresholdConfiguration = object_detection.ThresholdConfiguration
TestCaseMetricsSingleClass = object_detection.TestCaseMetricsSingleClass
TestSampleMetricsSingleClass = object_detection.TestSampleMetricsSingleClass


EXPECTED_COMPUTE_TEST_SAMPLE_METRICS: List[Tuple[TestSample, TestSampleMetricsSingleClass]] = [
    (
        TestSample(locator=fake_locator(112, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a", 1.0),
                ScoredLabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a", 0.9),
                ScoredLabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a", 0.8),
                ScoredLabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a", 0.7),
            ],
            FP=[],
            FN=[],
            count_TP=4,
            count_FP=0,
            count_FN=0,
            has_TP=True,
            has_FP=False,
            has_FN=False,
            ignored=False,
            max_confidence_above_t=1.0,
            min_confidence_above_t=0.7,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(113, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.1, 1.0), (2.1, 2.0), "a", 0.9),
                ScoredLabeledBoundingBox((3.3, 3.0), (4.3, 4.0), "a", 0.8),
            ],
            FP=[
                ScoredLabeledBoundingBox((7.7, 7.0), (8.7, 8.0), "a", 1.0),
                ScoredLabeledBoundingBox((5.5, 5.0), (6.5, 6.0), "a", 0.7),
            ],
            FN=[LabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a"), LabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a")],
            count_TP=2,
            count_FP=2,
            count_FN=2,
            has_TP=True,
            has_FP=True,
            has_FN=True,
            ignored=False,
            max_confidence_above_t=1.0,
            min_confidence_above_t=0.7,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(114, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a", 0.6),
                ScoredLabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a", 0.5),
                ScoredLabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a", 0.4),
                ScoredLabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a", 0.1),
            ],
            FP=[],
            FN=[],
            count_TP=4,
            count_FP=0,
            count_FN=0,
            has_TP=True,
            has_FP=False,
            has_FN=False,
            ignored=False,
            max_confidence_above_t=0.6,
            min_confidence_above_t=0.1,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(115, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a", 1.0),
                ScoredLabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a", 0.9),
                ScoredLabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a", 0.9),
                ScoredLabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a", 0.8),
            ],
            FP=[
                ScoredLabeledBoundingBox((0.0, 0.0), (1.0, 1.0), "a", 1.0),
                ScoredLabeledBoundingBox((0.0, 0.0), (1.0, 1.0), "a", 1.0),
                ScoredLabeledBoundingBox((0.0, 0.0), (1.0, 1.0), "a", 0.9),
                ScoredLabeledBoundingBox((0.0, 0.0), (1.0, 1.0), "a", 0.8),
            ],
            FN=[],
            count_TP=4,
            count_FP=4,
            count_FN=0,
            has_TP=True,
            has_FP=True,
            has_FN=False,
            ignored=False,
            max_confidence_above_t=1.0,
            min_confidence_above_t=0.8,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(116, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a", 1.0),
                ScoredLabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a", 0.4),
            ],
            FP=[],
            FN=[LabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a"), LabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a")],
            count_TP=2,
            count_FP=0,
            count_FN=2,
            has_TP=True,
            has_FP=False,
            has_FN=True,
            ignored=False,
            max_confidence_above_t=1.0,
            min_confidence_above_t=0.4,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(117, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[ScoredLabeledBoundingBox((5.0, 5.0), (6.0, 6.0), "a", 0.9)],
            FP=[ScoredLabeledBoundingBox((7.0, 7.0), (9.0, 9.0), "a", 0.9)],
            FN=[
                LabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a"),
                LabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a"),
                LabeledBoundingBox((7.0, 7.0), (8.0, 8.0), "a"),
            ],
            count_TP=1,
            count_FP=1,
            count_FN=3,
            has_TP=True,
            has_FP=True,
            has_FN=True,
            ignored=False,
            max_confidence_above_t=0.9,
            min_confidence_above_t=0.9,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(118, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[
                ScoredLabeledBoundingBox((1.0, 1.0), (2.0, 2.0), "a", 0.9),
                ScoredLabeledBoundingBox((3.0, 3.0), (4.0, 4.0), "a", 0.8),
            ],
            FP=[],
            FN=[],
            count_TP=2,
            count_FP=0,
            count_FN=0,
            has_TP=True,
            has_FP=False,
            has_FN=False,
            ignored=False,
            max_confidence_above_t=0.9,
            min_confidence_above_t=0.8,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(119, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[],
            FP=[],
            FN=[],
            count_TP=0,
            count_FP=0,
            count_FN=0,
            has_TP=False,
            has_FP=False,
            has_FN=False,
            ignored=True,
            max_confidence_above_t=None,
            min_confidence_above_t=None,
            thresholds=0.1,
        ),
    ),
    (
        TestSample(locator=fake_locator(120, "OD"), metadata={}),
        TestSampleMetricsSingleClass(
            TP=[],
            FP=[],
            FN=[],
            count_TP=0,
            count_FP=0,
            count_FN=0,
            has_TP=False,
            has_FP=False,
            has_FN=False,
            ignored=True,
            max_confidence_above_t=None,
            min_confidence_above_t=None,
            thresholds=0.1,
        ),
    ),
]


EXPECTED_COMPUTE_TEST_CASE_METRICS = TestCaseMetricsSingleClass(
    Objects=26,
    Inferences=26,
    TP=19,
    FN=7,
    FP=7,
    nIgnored=0,
    Precision=19 / 26,
    Recall=19 / 26,
    F1=19 / 26,
    AP=361 / 676,
)


EXPECTED_F1_CURVE_PLOT = CurvePlot(
    title="F1-Score vs. Confidence Threshold",
    x_label="Confidence Threshold",
    y_label="F1-Score",
    curves=[
        Curve(
            x=[0.1, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            y=[19 / 26, 12 / 17, 32 / 49, 5 / 8, 28 / 47, 26 / 45, 9 / 20, 3 / 16],
            label=None,
            extra={
                "Precision": [19 / 26, 18 / 25, 16 / 23, 15 / 22, 2 / 3, 13 / 19, 9 / 14, 0.5],
                "Recall": [19 / 26, 9 / 13, 8 / 13, 15 / 26, 7 / 13, 0.5, 9 / 26, 3 / 26],
            },
        ),
    ],
    x_config=None,
    y_config=None,
)


@pytest.mark.metrics
def test__object_detection__multiclass_evaluator__f1_optimal() -> None:
    TEST_CASE_NAME = "single class OD test fixed"
    TEST_CASE = TestCase(with_test_prefix(TEST_CASE_NAME + " case"))

    config = ThresholdConfiguration(
        iou_threshold=0.5,
        min_confidence_score=0.1,
    )

    eval = ObjectDetectionEvaluator(configurations=[config])

    test_sample_metrics = eval.compute_test_sample_metrics(
        test_case=TEST_CASE,
        inferences=TEST_DATA,
        configuration=config,
    )

    assert config.display_name() in eval.evaluator.threshold_cache
    assert eval.evaluator.threshold_cache[config.display_name()] == 0.1
    assert len(eval.evaluator.matchings_by_test_case) != 0
    assert len(eval.evaluator.matchings_by_test_case[config.display_name()]) != 0
    num_of_ignored = sum([1 for _, _, inf in TEST_DATA if inf.ignored])
    assert (
        len(eval.evaluator.matchings_by_test_case[config.display_name()][TEST_CASE.name])
        == len(TEST_DATA) - num_of_ignored
    )
    assert test_sample_metrics == EXPECTED_COMPUTE_TEST_SAMPLE_METRICS

    test_case_metrics = eval.compute_test_case_metrics(
        test_case=TEST_CASE,
        inferences=TEST_DATA,
        metrics=[pair[1] for pair in EXPECTED_COMPUTE_TEST_SAMPLE_METRICS],
        configuration=config,
    )

    assert TEST_CASE.name in eval.evaluator.locators_by_test_case
    assert len(eval.evaluator.locators_by_test_case[TEST_CASE.name]) == len(TEST_DATA)
    assert_test_case_metrics_equals_expected(test_case_metrics, EXPECTED_COMPUTE_TEST_CASE_METRICS)

    # test case plots only use the cached values
    plots = eval.compute_test_case_plots(
        test_case=TEST_CASE,
        inferences=[],
        metrics=[],
        configuration=config,
    )
    assert_curve_plot_equal(plots[1], EXPECTED_F1_CURVE_PLOT)

    # test suite behaviour is consistent with fixed evaluator
