import pang


def test_noteserver_00():
    server = pang.NoteServer()
    index = pang._get_next_available_server_index([server], 0.0)
    assert index == 0


def test_noteserver_01():
    server0 = pang.NoteServer()
    server1 = pang.NoteServer()
    server0._offset_instance = 2.0
    server1._offset_instance = 1.0
    index = pang._get_next_available_server_index([server0, server1], 0.0)
    assert index == 1


def test_noteserver_02():
    server = pang.NoteServer()
    server.serve(1.0, pang.SoundPoint(99999, 0.5, 0))
    assert server.durations == [1.0, 0.5]
    assert server.pitches == [None, 0]
    assert server.offset_instance == 1.5
