from .models import Location
from .models import Npc
from .models import Character


import time


def GetNearbyLocations(location_id):
    nearby_locations = Location.objects.raw(f"SELECT * \
                                            FROM rpg_location \
                                            WHERE neighbour_locations @> '{location_id}';")
        
    return nearby_locations


def GetLocationNpc(location_id):
    npcs = Npc.objects.raw(f"select * from rpg_character \
                          inner join rpg_npc on rpg_npc.character_id_id = rpg_character.id \
                          where rpg_character.current_location_id={location_id}")

    location_npc = [npc for npc in npcs if npc.enemy]
    location_enemies = [npc for npc in npcs if not npc.enemy]

    return location_enemies, location_npc
    
