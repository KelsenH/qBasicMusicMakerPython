'''
qBasicMusicPlayer.py
Author: Kelsen Hazelwood
Date Created: April 11, 2016
Purpose: Allow the user to type music using syntax from qBasic and have it output
to a midi device
'''

import pygame
from pygame import midi
from time import sleep
import pdb

'''Class that contains all the attributes and methods of the user's song
This includes the notes they can use, commands they can use, as well as their
music that they write in the shell. This class is the mechanism that runs this program'''
class userSong (midi.Output):
    def __init__ (self,outputDevice = 0, octave = 60, tempoBPM = 120,velocity = 100):
        super (midi.Output,self).__init__()
        pygame.midi.init()

        self.getOutputDevice() #Finds any connected MIDI device, and sets it as the output device
        self.setOctave(octave) #Sets the octave to the octave that the is set in initialization
        self.changeTempo (tempoBPM) #Sets the tempo to the tempo that is set in initialzation

        self.__notes = ['C','D','E','F','G','A','B','R'] #Notes that can be used

        self.__noteValues = [0,2,4,5,7,9,11,-1] #Midi values of the notes
        
        self.__commands = ['O','<','>','T'] #Commands that can be used

        self.__noteLengthValues = ((1,240),(2,120),(4,60),(8,30),(16,15)) #2D tuple of note length and value to make seconds

        self.music = input ("Play some music! ").upper() #Where the user can input their notes and commands to make the computer play music! 

        self.sortSong()
        
    '''Find the running device on the computer to play sound through'''
    def getOutputDevice (self):
        outputDeviceId = midi.get_default_output_id () #Method from midi to find default midi output connected to the machine
        self.midiOutput = midi.Output (outputDeviceId) #Sets the midiOutput of the instance to be what was found above

    '''Checks to make sure the octave is not larger than 120 or smaller than 0, if it is sets it to the closest one
    this program cheats by the octave actually being the note number of the C note that an octave starts on'''
    def setOctave (self,octave):
        if octave > 120:
            self.octave = 120
        elif octave < 0:
            self.octave = 0
        else:
            self.octave = octave

    '''Used with the < > commands to shift one octave up or one octave down'''
    def shiftOctave (self,direction):
        if direction == '<':
            self.octave = self.octave - 12
            self.setOctave(self.octave)
        elif direction == '>':
            self.octave = self.octave + 12
            self.setOctave(self.octave)

    '''Returns the octave by dividing the octave by 12 (number of half steps in an octave)'''
    def getOctave (self):
        octave = self.octave/12
        if octave < 1:
            octave = 0
        else:
            octave = int (octave)
        return octave

    '''Sets the tempo in BPM within the range of 5-990. This may need to be changed later'''
    def changeTempo (self,bpm):
        if bpm > 990:
            self.tempoBPM = 990
        elif bpm < 0:
            self.tempoBPM = 5
        else:
            self.tempoBPM = bpm

    '''Plays the note with all the attributes given'''
    def playNote (self,noteNum,length,octave,tempoBPM,velocity):
        self.midiOutput.note_on(noteNum,velocity) #Turns note on
        #To play note for the right number of seconds, find the number that corresponds to the note length
        #Take that number and divide it by the tempo. Tell the system to wait that many seconds before turning note off
        for group in self.__noteLengthValues:
            if length == group[0]:
                num = group[1]
                waitTime = num/tempoBPM
                sleep (waitTime)

    '''Matches the musicCounter input to the correct command and runs the code.
       Returns the new musicCounter value'''
    def commandExecute (self, musicCounter):
        #If command is T, change tempo
        if self.music[musicCounter] == 'T':
            newTempo = int (self.music [(musicCounter+1):(musicCounter+4)]) #Buggy thing here. Tempo must be three characters.
            self.changeTempo (newTempo)
            musicCounter = musicCounter + 4
            return musicCounter
                        
        #If command is O, change the octave   
        elif self.music [musicCounter] == 'O':
            newOctave = int (self.music [(musicCounter+1)]) * 12 #Octave must be only one charcter long
            self.setOctave (newOctave)
            musicCounter = musicCounter + 1
            return musicCounter
                        
        #If command is < or > shift in the appropriate direction
        elif self.music [musicCounter] == '<':
            self.shiftOctave ('<')
            musicCounter = musicCounter + 1
            return musicCounter
                        
        elif self.music [musicCounter] == '>':
            self.shiftOctave ('>')
            musicCounter = musicCounter + 1
            return musicCounter
        
    '''Finds the midi value, velocity, and length of the note. Returns new musicCounter value'''
    def noteCreate (self,musicCounter):
        note = self.__notes.index (self.music[musicCounter]) #Gets the note midi for octave 0
        noteValue = self.__noteValues [note]
                
        if noteValue == -1:
            self.velocity = 0
            strNoteLength = ''
                    
        else:
            self.velocity = 100
            noteNum = noteValue + self.octave #Adds the octave to it to move note to correct octave
            strNoteLength = ''
                    
        #If next thing in string is a sharp or a flat, subtract or add one half-step to the note
        #If the next thing in the string is a number, save all numbers together and set them as length
        keepGoing = True
        while keepGoing:

            place = musicCounter + 1 #Adds one to where you currently are so it can be checked

            #If it is passed or at the end of the song, go back to the end, play the final note, and end the loop
            if place >= len (self.music):
                place = place - 1 #Sets place back to being at the end of the string so it won't error
                noteLength = int(strNoteLength) #Sets note length to whatever is currently in the string
                velocity = 100
                self.playNote (noteNum,noteLength,self.octave,self.tempoBPM,self.velocity) 
                keepGoing = False
                continue #Jumps back to beginning of while loop rather than run through the rest of it pointlessly
                        
                        
            nextInString = self.music [(place)] #Gets the value from the music string of where program currently is

            #If - subtract a half step from the note num
            if nextInString == '-':
                noteNum = noteNum-1
                musicCounter = musicCounter + 1 #Add one to move on to the next thing in the string
                        
            #If # add a half step to the note num    
            elif nextInString == '#':
                noteNum = noteNum + 1
                musicCounter = musicCounter + 1

            #If it is a digit, add it to the length string
            elif nextInString.isdigit():
                strNoteLength = strNoteLength + nextInString
                musicCounter = musicCounter + 1

            #If it is anything else that does not affect the note, play the note and end the loop
            else:
                noteLength = int (strNoteLength)
                self.playNote (noteNum,noteLength,self.octave,self.tempoBPM,self.velocity)
                musicCounter = musicCounter + 1
                keepGoing = False

        return musicCounter
        
        
        
            
    '''The meat and potatoes of this program. Searches for commands and notes and performs the appropriate function.'''
    def sortSong (self):
        noteNum = 0 #Beginning value for noteNum, it will be changed as program runs
        noteLength = 1 #Beginning value for noteLength, it will be changed as the program runs
        musicCounter = 0 
                

        '''Runs through everything in the musicStr if it is a command, do the apporpriate action such as change octave
           or set tempo. If it is a note, save the note, find its length and play it'''
        while musicCounter < len (self.music):

            #If current thing in the string is a command, pass it to the commandExecute function                       
            if self.music [musicCounter] in self.__commands:
                musicCounter = self.commandExecute (musicCounter)

            #If thing in string is a note, pass it to the noteCreate function        
            elif self.music [musicCounter] in self.__notes:
                musicCounter = self.noteCreate (musicCounter)

            #Helps to skip spaces or unrecognized keys
            else:
                musicCounter = musicCounter +1

                        
        
def main():
    k = userSong () #Initialize an instance of userSong
    

#Only run main if not inherited. Basically, the final lines that makes this an official program and makes me look smarter
if __name__ == "__main__":
    main ()
        
    
