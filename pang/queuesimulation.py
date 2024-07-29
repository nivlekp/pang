import queue

from .noteserver import NoteServer, _get_closest_server
from .sequences import Sequence


def simulate_queue(sequence: Sequence, servers: tuple[NoteServer, ...]):
    """
    Simulate the queue based on the queue type.
    """
    # TODO: model rest_threshold
    assert sequence.instances is not None and len(sequence.instances) > 0
    curr_time = 0.0
    q: queue.Queue = queue.Queue()
    arrival_index = 0
    while arrival_index < len(sequence.instances) or not q.empty():
        server_index, closest_offset_instance = _get_closest_server(servers)
        if q.empty():
            if closest_offset_instance > sequence.instances[arrival_index]:
                # previous note has not finished yet, so we should queue
                # the newly arrived note
                q.put(arrival_index)
                curr_time = sequence.instances[arrival_index]
                arrival_index = arrival_index + 1
            else:
                curr_time = sequence.instances[arrival_index]
                servers[server_index].serve(
                    curr_time,
                    sound_point=sequence._sound_points[arrival_index],
                )
                arrival_index = arrival_index + 1
        else:  # there's already a client in the queue
            # queue the current note
            if (
                arrival_index < len(sequence.instances)
                and closest_offset_instance > sequence.instances[arrival_index]
            ):
                q.put(arrival_index)
                curr_time = sequence.instances[arrival_index]
                arrival_index = arrival_index + 1
            else:
                index = q.get()
                curr_time = closest_offset_instance
                servers[server_index].serve(
                    curr_time,
                    sound_point=sequence._sound_points[index],
                )
