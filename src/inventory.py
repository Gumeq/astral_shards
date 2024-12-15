class Inventory:
    def __init__(self):
        self.equipped = {
            "weapon": None,
            "armor": None
        }
        self.consumables = [None] * 5  # 5 consumable slots

    def equip(self, slot, item):
        if slot in self.equipped:
            self.equipped[slot] = item

    def has_consumable_space(self):
        """Check if there's at least one empty slot for a consumable."""
        return any(slot is None for slot in self.consumables)

    def add_consumable(self, consumable):
        """Add a consumable to the first available slot."""
        for i in range(len(self.consumables)):
            if self.consumables[i] is None:
                self.consumables[i] = consumable
                return
        print("No available slot for consumable.")

    def use_consumable(self, slot, player):
        if 0 <= slot < len(self.consumables):
            consumable = self.consumables[slot]
            if consumable and not consumable.is_active:
                consumable.apply_effect(player)

    def update_consumables(self):
        for i, consumable in enumerate(self.consumables):
            if consumable:
                consumable.update()
                if consumable.is_used and consumable.get_time_remaining() == 0:
                    self.consumables[i] = None
