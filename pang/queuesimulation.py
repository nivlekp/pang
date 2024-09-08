from .noteserver import NoteServer
from .sequences import Sequence


def _get_next_available_server_index(servers, next_arrival_time: float | None):
    _, index = min(
        (max(server.offset_instance, next_arrival_time or 0.0), idx)
        for (idx, server) in enumerate(servers)
    )
    return index


def simulate_queue(sequence: Sequence, servers: tuple[NoteServer, ...]):
    """
    Simulate the queue based on the queue type.
    """
    # TODO: model rest_threshold
    assert sequence.instances is not None and len(sequence.instances) > 0
    queue: list[int] = []
    arrival_index = 0
    while arrival_index < len(sequence.instances) or queue:
        server_index = _get_next_available_server_index(
            servers,
            (
                None
                if arrival_index == len(sequence.instances)
                else sequence.instances[arrival_index]
            ),
        )
        closest_offset_instance = servers[server_index].offset_instance
        if (
            arrival_index < len(sequence.instances)
            and closest_offset_instance > sequence.instances[arrival_index]
        ):
            # previous note has not finished yet, so we should queue
            # the newly arrived note
            queue.append(arrival_index)
            arrival_index = arrival_index + 1
        elif not queue:
            servers[server_index].serve(
                sequence.instances[arrival_index],
                sound_point=sequence._sound_points[arrival_index],
            )
            arrival_index = arrival_index + 1
        else:  # there's already a client in the queue
            servers[server_index].serve(
                closest_offset_instance,
                sound_point=sequence._sound_points[queue.pop(0)],
            )
    return servers
