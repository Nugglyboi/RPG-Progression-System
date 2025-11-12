import structs
import csvparser as parser

_story_beats = parser.read_csv("data/StoryBeats.csv", structs.World)


def create_world() -> structs.World:
    return _story_beats[0]


def max_zone_level() -> int:
    """Return the highest zone level defined in story beats.

    Mirrors the player.max_level() pattern by exposing the maximum
    zone level available from the loaded story beats data.
    """
    return _story_beats[-1].ZoneLevel

def progress_story(turn: int, world: structs.World) -> structs.World:
    for i in range(len(_story_beats) - 1):
        if _story_beats[i].BeatNum == world.BeatNum:
            if turn >= _story_beats[i + 1].BeatStartStep:
                return _story_beats[i + 1]  # progress stages
    return world  # stay on current stage
