import chess
import gpiozero
import time
import serial
from collections import Counter
import atexit
import math

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
end_turn = False

turn_button = gpiozero.Button(12)

#--------------------------convers int to correct poll selector pins


def next_turn():
    global end_turn
    end_turn = True
    print("turn ended \n")

turn_button.when_pressed = next_turn

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

def closing():
	print("closing serial port")
	ser.close()
	
atexit.register(closing);


#convert true false array to arduino string
def toArduinoString(board):
	s = ''
	
	for b in board:
		if b == True:
			s += '1'
		else:
			s += '0'
	
	return s

#set serial parameters

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
ntl = ['a','b','c','d','e','f','g','h' ]

# convert int to board coordinate
def convert_loc(num):
    row_num = math.floor(num/8)
    row = str(row_num+1)
    col = ntl[num-(row_num*8)]
    return col+row
    

def main():
    board = chess.Board() # for chess api
    ser.write("hello".encode())
    time.sleep(2)
    crnt = [True]*16 + [False]*32, [True]*16 #sets starting board
    change_list = [] #vector of matrixs to keep track of changes
    count = 0 # number of changes
    #change_list.append(crnt)
    start_loc = -1 #piece start and end locations
    end_loc = -1
    num_pieces = 32
    piece_taken = False
    global end_turn
    white = True
    atts = []
    
    
    while(False == end_turn):# wait for end turn to calabrate board
        ser.flush()
        crnt = poll_board()
        change_list.append(crnt)
        print(toArduinoString(crnt))
        print(len(toArduinoString(crnt)))
        ser.write(toArduinoString(crnt).encode())
        print("sending to arduino")
        print("\nnumber of pieces detected: "+str(Counter(crnt)[True]))
        time.sleep(5)
	
    end_turn = False
    
    while(True): # run indefinatly
        time.sleep(1)
        crnt = poll_board() #get board state
        
        if(end_turn): #check if turn ended, if true reset to begining with crnt state
            print("moving to next turn\n")
            end_turn = False
            count = 0
            num_pieces = Counter(crnt)[True]
            print("move string")
            print(str(start_loc+end_loc))
            if(crnt != change_list[0]):
                #check if legal move
                if(chess.Move.from_uci(start_loc+end_loc) in board.pseudo_legal_moves):
                    move = chess.Move.from_uci(start_loc+end_loc)
                    board.push(move)
                    print(board)
                    print("chess.WHITE before flip: " + str(chess.WHITE))
                    if(white):
                        white = False
                    else:
                        white = True
                    change_list = []
                    change_list.append(crnt)
                    
                else:
                    print("not legal move")
                    #alert player 
                    ser.flush()

                    while(False == end_turn):# wait for end turn to calabrate board
                        print("illegal move detected please move pieces back to the start of turn positioning.\n")
                        print(toArduinoString(change_list[0]))
                        ser.write(toArduinoString(change_list[0]).encode())
                        print("sending to arduino")
                        time.sleep(8)
                        break
                
                    end_turn = False
                    crnt = change_list[0]
                    change_list = []
                    change_list.append(crnt)
                    count = 0   
                    print("\nstart turn\n")         

            
            
            
            #chess.WHITE = ~chess.WHITE
            #chess.BLACK = ~chess.BLACK
            
            
        if(crnt == change_list[count]): # no change so keep moving
            pass
        else:# found change, send piece and location to arduino
            count+=1
            print("found change \n")
            #print(change_list)
            change_loc = find_dif(change_list[count-1], crnt)
            print(change_loc)
            sqr =chess.SQUARES[change_loc]
            atts = []
           
            
            
            change_list.append(crnt)
            
            if(count == 1): # piece picked up, mark starting location
                start_loc = convert_loc(change_loc)
                if(board.piece_type_at(sqr) == 1):#if piece is a pawn
                    print("is it whites turn")
                    print(white)
                    if(white):
                        shift = 8
                    else:
                        shift = -8
                        
                    if((change_loc >= 8 and change_loc <= 15 and white) or (change_loc >= 48 and change_loc <= 55 and white == False)):
                        atts.append(change_loc+shift)
                        atts.append(change_loc+(shift*2))
                    else:
                        atts.append(change_loc+shift)
                        
                    if(crnt[change_loc+shift+1]):
                        atts.append(change_loc+shift+1)
                    if(crnt[change_loc+shift-1]):
                        atts.append(change_loc+shift-1)
                    
                else:
                    atts = list(board.attacks(sqr))
                amoves = [False]*64
                for i in range(0,len(atts)):
                    print(atts)
                    amoves[atts[i]] = True
                #send to arduino, fpiece, change_loc
                ser.write(toArduinoString(amoves).encode())
                
            elif(count == 2):# piece either picked up for taking, or original piece picked up or a simple move 
                if(change_list[count] != change_list[0]): # not put back either normal move or taken piece
                    end_loc = convert_loc(change_loc)
                    if(num_pieces-2 == Counter(crnt)[True]): #piece is taken
                        piece_taken = True
                        
                else: # put piece back
                    count = 0
                    change_list = [change_list[0]]                    
            elif(count == 3):#third change, check if put piece back after being taken
                if(piece_taken == True and num_pieces-1 == Counter(crnt)[True]):
                    piece_taken == False
            else:
                while(False == end_turn):# wait for end turn to calabrate board
                    ser.flush()
                    print("error detected please move pieces back to the start of turn positioning.\n")
                    print(toArduinoString(change_list[0]))
                    ser.write(toArduinoString(change_list[0]).encode())
                    print("sending to arduino")
                    time.sleep(8)
                    break
                
                end_turn = False
                crnt = change_list[0]
                change_list = []
                change_list.append(crnt)
                count = 0   
                print("\nstart turn\n")
        if(board.is_checkmate()):
            print("checkmate")
                
                


	
main()

'''
print(poll_board())

while(True):
	
    ser.flush()
	
	#print ("\nnumber of true: "+ str(poll_board()))
    board_str = toArduinoString(poll_board())

    #board_str = "0010000001100000011000000110000011000000110000001100000011000000"
    print("about to send to arduino: " + board_str)
    ser.write(board_str.encode())
    print("sent to arduino")
    time.sleep(8.5)
'''
