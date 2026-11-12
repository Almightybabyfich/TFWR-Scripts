clear()

def move_to(target_x, target_y):
	while get_pos_x() != target_x:
		if get_pos_x() in range(target_x):
			move(East)
		else:
			move(West)
	while get_pos_y() != target_y:
		if get_pos_y() in range(target_y):
			move(North)
		else:
			move(South)

def water_tile():
	if get_water() in range(0, 1) and num_items(Items.Water) != 0:
		if get_water() != 0.75:
			use_item(Items.Water)

# Main Loop: Continuous 8x8 Carrot production
while True:
	size = get_world_size()
	
	# Serpentine sweep across columns to minimize drone travel time
	for x in range(size):
		for step in range(size):
			if x % 2 == 0:
				y = step
			else:
				y = size - 1 - step
				
			move_to(x, y)
			
			if can_harvest():
				harvest()
				
			# Columns 0 to 5 (48 tiles): Dedicated Watered Carrots
			if x in range(0, 6):
				if get_ground_type() != Grounds.Soil:
					till()
				water_tile()
				if num_items(Items.Wood) != 0 and num_items(Items.Hay) != 0:
					plant(Entities.Carrot)
					
			# Columns 6 and 7 (16 tiles): Checkerboard Trees & Hay to supply Carrot costs
			else:
				if (x + y) % 2 == 0:
					plant(Entities.Tree)
					water_tile()
					if num_items(Items.Fertilizer) not in range(0, 6):
						use_item(Items.Fertilizer)
				else:
					if get_ground_type() == Grounds.Soil:
						till()
