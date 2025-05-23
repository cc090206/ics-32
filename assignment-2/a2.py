#!/usr/bin/env python3

import shlex
from game_logic import DrMarioGame

def main():
    rows = int(input().strip())
    columns = int(input().strip())
    
    game = DrMarioGame(rows, columns)
    
    config_type = input().strip()
    
    if config_type == 'CONTENTS':
        contents = []
        for _ in range(rows):
            row = input()
            contents.append(row)
        game.set_initial_contents(contents)
    elif config_type == 'EMPTY':
        pass
    
    matches = game._find_matches()
    if matches:
        field_rep = game.get_matching_field_representation(matches)
        for line in field_rep:
            print(line)
        
        game._apply_matches(matches)
        game._apply_gravity()
        
        matches = game._find_matches()
        while matches:
            field_rep = game.get_matching_field_representation(matches)
            for line in field_rep:
                print(line)
                
            game._apply_matches(matches)
            game._apply_gravity()
            matches = game._find_matches()
    
    field_rep = game.get_field_representation()
    for line in field_rep:
        print(line)
    
    while True:
        command = input().strip()
        
        if command == 'Q':
            break
            
        elif command == '':
            game.update()
            
        elif command.startswith('F'):
            parts = shlex.split(command)
            if len(parts) == 3:
                left_color = parts[1]
                right_color = parts[2]
                
                mid = (columns // 2) - 1
                
                if game.field[1][mid] != ' ' or game.field[1][mid+1] != ' ':
                    print("GAME OVER")
                    break
                    
                game.create_faller(left_color, right_color)
                
        elif command == 'A':
            game.rotate_faller_clockwise()
            
        elif command == 'B':
            game.rotate_faller_counterclockwise()
            
        elif command == '<':
            game.move_faller_left()
            
        elif command == '>':
            game.move_faller_right()
            
        elif command.startswith('V'):
            parts = shlex.split(command)
            if len(parts) == 4:
                row = int(parts[1])
                col = int(parts[2])
                color = parts[3]
                
                game.create_virus(row, col, color)
                
        matches = game._find_matches()
        if matches:
            field_rep = game.get_matching_field_representation(matches)
            for line in field_rep:
                print(line)
                
            game._apply_matches(matches)
            game._apply_gravity()
            
            matches = game._find_matches()
            while matches:
                field_rep = game.get_matching_field_representation(matches)
                for line in field_rep:
                    print(line)
                    
                game._apply_matches(matches)
                game._apply_gravity()
                matches = game._find_matches()
        
        field_rep = game.get_field_representation()
        for line in field_rep:
            print(line)

if __name__ == '__main__':
    main()