import chess
import gpiozero
import time
import serial
from collections import Counter

#-----------------pin assignment------------------

#-------------------poll pins--------------
switch0 = gpiozero.Button(18, pull_up = False)
switch1 = gpiozero.Button(4, pull_up = False)
switch2 = gpiozero.Button(17, pull_up = False)
switch3 = gpiozero.Button(27, pull_up = False)
switch4 = gpiozero.Button(22, pull_up = False)
switch5 = gpiozero.Button(6, pull_up = False)
switch6 = gpiozero.Button(13, pull_up = False)
switch7 = gpiozero.Button(19, pull_up = False)

mux0 = gpiozero.LED(21)
mux1 = gpiozero.LED(20)
mux2 = gpiozero.LED(16)


poll_select = [mux0, mux1, mux2]

read_pins = [switch0, switch1, switch2, switch3, switch4, switch5, switch6, switch7]

#poll_select  = [gpiozero.LED(21), gpiozero.DigitalOutputDevice(20), gpiozero.DigitalOutputDevice(16)]

#read_pins = [gpiozero.Button(18), gpiozero.Button(4), gpiozero.Button(17), gpiozero.Button(27), gpiozero.Button(22), gpiozero.Button(6), gpiozero.Button(13), gpiozero.Button(19),]


# ----turn button--
#turn_button = gpiozero.Button()

#--------------------------convers int to correct poll selector pins
end_turn = False

def next_turn():
    end_turn = True

#turn_button.when_pressed(next_turn())

#set serial parameters
    '''
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()
'''
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
        poll_select[2].on()  
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
    for i in range(0,8):
        poll_number_set(i)
        for j in range(0,8):
            read_list.append(read_pins[j].is_pressed)

    return read_list


# find difference between two matrixs returns num 0-63 for the array
def find_dif(o_state,n_state):
    dif = -1
    tmp_cnt = 0
    for i in range(0,len(o_state)):#maybe add one because range is stpd not inclusive
        if(o_state[i] != n_state[i]):
            dif = i
            tmp_cnt+=1
                
    if(tmp_cnt == 1 and dif >= 0):
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

    
#returns what type ie k, K,q, b, R
# use board.piece_type_at(sqr) instead
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
ntl = ['A','B','C','D','E','F','G','H' ]

# convert int to board coordinate
def convert_loc(num):
    row_num = math.floor(num/8)
    row = ntl[row_num]
    col = num-row_num
    return row+col

def main():
    board = chess.Board() # for chess api
    crnt = [[True]*16 + [False]*32, [True]*16] #sets starting board
    change_list = [] #vector of matrixs to keep track of changes
    count = 0 # number of changes
    change_list.append(crnt)
    start_loc = -1 #piece start and end locations
    end_loc = -1
    num_pieces = 32
    piece_taken = False
    
    while(True): # run indefinatly
        crnt = poll_board() #get board state
        if(end_turn): #check if turn ended, if true reset to begining with crnt state
            change_list = []
            change_list.append(crnt)
            end_turn = False
            count = 0
            num_pieces = crnt.Counter()[True]
            
            if(change_list[count] != change_list[0]):
                #check if legal move
                if(chess.Move.from_uci(start_loc+end_loc) in board.legal_moves):
                    move = chess.Move.from_uci(start_loc+end_loc)
                    board.push(move)
                    
                else:
                    print("not legal move")
                    #alert player                                
            
            
        if(crnt == change_list[count]): # no change so keep moving
            pass
        else:# found change, send piece and location to arduino
            count+=1
            change_loc = find_dif(change_list[count], crnt)
            sqr =chess.SQUARES[change_loc]
            if(board.piece_type_at(sqr) == 1):#if piece is a pawn
                if(chess.WHITE):
                    shift = 8
                else:
                    shift = -8
                    
                if(board.fullmove_number == 1):
                    attts = [change_loc+shift, change_loc+(shift*2)]
                else:
                    atts = [change_loc+shift]
                    
                if(crnt[change_loc+shift+1]):
                    atts.append(change_loc+shift+1)
                if(crnt[change_loc+shift-1]):
                    atts.append(change_loc+shift-1)
                
            else:
                atts = list(board.attacks(sqr))
            amoves = [0]*64
            for i in range(0,len(atts)):
                amoves[atts[i]] = 1 
            #send to arduino, fpiece, change_loc
            ser.write(amoves+"\r\n")
            
            
            change_list.append(crnt)
            
            if(count == 1): # piece picked up, mark starting location
                start_loc = convert_loc(change_loc)
                
            elif(count == 2):# piece either picked up for taking, or original piece picked up or a simple move 
                if(change_list[count] != change_list[0]): # not put back either normal move or taken piece
                    end_loc = convert_loc(change_loc)
                    if(num_pieces-2 == Counter(crnt)[True]): #piece is taken
                        piece_taken = True
                        
                else: # put piece back
                    count = 0
                    change_list = [change_list[0]]                    
            else:#third change, check if put piece back after being taken
                if(piece_taken == True and num_pieces-1 == Counter(crnt)[True]):
                    piece_taken == False
        
                        
        
        if(board.is_checkmate()):
            print("checkmate")
                
                


def toArduinoString(board):
	s = ''
	for b in board:
		if b == True:
			s += '1'
		else:
			s += '0'
			
			
	return s


print(poll_board())
while(True):
	
	#print ("\nnumber of true: "+ str(poll_board()))
	print(toArduinoString(poll_board()))
	time.sleep(2)
