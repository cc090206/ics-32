class DrMarioGame:
    
    def __init__(self, rows, columns):
        
        self.rows = rows
        self.columns = columns
        self.field = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.faller = None
        self.faller_landed = False
        
        # Track horizontal connections separately
        self.connections = {}
        
    def get_rows(self):
        return self.rows
        
    def get_columns(self):
        return self.columns
    
    def set_initial_contents(self, contents):
        for i in range(self.rows):
            for j in range(self.columns):
                if j < len(contents[i]):
                    self.field[i][j] = contents[i][j]
                else:
                    self.field[i][j] = ' '
                
        for row in range(self.rows):
            for col in range(self.columns - 1): 
                if self.field[row][col] in 'RBY' and self.field[row][col + 1] == self.field[row][col]:
                    self._add_connection(row, col, row, col + 1)
    
    def create_faller(self, left_color, right_color):
        if self.faller is not None:
            return False
            
        mid = (self.columns // 2) - 1
        
        if self.field[1][mid] != ' ' or self.field[1][mid+1] != ' ':
            return False
            
        self.faller = {
            'orientation': 'horizontal',  
            'landed': False,
            'segments': [
                {'row': 1, 'col': mid, 'color': left_color},
                {'row': 1, 'col': mid+1, 'color': right_color}
            ]
        }
        return True
    
    def create_virus(self, row, column, color):
        if self.field[row][column] != ' ':
            return False
            
        self.field[row][column] = color
        return True
    
    def move_faller_left(self):
        if self.faller is None:
            return False
            
        for segment in self.faller['segments']:
            if segment['col'] - 1 < 0: 
                return False
            
            if segment['col'] - 1 >= 0:
                check_row, check_col = segment['row'], segment['col'] - 1
                if any(s['row'] == check_row and s['col'] == check_col for s in self.faller['segments']):
                    continue
                if self.field[check_row][check_col] != ' ':
                    return False
        
        for segment in self.faller['segments']:
            segment['col'] -= 1
            
        self.check_if_landed()
        return True
    
    def move_faller_right(self):
        if self.faller is None:
            return False
            
        for segment in self.faller['segments']:
            if segment['col'] + 1 >= self.columns: 
                return False
            
            if segment['col'] + 1 < self.columns:
                check_row, check_col = segment['row'], segment['col'] + 1
                if any(s['row'] == check_row and s['col'] == check_col for s in self.faller['segments']):
                    continue
                if self.field[check_row][check_col] != ' ':
                    return False
        
        for segment in self.faller['segments']:
            segment['col'] += 1
            
        self.check_if_landed()
        return True
        
    def check_if_landed(self):
        if self.faller is None:
            return False
            
        for segment in self.faller['segments']:
            if segment['row'] + 1 >= self.rows:
                self.faller['landed'] = True
                return True
                
            check_row, check_col = segment['row'] + 1, segment['col']
            if self.faller['orientation'] == 'vertical' and any(s['row'] == check_row and s['col'] == check_col for s in self.faller['segments']):
                continue
            
            if self.field[check_row][check_col] != ' ':
                self.faller['landed'] = True
                return True
                
        self.faller['landed'] = False
        return False
    
    def rotate_faller_clockwise(self):
        if self.faller is None:
            return False
            
        if self.faller['orientation'] == 'horizontal':
            top_segment = self.faller['segments'][0]  
            bottom_segment = self.faller['segments'][1]
            
            new_top_row = top_segment['row'] - 1
            new_top_col = top_segment['col']
            new_bottom_row = top_segment['row'] 
            new_bottom_col = top_segment['col'] 
            
            if new_top_row < 0:
                return False
                
            if new_top_row >= 0 and self.field[new_top_row][new_top_col] != ' ':
                return False
                
            self.faller['orientation'] = 'vertical'
            self.faller['segments'][0]['row'] = new_top_row
            self.faller['segments'][0]['col'] = new_top_col
            self.faller['segments'][1]['row'] = new_bottom_row
            self.faller['segments'][1]['col'] = new_bottom_col
            
        else:
            top_segment = self.faller['segments'][0]
            bottom_segment = self.faller['segments'][1]
            
            new_left_row = bottom_segment['row']
            new_left_col = bottom_segment['col']
            new_right_row = bottom_segment['row']
            new_right_col = bottom_segment['col'] + 1
            
            if new_right_col >= self.columns or self.field[new_right_row][new_right_col] != ' ':
                if new_left_col - 1 < 0 or self.field[new_left_row][new_left_col - 1] != ' ':
                    return False
                else:
                    new_left_col -= 1
                    new_right_col -= 1
            
            self.faller['orientation'] = 'horizontal'
            self.faller['segments'][0]['row'] = new_left_row
            self.faller['segments'][0]['col'] = new_left_col
            self.faller['segments'][1]['row'] = new_right_row
            self.faller['segments'][1]['col'] = new_right_col
            
        self.check_if_landed()
        return True
    
    def rotate_faller_counterclockwise(self):
        if self.faller is None:
            return False
            
        if self.faller['orientation'] == 'horizontal':
            left_segment = self.faller['segments'][0]
            right_segment = self.faller['segments'][1]
            
            new_top_row = right_segment['row'] - 1
            new_top_col = right_segment['col']
            new_bottom_row = right_segment['row']
            new_bottom_col = right_segment['col']
            
            if new_top_row < 0: 
                return False
                
            if self.field[new_top_row][new_top_col] != ' ':
                return False
                
            self.faller['orientation'] = 'vertical'
            self.faller['segments'][0]['row'] = new_top_row
            self.faller['segments'][0]['col'] = new_top_col
            self.faller['segments'][1]['row'] = new_bottom_row
            self.faller['segments'][1]['col'] = new_bottom_col
            
        else: 
            top_segment = self.faller['segments'][0]
            bottom_segment = self.faller['segments'][1]
            
            new_left_row = bottom_segment['row']
            new_left_col = bottom_segment['col'] - 1
            new_right_row = bottom_segment['row']
            new_right_col = bottom_segment['col']
            
            if new_left_col < 0 or self.field[new_left_row][new_left_col] != ' ':
                if new_right_col + 1 >= self.columns or self.field[new_right_row][new_right_col + 1] != ' ':
                    return False
                else:
                    new_left_col += 1
                    new_right_col += 1
            
            self.faller['orientation'] = 'horizontal'
            self.faller['segments'][0]['row'] = new_left_row
            self.faller['segments'][0]['col'] = new_left_col
            self.faller['segments'][1]['row'] = new_right_row
            self.faller['segments'][1]['col'] = new_right_col
            
        self.check_if_landed()
        return True
    
    def update(self):
        if self.faller is not None:
            if self.faller['landed']:
                self._freeze_faller()
                
                matches = self._find_matches()
                if matches:
                    self._apply_matches(matches)
                    
                self._apply_gravity()
                
                matches = self._find_matches()
                while matches:
                    self._apply_matches(matches)
                    self._apply_gravity()
                    matches = self._find_matches()
                    
                self.faller = None
                
            else:
                for segment in self.faller['segments']:
                    segment['row'] += 1
                
                self.check_if_landed()
                
        else:
            matches = self._find_matches()
            if matches:
                self._apply_matches(matches)
                self._apply_gravity()
                
                matches = self._find_matches()
                while matches:
                    self._apply_matches(matches)
                    self._apply_gravity()
                    matches = self._find_matches()
                    
        return None
    
    def _freeze_faller(self):

        if self.faller is None:
            return
            
        if self.faller['orientation'] == 'horizontal':
            left_row = self.faller['segments'][0]['row']
            left_col = self.faller['segments'][0]['col']
            self.field[left_row][left_col] = self.faller['segments'][0]['color']
            
            right_row = self.faller['segments'][1]['row']
            right_col = self.faller['segments'][1]['col']
            self.field[right_row][right_col] = self.faller['segments'][1]['color']
            
            self._add_connection(left_row, left_col, right_row, right_col)
            
        else: 
            for segment in self.faller['segments']:
                self.field[segment['row']][segment['col']] = segment['color']
    
    def _add_connection(self, row1, col1, row2, col2):
        key1 = f"{row1},{col1}"
        key2 = f"{row2},{col2}"
        
        self.connections[key1] = (row2, col2)
        self.connections[key2] = (row1, col1)
        
    def _remove_connection(self, row, col):
        key = f"{row},{col}"
        if key in self.connections:
            connected_row, connected_col = self.connections[key]
            connected_key = f"{connected_row},{connected_col}"
            
            if connected_key in self.connections:
                del self.connections[connected_key]
            
            del self.connections[key]
    
    def is_horizontally_connected(self, row, col, direction):
        key = f"{row},{col}"
        if key not in self.connections:
            return False
            
        connected_row, connected_col = self.connections[key]
        
        if direction == 'right' and connected_col > col:
            return True
        elif direction == 'left' and connected_col < col:
            return True
            
        return False
    
    def _find_matches(self):
        matches = set()  
        
        for row in range(self.rows):
            current_color = None
            current_group = []
            
            for col in range(self.columns):
                cell_value = self.field[row][col]
                cell_color = cell_value.lower() if cell_value in 'RBYrby' else None
                
                if cell_color is None:
                    if current_color is not None and len(current_group) >= 4:
                        matches.update(current_group)
                    
                    current_color = None
                    current_group = []
                    
                elif cell_color == current_color:
                    current_group.append((row, col))
                    
                else:
                    if current_color is not None and len(current_group) >= 4:
                        matches.update(current_group)
                    
                    current_color = cell_color
                    current_group = [(row, col)]
            
            if current_color is not None and len(current_group) >= 4:
                matches.update(current_group)
        
        for col in range(self.columns):
            current_color = None
            current_group = []
            
            for row in range(self.rows):
                cell_value = self.field[row][col]
                cell_color = cell_value.lower() if cell_value in 'RBYrby' else None
                
                if cell_color is None:
                    if current_color is not None and len(current_group) >= 4:
                        matches.update(current_group)
                    
                    current_color = None
                    current_group = []
                    
                elif cell_color == current_color:
                    current_group.append((row, col))
                    
                else:
                    if current_color is not None and len(current_group) >= 4:
                        matches.update(current_group)
                    
                    current_color = cell_color
                    current_group = [(row, col)]
            
            if current_color is not None and len(current_group) >= 4:
                matches.update(current_group)
        
        return list(matches)
    
    def _apply_matches(self, matches):
        if matches:
            for row, col in matches:
                self._remove_connection(row, col)
                self.field[row][col] = ' '
    
    def _apply_gravity(self):
        for row in range(self.rows - 2, -1, -1): 
            for col in range(self.columns):
                if self.field[row][col] in 'RBY':
                    if self.field[row + 1][col] == ' ':
                        key = f"{row},{col}"
                        if key in self.connections:
                            connected_row, connected_col = self.connections[key]
                            
                            if connected_col > col:
                                if self.field[row + 1][connected_col] == ' ':
                                    self.field[row + 1][col] = self.field[row][col]
                                    self.field[row + 1][connected_col] = self.field[row][connected_col]
                                    self.field[row][col] = ' '
                                    self.field[row][connected_col] = ' '
                                    
                                    self._remove_connection(row, col)
                                    self._add_connection(row + 1, col, row + 1, connected_col)
                            elif connected_col < col:
                                pass
                        else:
                            self.field[row + 1][col] = self.field[row][col]
                            self.field[row][col] = ' '
    
    def has_viruses(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.field[row][col] in 'rby':
                    return True
        return False
    
    def get_field_representation(self):
        field_rep = []
        
        for row in range(self.rows):
            row_str = '|'
            
            for col in range(self.columns):
                cell = self.field[row][col]
                
                is_faller_cell = False
                if self.faller is not None:
                    for i, segment in enumerate(self.faller['segments']):
                        if segment['row'] == row and segment['col'] == col:
                            is_faller_cell = True
                            color = segment['color']
                            
                            if self.faller['landed']:
                                if self.faller['orientation'] == 'horizontal':
                                    if i == 0:  
                                        row_str += '|' + color + '-'
                                    else:
                                        row_str += '-' + color + '|'
                                else:
                                    row_str += '|' + color + '|'
                            else:
                                if self.faller['orientation'] == 'horizontal':
                                    if i == 0:  
                                        row_str += '[' + color + '-'
                                    else:
                                        row_str += '-' + color + ']'
                                else:
                                    row_str += '[' + color + ']'
                            
                            break
                            
                if not is_faller_cell:
                    if cell == ' ':
                        row_str += '   '
                    elif cell in 'rby':
                        row_str += ' ' + cell + ' '
                    elif cell in 'RBY':
                        if self.is_horizontally_connected(row, col, 'right'):
                            row_str += ' ' + cell + '-'
                        elif self.is_horizontally_connected(row, col, 'left'):
                            row_str += '-' + cell + ' '
                        else:
                            row_str += ' ' + cell + ' '
            
            row_str += '|'
            field_rep.append(row_str)
            
        field_rep.append(' ' + '-' * (3 * self.columns) + ' ')
        
        if not self.has_viruses():
            field_rep.append('LEVEL CLEARED')
            
        return field_rep
    
    def get_matching_field_representation(self, matches):
        field_rep = []
        
        for row in range(self.rows):
            row_str = '|'
            
            for col in range(self.columns):
                is_match = (row, col) in matches
                
                if is_match:
                    cell = self.field[row][col]
                    row_str += '*' + cell + '*'
                else:
                    cell = self.field[row][col]
                    
                    is_faller_cell = False
                    if self.faller is not None:
                        for i, segment in enumerate(self.faller['segments']):
                            if segment['row'] == row and segment['col'] == col:
                                is_faller_cell = True
                                color = segment['color']
                                
                                if self.faller['landed']:
                                    if self.faller['orientation'] == 'horizontal':
                                        if i == 0:
                                            row_str += '|' + color + '-'
                                        else:
                                            row_str += '-' + color + '|'
                                    else:
                                        row_str += '|' + color + '|'
                                else:
                                    if self.faller['orientation'] == 'horizontal':
                                        if i == 0:
                                            row_str += '[' + color + '-'
                                        else:
                                            row_str += '-' + color + ']'
                                    else:  
                                        row_str += '[' + color + ']'
                                
                                break
                                
                    if not is_faller_cell:
                        if cell == ' ':
                            row_str += '   '
                        elif cell in 'rby':
                            row_str += ' ' + cell + ' '
                        elif cell in 'RBY':
                            if self.is_horizontally_connected(row, col, 'right'):
                                row_str += ' ' + cell + '-'
                            elif self.is_horizontally_connected(row, col, 'left'):
                                row_str += '-' + cell + ' '
                            else:
                                row_str += ' ' + cell + ' '
            
            row_str += '|'
            field_rep.append(row_str)
            
        field_rep.append(' ' + '-' * (3 * self.columns) + ' ')
                
        return field_rep