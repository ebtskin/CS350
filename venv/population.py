# imports midi module into project
import midi

# imports random number module
import random as rand

# imports math module
import math as math

# allows downloading midi tracks
from google.colab import files

# useful constants
PITCH_MAX = 127
VEL_MAX = 127

class Population():

    def __init__(self, num_of_members):
        for x in range(0, num_of_members):
            tracks = []
            new_track = Track()
            new_track.dumbRandom(goal_track)
            tracks.append(new_track)

    def delete_parent(self, parent1, parent2):
        del tracks[parent1]
        del tracks[parent2]



class Track():
    # Holds the notes and BPM for a given track

    # Serves effectively as a "genome" for our use, with the
    # notes list serving as the "alleles"

    # A track is a list of notes, a number describing the number of notes, and a
    # bpm which gives time context to ticks
    ##
    # Each note is
    #         name                desc                         range
    #      start tick     the tick the note begins at         0 - inf
    #      duration       how many ticks the note lasts       0 - inf
    #      pitch          what the note's sound is            0 - 127
    #      velocity       how hard the note is played         0 - 127
    #
    # more info on pitch (might be relevant for heuristics):
    #             There are 12 notes in total
    #        C  C#  D  D#  E  F  F#  G  G#  A  A#  B
    # pitch  0  1   2  3   4  5  6   7  8   9  10  11
    #
    #        These repeat until the max value of 127 (which happens to be a G)
    #        Each repetition is called an Octave, with 0-11 being octave 1,
    #        12-23 octave 2, etc...
    #
    #        You can get the note name by calling
    #             midi.NOTE_NAMES[note.pitch % midi.OCTAVE_MAX_VALUE]
    #        where note.pitch is the note you want the name of

    # List of notes in the track
    notes = []

    # "B"eats "P"er "M"inute - the number of quarter notes per minute
    # might be relevant later when calculating the fitness
    # of note durations
    bpm = 0

    # Number of notes in the track
    num = 0

    def __init__(self):
        self.notes = []
        self.bpm = 0
        self.num = 0

    # overloads the print operation
    def __repr__(self):
        print("BPM: ", self.bpm)
        for note in self.notes:
            print(self.notes.index(note), " ", note)
        return " "

    # Parses out the notes from the input pattern and sets the track's bpm and
    # number of notes
    #
    # NoteOnEvents dictate when a note starts, so it is copied over to the notes list
    # NoteOffEvents only come after NoteOnEvents, and are associated with the same pitch
    #                                     so we can find the duration of the note
    def parsePattern(self, pattern):
        self.bpm = pattern[0][0].get_bpm()
        pattern.make_ticks_abs()
        for event in pattern[1]:
            if isinstance(event, midi.NoteOnEvent):
                note = Track.Note(event.tick, 0, event.pitch, event.velocity)
                self.notes.append(note)
                self.num += 1
            elif isinstance(event, midi.NoteOffEvent):
                for note in self.notes:
                    if (note.duration == 0) and (note.pitch == event.data[0]):
                        note.duration = event.tick - note.start

    # Outputs the track as a midi.Pattern to be encoded back into a midi file
    # by the midi module
    ##
    # NEEDS the input pattern in order to reattach certain parts
    def outputPattern(self, pattern):
        output = midi.Pattern(resolution=pattern.resolution)
        output.append(pattern[0])
        track = midi.Track()

        # for event in pattern[1]:
        # if isinstance(event, midi.NoteOnEvent):
        #    break
        #  track.append(event)

        for note in self.notes:
            track.append(midi.NoteOnEvent(tick=note.start, pitch=note.pitch, velocity=note.velocity))

            track.append(midi.NoteOffEvent(tick=(note.start + note.duration), \
                                           pitch=note.pitch, \
                                           velocity=100))

        track.append(midi.EndOfTrackEvent(tick=track[-1].tick + 10))
        output.append(track)
        return output

    # creates random notes and stores them in its note list
    #
    # this method uses no outside information besides the number of notes to create
    def dumbRandom(self, goal):
        self.num = goal.num
        self.bpm = goal.bpm

        for x in range(0, goal.num):
            temp_note = Track.Note()
            temp_note.random()
            self.notes.append(temp_note)

    # calculates a direct comparison between two tracks
    # using Note()'s compare method
    def dumbFitness(self, target):
        if (self.num != target.num):
            return 0

        fitness = 0
        for i in range(0, self.num):
            fitness += self.notes[i].compare(target.notes[i])
        return fitness

    class Note():
        # Holds the note information

        # initalizes note to parameters or to 0 if none given
        def __init__(self, start=0, duration=0, pitch=0, velocity=0):
            self.start = start
            self.duration = duration
            self.pitch = pitch
            self.velocity = velocity

        # overloads less-than operator for list sorting
        # USES ticks as sort value
        # used at the moment for reorganizing random notes
        # that are out of order in the note list
        def __lt__(self, other):
            return self.start < other.start

        def __repr__(self):
            return "Note(start=%r, duration=%r, pitch=%r, velocity=%r)" % \
                   (self.start, self.duration, self.pitch, self.velocity)

        # creates random note, start arbitrarily capped at 1000
        #                      duration arbitrarily capped at 640
        def random(self):
            self.start = rand.randint(0, 2000)
            self.pitch = rand.randint(37, 49)
            # self.duration = rand.randint(0, 640)
            # self.velocity = rand.randint(0, VEL_MAX)
            self.duration = 240
            self.velocity = 100

        # directly compares two notes and returns value based on comparison
        # to keep things simple on this one, each field is worth one fitness
        ##
        # probably a better way to do this...
        def compare(self, note):
            value = 0
            if (self.start == note.start):
                value += 1
            else:
                value -= 1
            if (self.duration == note.duration):
                value += 1
            else:
                value -= 1
            if (self.pitch == note.pitch):
                value += 1
            else:
                value -= 1
            if (self.velocity == note.velocity):
                value += 1
            else:
                value -= 1

            return value

