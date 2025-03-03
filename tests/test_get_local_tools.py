from src.utils.get_local_tools import get_local_tools

def test_get_local_tools():
    tools = get_local_tools()
    assert tools == ['tool_2.py', 'youtubeShortExtractor.py', 'tool_1.py', 'tool_3.py']
