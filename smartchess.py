import chess
import gpiozero
import time
import copy
import pyserial

#-----------------pin assignment------------------

#-------------------poll pins--------------
poll_select  = [gpiozero.DigitalOutputDevice(a), gpiozero.DigitalOutputDevice(b), gpiozero.DigitalOutputDevice(c)]

read_pins = [gpiozero.Button(), gpiozero.Button(), gpiozero.Button(), gpiozero.Button(), gpiozero.Button(), gpiozero.Button(), gpiozero.Button(), gpiozero.Button()]


# ----turn button--
turn_button = gpiozero.Button()

#--------------------------convers int to correct poll selector pins
end_turn = False

def next_turn():
    end_turn = True

turn_button.when_pressed(next_turn())

def poll_number_set(num):
    poll_select[0].off()
    poll_select[1].off()
    poll_select[2].off()    
    if(num == 0):
        pass
    elif(num == 1):
        poll_select[0].on()
    elif(num == 2):
        poll_select[1].on()
    elif(num == 3):
        poll_select[0].on()
        poll_select[1].on()
    elif(num == 4):
        poll_select[2].off()  
    elif(num == 5):
        poll_select[0].on()
        poll_select[2].on()
    elif(num == 6):
        poll_select[1].on()
        poll_select[2].on()
    elif(num == 7):
        poll_select[0].on()
        poll_select[1].on()
        poll_select[2].on()
    else:
        print("range error")
        

#-----------------------------get the state of the board returns 64 bool list
def poll_board():
    read_list = []
    for i in range(0,7):
        poll_number_set(i)
        for j in range(0,7):
            read_list.append(read_pins[j])
        
    return read_list


# find difference between two matrixs
def find_dif(o_state,n_state):
    dif = -1
    tmp_cnt = 0
    for i in range(0,len(o_state)):
        if(o_state[i] != n_state[i]):
            dif = i
            tmp_cnt+=1
                
    if(tmp_cnt == 1):
        return dif
    else:
        print("\n multiple changes detected between cycles")
        return dif
    
# dertermind if char is number 
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

    
def find_piece(loc):
    if(loc > 63 or loc < 0):
        print("range error")
        return -1
    b = board.board_fen()
    i=0
    while(i<loc):
        if(is_number(b[i])):
            i+=b[i]
        else:
            i+=1
    return b[i]
        

# number index to letter index
ntl = ['a','b','c','d','e','f','g','h' ]

# convert int to board coordinate
def convert_loc(num):
    row_num = math.floor(num/8)
    row = ntl[row_num]
    col = num-row_num
    return [row,col]

def main():
    board = chess.Board() # for chess api
    crnt = [[True]*16 + [False]*32, [True]*16] #sets starting board
    change_list = [] #vector of matrixs to keep track of changes
    count = 0 # number of changes
    change_list.append(crnt)
    start_loc = -1 #piece start and end locations
    end_loc = -1
    
    while(True): # run indefinatly
        crnt = poll_board() #get board state
        if(end_turn): #check if turn ended, if true reset to begining with crnt state
            change_list = []
            change_list.append(crnt)
            end_turn = False
            count = 0
        if(crnt == change_list[count]): # no change so keep moving
            pass
        else:# found change, send piece and location to arduino
            count+=1
            change_loc = find_dif(change_list[count], crnt)
            f_pieve = find_piece(change_loc)
            #send to arduino, fpieve, change_loc
            change_list.append(crnt)
            
            if(count == 1):
                start_loc = convert_loc(change_loc)
            elif(count ==2):
                end_loc = convert_loc(change_loc)
            else:#third change, check if put piece back or made move
                if(change_list[count] != change_list[0]):
                    #check if legal move
                    if(chess.Move.from_uci(start_loc+end_loc) in board.legal_moves):
                        move = chess.Move.from_uci(start_loc+end_loc)
                        board.push(move)
                    else:
                        print("not legal move")
                        #alert player
                        
                        
                else:#put piece back
                    count = 0
                    change_list = [change_list[0]]
                
                
            
        