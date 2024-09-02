from .noteserver import NoteServer
from .sequences import Sequence


def _get_next_available_server(servers):
    offset_instance, idx = min(
        (server.offset_instance, idx) for (idx, server) in enumerate(servers)
    )
    return idx, offset_instance


def simulate_queue(sequence: Sequence, servers: tuple[NoteServer, ...]):
    """
    Simulate the queue based on the queue type.
    """
    # TODO: model rest_threshold
    assert sequence.instances is not None and len(sequence.instances) > 0
    curr_time = 0.0
    queue: list[int] = []
    arrival_index = 0
    while arrival_index < len(sequence.instances) or queue:
        server_index, closest_offset_instance = _get_next_available_server(servers)
        if not queue:
            if closest_offset_instance > sequence.instances[arrival_index]:
                # previous note has not finished yet, so we should queue
                # the newly arrived note
                queue.append(arrival_index)
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
                queue.append(arrival_index)
                curr_time = sequence.instances[arrival_index]
                arrival_index = arrival_index + 1
            else:
                index = queue.pop(0)
                curr_time = closest_offset_instance
                servers[server_index].serve(
                    curr_time,
                    sound_point=sequence._sound_points[index],
                )
    return servers
