import csv
import numpy as np

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

    def update_tot_distance(self):
        try:
            dx = np.array(self.curr_position) - np.array(self.last_position)
            dx = np.linalg.norm(dx)
            self.tot_distance += dx
        except:
            pass