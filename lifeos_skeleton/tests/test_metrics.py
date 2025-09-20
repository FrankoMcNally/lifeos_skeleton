from lifeos import metrics

def test_metrics_import():
    # Just check we can import and use something simple
    assert hasattr(metrics, "__file__") or metrics is not None
