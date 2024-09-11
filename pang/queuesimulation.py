from .noteserver import NoteServer
from .sequences import Sequence
from .soundpointsgenerators import SoundPoint


def _get_next_available_server_index(servers, next_arrival_time: float):
    _, index = min(
        (max(server.offset_instance, next_arrival_time), idx)
        for (idx, server) in enumerate(servers)
    )
    return index


def _get_all_available_servers_by_next_arrival(
    servers: tuple[NoteServer, ...], next_arrival_time: float
):
    return tuple(
        [server for server in servers if server.offset_instance <= next_arrival_time]
    )


def _get_all_available_servers(servers: tuple[NoteServer, ...], current_time: float):
    return tuple(
        [server for server in servers if server.offset_instance <= current_time]
    )


def _get_all_servable_servers(
    available_servers: tuple[NoteServer, ...], sound_point: SoundPoint
):
    return tuple(
        [server for server in available_servers if server.can_serve(sound_point)]
    )


def when_another_server_is_done(servers, current_time):
    not_yet_available_servers = tuple(
        [server for server in servers if server.offset_instance > current_time]
    )
    next_offset_instance, _ = min(
        (server.offset_instance, index)
        for index, server in enumerate(not_yet_available_servers)
    )
    return next_offset_instance


def simulate_queue(sequence: Sequence, servers: tuple[NoteServer, ...]):
    queue: list[SoundPoint] = []
    for index, sound_point in enumerate(sequence._sound_points):
        queue.append(sound_point)
        current_time = sound_point.instance
        _try_serving(servers, queue, current_time)
        if index == len(sequence._sound_points) - 1:
            break
        while queue and current_time < sequence._sound_points[index + 1].instance:
            if not _try_serving(servers, queue, current_time):
                current_time = when_another_server_is_done(servers, current_time)
    while queue:
        if not _try_serving(servers, queue, current_time):
            current_time = when_another_server_is_done(servers, current_time)
    return servers


def _try_serving(servers, queue, current_time) -> bool:
    for index, sound_point in enumerate(queue):
        available_servers = _get_all_available_servers(servers, current_time)
        servable_servers = _get_all_servable_servers(available_servers, sound_point)
        if servable_servers:
            servable_servers[0].serve(current_time, queue.pop(index))
            return True
    return False


def simulate_queue_backup(sequence: Sequence, servers: tuple[NoteServer, ...]):
    """
    Simulate the queue based on the queue type.
    """
    # TODO: model rest_threshold
    assert sequence.instances is not None and len(sequence.instances) > 0
    queue: list[int] = []
    arrival_index = 0
    when_next_server_is_available = 0.0
    while arrival_index < len(sequence.instances) or queue:
        server_index = _get_next_available_server_index(
            servers,
            (
                when_next_server_is_available
                if arrival_index == len(sequence.instances)
                else sequence.instances[arrival_index]
            ),
        )
        closest_offset_instance = servers[server_index].offset_instance
        if arrival_index < len(sequence.instances) and (
            closest_offset_instance > sequence.instances[arrival_index]
            or not servers[server_index].can_serve(
                sequence._sound_points[arrival_index]
            )
        ):
            # previous note has not finished yet, so we should queue
            # the newly arrived note
            queue.append(arrival_index)
            arrival_index = arrival_index + 1
        elif not queue:
            assert servers[server_index].can_serve(
                sequence._sound_points[arrival_index]
            )
            servers[server_index].serve(
                sequence.instances[arrival_index],
                sound_point=sequence._sound_points[arrival_index],
            )
            arrival_index = arrival_index + 1
        else:  # there's already a client in the queue
            sound_point_to_serve = sequence._sound_points[queue.pop(0)]
            servers[server_index].serve(closest_offset_instance, sound_point_to_serve)
            when_next_server_is_available = sum(servers[server_index].durations)
    return servers
