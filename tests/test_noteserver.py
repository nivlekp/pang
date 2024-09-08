import pang


def test_noteserver_serve():
    server = pang.NoteServer()
    server.serve(1.0, pang.SoundPoint(99999, 0.5, 0))
    assert server.durations == [1.0, 0.5]
    assert server.pitches == [None, 0]
    assert server.offset_instance == 1.5
