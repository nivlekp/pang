import pang


def test_noteserver_00():
    server = pang.NoteServer()
    index, offset_instance = pang._get_closest_server([server])
    assert index == 0
    assert offset_instance == 0.0


def test_noteserver_01():
    server0 = pang.NoteServer()
    server1 = pang.NoteServer()
    server0._offset_instance = 2.0
    server1._offset_instance = 1.0
    index, offset_instance = pang._get_closest_server([server0, server1])
    assert index == 1
    assert offset_instance == 1.0


def test_noteserver_02():
    server = pang.NoteServer()
    server.serve(curr_time=1.0, duration=0.5, pitch=0)
    assert server.durations == [1.0, 0.5]
    assert server.pitches == [None, 0]
    assert server.offset_instance == 1.5
