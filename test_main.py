import main


def test_parse_allocations():
	allocations = main._parse_allocations()
	assert 'VTSAX' in allocations
