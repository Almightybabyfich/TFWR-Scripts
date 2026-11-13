# Max-Speed + Max-Reward (20,736 Bones) 12x12 Dinosaur Solver
# Includes a pre-run 12x12 Sunflower Power Engine for 2x Drone Speed

GRID = 12
TOTAL_TILES = GRID * GRID

# Precompute a static Hamiltonian cycle order (0 to 143) for every (x, y) tile
HAMILTONIAN_INDEX = {}

def build_hamiltonian_map():
	idx = 0
	x, y = 0, 0
	for step in range(TOTAL_TILES):
		HAMILTONIAN_INDEX[(x, y)] = idx
		idx += 1
		if x == 0 and y == 0:
			y += 1
		elif y == 0:
			x -= 1
		elif x % 2 == 0:
			if y < GRID - 1:
				y += 1
			else:
				x += 1
		else:
			if y > 1:
				y -= 1
			else:
				if x < GRID - 1:
					x += 1
				else:
					y -= 1

def move_to_origin():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def move_to(tx, ty):
	# Uses world-wrapping shortest path to reach (tx, ty) quickly
	dx = (tx - get_pos_x()) % GRID
	if dx > GRID // 2:
		for _ in range(GRID - dx):
			move(West)
	else:
		for _ in range(dx):
			move(East)
			
	dy = (ty - get_pos_y()) % GRID
	if dy > GRID // 2:
		for _ in range(GRID - dy):
			move(South)
	else:
		for _ in range(dy):
			move(North)

def farm_sunflower_power():
	# Plant a full 12x12 field of sunflowers and harvest in max-petal order for 2x speed
	clear()
	move_to_origin()
	
	# Bucket coordinates by petal count (15 down to 7)
	petal_buckets = {}
	for p in range(7, 16):
		petal_buckets[p] = []
	
	# Pass 1: Till, plant, water, and record petal counts
	for x in range(GRID):
		for y in range(GRID):
			move_to(x, y)
			if get_ground_type() != Grounds.Soil:
				till()
			if get_water() < 0.75:
				use_item(Items.Water)
			plant(Entities.Sunflower)
			petals = measure()
			if petals != None and petals in petal_buckets:
				petal_buckets[petals].append((x, y))
				
	# Pass 2: Harvest strictly from highest petals (15) to lowest (7)
	# Always picking the largest sunflower keeps the 5x Power bonus active
	for p in range(15, 6, -1):
		for pos in petal_buckets[p]:
			move_to(pos[0], pos[1])
			while not can_harvest():
				if get_water() < 0.5:
					use_item(Items.Water)
			harvest()

def is_safe_step(nx, ny, target_idx, head_idx, tail_idx, tail_len):
	if nx < 0 or nx >= GRID or ny < 0 or ny >= GRID:
		return False
	
	next_idx = HAMILTONIAN_INDEX[(nx, ny)]
	dist_to_next = (next_idx - head_idx) % TOTAL_TILES
	if dist_to_next == 0:
		return False
	
	if tail_len == 0:
		return True
	
	dist_to_tail = (tail_idx - head_idx) % TOTAL_TILES
	if dist_to_tail == 0:
		dist_to_tail = TOTAL_TILES
		
	if dist_to_next >= dist_to_tail - 1:
		return False
		
	dist_to_apple = (target_idx - head_idx) % TOTAL_TILES
	if dist_to_apple > 0 and dist_to_next > dist_to_apple:
		return False
		
	return True

def run_fast_dinosaur():
	clear()
	move_to_origin()
	change_hat(Hats.Dinosaur_Hat)
	
	body = [(0, 0)]
	apple = measure()
	
	directions = [
		(North, 0, 1),
		(South, 0, -1),
		(East, 1, 0),
		(West, -1, 0)
	]
	
	while len(body) < TOTAL_TILES:
		hx, hy = get_pos_x(), get_pos_y()
		head_idx = HAMILTONIAN_INDEX[(hx, hy)]
		tail_idx = HAMILTONIAN_INDEX[body[0]]
		target_idx = head_idx
		if apple != None:
			target_idx = HAMILTONIAN_INDEX[apple]
			
		best_dir = None
		best_dist = 999999
		
		for d, dx, dy in directions:
			nx, ny = hx + dx, hy + dy
			if is_safe_step(nx, ny, target_idx, head_idx, tail_idx, len(body) - 1):
				if apple != None:
					manhattan = abs(nx - apple[0]) + abs(ny - apple[1])
				else:
					manhattan = 0
				if manhattan < best_dist:
					best_dist = manhattan
					best_dir = d
					
		if best_dir == None:
			next_cycle_idx = (head_idx + 1) % TOTAL_TILES
			for d, dx, dy in directions:
				nx, ny = hx + dx, hy + dy
				if 0 <= nx < GRID and 0 <= ny < GRID:
					if HAMILTONIAN_INDEX[(nx, ny)] == next_cycle_idx:
						best_dir = d
						break
						
		if best_dir == None or not move(best_dir):
			break
			
		new_pos = (get_pos_x(), get_pos_y())
		body.append(new_pos)
		
		if apple == None or new_pos != apple:
			body.pop(0)
		else:
			apple = measure()
			
	# Cash out all 144 tiles for 20,736 bones
	change_hat(Hats.Straw_Hat)

# Initialize cycle lookup table once
build_hamiltonian_map()

# Main Loop
while True:
	# Stock up on Power before running if we have enough carrots and low power
	if num_items(Items.Power) < 500 and num_items(Items.Carrot) >= 200:
		farm_sunflower_power()
		
	if num_items(Items.Cactus) >= 200:
		run_fast_dinosaur()
	else:
		do_a_flip()
		
