import csv
import math
import os

class Player:

    id:int = None
    coords_path:str = None
    coords_buffer:list = None
    last_position:tuple = None
    curr_position:tuple = None
    tot_distance:float = None
    

    def __init__(self, id) -> None:
        self.id = id
        self.coords_path = f'data/coords_player_{id}.csv'
        self.coords_buffer = []
        self.tot_distance = 0
        if not os.path.exists('data'):
            os.mkdir('data')

        with open(self.coords_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["x_pos", "y_pos", "num_frame"])

        f.close()

    def update_coords_buffer(self, coords:tuple[int]) -> None:
        self.last_position = self.curr_position
        self.curr_position = coords    
        self.coords_buffer.append(coords)
    
    def update_coords_file(self) -> None:
        with open(self.coords_path, 'a', newline='') as f:
            writer = csv.writer(f)
            for coords in self.coords_buffer:
                writer.writerow(coords)
        f.close()

    def update_tot_distance(self, field_width, field_height, 
                            screen_width, screen_height) -> None:
        
        try:
            dx_px = self.curr_position[0] - self.last_position[0]
            dy_px = self.last_position[1] - self.last_position[1]

            dx_r = dx_px * (field_width/screen_width)
            dy_r = dy_px * (field_height/screen_height)
            
            self.tot_distance += math.sqrt(dx_r**2 + dy_r**2)
            #print(self.tot_distance)
        except:
            pass
    
    def instant_speed(self, field_width, field_height, 
                            screen_width, screen_height, frame_time) -> None:
        try:
            dx_px = self.curr_position[0] - self.last_position[0]
            dy_px = self.last_position[1] - self.last_position[1]

            dx_r = dx_px * (field_width/screen_width)
            dy_r = dy_px * (field_height/screen_height)
            distance = math.sqrt(dx_r**2 + dy_r**2) 

            insta_speed = 3.6 * distance/frame_time
            print(insta_speed, 'km/h')
        except:
            pass