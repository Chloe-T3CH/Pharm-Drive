from app.utils import diff_texts

def test_diff_texts():
    old = "line1\nline2"
    new = "line1\nline3"
    diff = diff_texts(old, new)
    assert "-line2" in diff
    assert "+line3" in diff
