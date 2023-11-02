from django.db import connection
from .models import Item
from .utils import serialize_one
from .models import Character
from .models import Equipment
from .contants import *
import json


def get_inventory(inventory):
    inventory_json = json.loads(inventory)
    if inventory_json:
        item_ids = []
        for item in inventory_json:
            item_ids.append(inventory_json[item]['item_id'])

        items = Item.objects.raw(f"SELECT * from rpg_item \
                                 WHERE rpg_item.id = ANY(ARRAY{item_ids}) \
                                 ORDER BY array_position(ARRAY{item_ids}, rpg_item.id)")
        
        i = 0
        for item in inventory_json:
            inventory_json[item]['item'] = serialize_one(items[i])['fields']
            i += 1

    print(inventory_json)
            
    return inventory_json


def add_items(new_item_ids, quantities, character_id, inventory_json):
    print(f"add items: {new_item_ids}")
    items = Item.objects.raw(f"SELECT * from rpg_item \
                                     WHERE rpg_item.id = ANY(ARRAY{new_item_ids}) \
                                     ORDER BY array_position(ARRAY{new_item_ids}, rpg_item.id)")
    i = 0
    for new_item in items:
        print(serialize_one(new_item)['fields'])
        item_id = str(new_item_ids[i])
        if item_id in inventory_json:
            inventory_json[item_id]['quantity'] += quantities[i]
        else:
            print("add new item")
            inventory_json[item_id] = {'quantity': quantities[i],
                                       'item': serialize_one(new_item)['fields']}
        i += 1

    Character.objects.filter(id=character_id).update(inventory=json.dumps(inventory_json))

    return inventory_json


def use_item(item_id, quantity, character_id, inventory_json):
    print(f"use items: {item_id}")
    result_quantity = quantity
    if inventory_json[str(item_id)]['quantity'] > quantity:
        inventory_json[str(item_id)]['quantity'] -= quantity
        Character.objects.filter(id=character_id).update(inventory=json.dumps(inventory_json))
    if inventory_json[str(item_id)]['quantity'] <= quantity:
        result_quantity = inventory_json[str(item_id)]['quantity']
        remove_item(item_id, character_id, inventory_json)

    return inventory_json, result_quantity


def remove_item(item_id, character_id, inventory_json):
    print(f"remove items: {item_id}")
    inventory_json.pop(str(item_id))
    Character.objects.filter(id=character_id).update(inventory=json.dumps(inventory_json))
    return  inventory_json
    #update rpg_character set inventory = jsonb_set(inventory, '{items}', '[{"item_id": 3,"quatity": 1},{"item_id": 2,"quatity": 1},{"item_id": 1,"quatity": 1}]') where rpg_character.id = 3


def add_stats(stats, character_stats):
    print(f"add stats: {stats.keys()}")
    for stat in stats.keys():
        match stat:
            case StatType.DAMAGE:
                character_stats[StatType.DAMAGE] += stats[StatType.DAMAGE]

            case StatType.DEFENSE:
                character_stats[StatType.DEFENSE] += stats[stat][StatType.DEFENSE]
            case StatType.MAX_HEALTH:
                character_stats[StatType.MAX_HEALTH] += stats[stat][StatType.MAX_HEALTH]
            case StatType.CURRENT_HEALTH:
                character_stats[StatType.CURRENT_HEALTH] += stats[stat][StatType.CURRENT_HEALTH]
            case StatType.STRENGTH:
                character_stats[StatType.STRENGTH] += stats[stat][StatType.STRENGTH]
            case StatType.AGILITY:
                character_stats[StatType.AGILITY] += stats[stat][StatType.AGILITY]
            case StatType.INTELLIGENCE:
                character_stats[StatType.INTELLIGENCE] += stats[stat][StatType.INTELLIGENCE]
                
    print(f"result_stats: {character_stats}")
                
    return character_stats
            

def remove_stats(stats, character_stats):
    for stat in stats:
        print(stats[stat])
        match stats.keys():
            case StatType.DAMAGE:
                character_stats[StatType.DAMAGE] -= stats[StatType.DAMAGE]
            case StatType.DEFENSE:
                character_stats[StatType.DEFENSE] -= stats[stat][StatType.DEFENSE]
            case StatType.MAX_HEALTH:
                character_stats[StatType.MAX_HEALTH] -= stats[stat][StatType.MAX_HEALTH]
            case StatType.CURRENT_HEALTH:
                character_stats[StatType.CURRENT_HEALTH] -= stats[stat][StatType.CURRENT_HEALTH]
            case StatType.STRENGTH:
                character_stats[StatType.STRENGTH] -= stats[stat][StatType.STRENGTH]
            case StatType.AGILITY:
                character_stats[StatType.AGILITY] -= stats[stat][StatType.AGILITY]
            case StatType.INTELLIGENCE:
                character_stats[StatType.INTELLIGENCE] -= stats[stat][StatType.INTELLIGENCE  ]
                
    return character_stats
          

def unequip_item(item_id, quantity, character, inventory, db_request=True):
    cursor = connection.cursor()
    item = Item.objects.get(id=item_id)
    character_stats = character.stats
    if db_request:
        cursor.execute(f"update rpg_equipment set {item.type}_id = 0 \
                         where rpg_equipment.id={character.equipment_id}")
    if item.type != ItemType.CONSUMABLES:
        character_stats = remove_stats(item.stats, character_stats)
        if db_request:
            cursor.execute(f"update rpg_character set stats = '{json.dumps(character_stats)}' \
                             where rpg_character.id = {character.id}")
            
    inventory = add_items([item_id], [quantity], character.id, inventory)
    if db_request:
        cursor.execute(f"update rpg_character set inventory = '{json.dumps(inventory)}' \
                                where rpg_character.id = {character.id}")
    
    return inventory, character_stats
    

def equip_item(item_id, quantity, character, inventory):
    cursor = connection.cursor()
    item = Item.objects.get(id=item_id)
    current_item = Equipment.objects.raw(f"select rpg_equipment.id, {item.type}_id from rpg_equipment \
                                           where rpg_equipment.id={character.equipment_id}")
    
    current_item_id = getattr(current_item[0], f"{item.type}_id")
    print(f"Current item:{current_item_id}")
    #current_item_id = current_item[0]['id']
    
    # REDO equipment.consumable to separate fields from 1 to 4
    #if item.type == ItemType.CONSUMABLES:
    #    consumables = character.equipment.consumables
    #    if len(consumables) == 4:
    #        for first in consumables:
    #            
    #else:
    #current_item_id = Character.equipment.field[item.type]
    quantity = 1
    character_stats = 0
    if current_item_id != 0:
        inventory, character_stats = unequip_item(current_item_id, quantity, character, inventory, False)
    
    inventory_json, result_quantity = use_item(item_id, quantity, character.id, inventory)
    cursor.execute(f"update rpg_equipment set {item.type}_id = {item.id} \
                     where rpg_equipment.id={character.equipment_id}")
    if item.type != ItemType.CONSUMABLES:
        print(f"Not consumable: {item.type}")
        character_stats = add_stats(item.stats, character_stats)
        cursor.execute(f"update rpg_character set stats = '{json.dumps(character_stats)}' \
                                where rpg_character.id = {character.id}")
        
    cursor.execute(f"update rpg_character set inventory = '{json.dumps(inventory_json)}' \
                                where rpg_character.id = {character.id}")

    return inventory_json
    
    