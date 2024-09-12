from .noteserver import NoteServer
from .sequences import Sequence
from .soundpointsgenerators import SoundPoint


def simulate_queue(
    sequence: Sequence, servers: tuple[NoteServer, ...]
) -> tuple[NoteServer, ...]:
    queue: list[SoundPoint] = []
    for index, sound_point in enumerate(sequence._sound_points):
        queue.append(sound_point)
        current_time = sound_point.instance
        _try_serving(servers, queue, current_time)
        if index == len(sequence._sound_points) - 1:
            break
        while queue and current_time < sequence._sound_points[index + 1].instance:
            if not _try_serving(servers, queue, current_time):
                current_time = _when_another_server_is_done(servers, current_time)
    while queue:
        if not _try_serving(servers, queue, current_time):
            current_time = _when_another_server_is_done(servers, current_time)
    return servers


def _try_serving(servers, queue, current_time) -> bool:
    for index, sound_point in enumerate(queue):
        available_servers = _get_all_available_servers(servers, current_time)
        servable_servers = _get_all_servable_servers(available_servers, sound_point)
        if servable_servers:
            servable_servers[0].serve(current_time, queue.pop(index))
            return True
    return False


def _get_all_available_servers(
    servers: tuple[NoteServer, ...], current_time: float
) -> tuple[NoteServer, ...]:
    return tuple(
        [server for server in servers if server.offset_instance <= current_time]
    )


def _get_all_servable_servers(
    available_servers: tuple[NoteServer, ...], sound_point: SoundPoint
) -> tuple[NoteServer, ...]:
    return tuple(
        [server for server in available_servers if server.can_serve(sound_point)]
    )


def _when_another_server_is_done(
    servers: tuple[NoteServer, ...], current_time: float
) -> float:
    not_yet_available_servers = tuple(
        [server for server in servers if server.offset_instance > current_time]
    )
    next_offset_instance, _ = min(
        (server.offset_instance, index)
        for index, server in enumerate(not_yet_available_servers)
    )
    return next_offset_instance
