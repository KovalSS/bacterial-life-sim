class FearMixin:
    def get_fear_vector(self, world, enemy_grids):
        total_run_dx = 0
        total_run_dy = 0

        enemies = []
        for grid in enemy_grids:
            enemies.extend(world.get_nearby_from_grid(self, grid))

        for enemy in enemies:
            if hasattr(enemy, 'is_dead') and enemy.is_dead():
                continue

            dx = self.position_X - enemy.position_X
            dy = self.position_Y - enemy.position_Y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if 0 < dist < self.dna["fear_radius"]:
                strength = self.dna["fear"] / dist

                total_run_dx += dx * strength
                total_run_dy += dy * strength

        return total_run_dx, total_run_dy