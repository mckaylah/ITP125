import getopt, sys
import platform
import os
import urllib
from subprocess import call

#holds all of the filenames of numeric option-files
numeric_file_strings = ['0.mp3', '1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3', '8.mp3', '9.mp3']

#holds all filenames of non-numeric option-files
media_files = {'m':
                 {'endings': [
                        ['Riding a Horse', 'Listening to a jingle', 'On a phone', 'Swan dive', 'Voicemail'],
                        ['m-e1-horse.mp3', 'm-e2-jingle.mp3', 'm-e3-on_phone.mp3', 'm-e4-swan_dive.mp3', 'm-e5-voicemail.mp3']
                    ],
                  'reasons': [
                        ['On top of a building', 'Cracking Walnuts', 'Polishing a monocle', 'Ripping weights'],
                        ['m-r1-building.mp3', 'm-r2-cracking_walnuts.mp3', 'm-r3-polishing_monocle.mp3', 'm-r4-ripping_weights.mp3']
                    ]
                 },
               'f':
                 {'reasons': [
                        ['Ingesting Old Spice', 'Listening to Reading', 'Lobster Dinner', 'Moon Kiss', 'Riding a Horse'],
                        ['f-r1-ingesting_old_spice.mp3', 'f-r2-listening_to_reading.mp3', 'f-r3-lobster_dinner.mp3', 'f-r4-moon_kiss.mp3', 'f-r5-riding_a_horse.mp3']
                    ],
                  'endings': [
                        ['She will get back to you', 'Thanks for Calling'],
                        ['f-e1-she_will_get_back_to_you.mp3', 'f-e2-thanks_for_calling.mp3']
                     ]
                 }
              }

default_files = ['m-b1-hello.mp3', 'm-b2-have_dialed.mp3', 'f-b1-hello_caller.mp3', 'f-b2-lady_at.mp3', 'm-r0-cannot_come_to_phone.mp3',
        'f-r0.1-unable_to_take_call.mp3', 'f-r0.2-she_is_busy.mp3', 'm-leave_a_message.mp3', 'm-youre_welcome.mp3']

#initializes the global list of filenames
mp3_file_list = list()

#global vars
gender = ''
outputFile = ''
helpMenu = False

## Function retrieveGender(arg)
# this function will set the global gender var
# to the appropriate value and then add the starting default mp3 files
# @param arg the string argument that is a gender, either 'm' or 'f', otherwise raising an exception
def retrieveGender( arg ):
    global gender
    gender = str(arg)
    if(gender == 'm'):
        mp3_file_list.append('m-b1-hello.mp3')
        mp3_file_list.append('m-b2-have_dialed.mp3')
    elif(gender == 'f'):
        mp3_file_list.append('f-b1-hello_caller.mp3')
        mp3_file_list.append('f-b2-lady_at.mp3')
    else:
        #raise error message if neither
        raise Exception('\''+ gender + '\' is not a valid gender')

## Function keyIsInvalid(key_arg, type)
# This function checks to see if the value of the index is valid
# @param key_arg the integer value of the index of the option
# @param type the string argument of the type of value the index refers too, i.e. 'reasons' or 'endings'
# @return True if the key is valid, false otherwise
def keyIsValid(key_arg, type):
    key = int(key_arg)
    value_type = str(type)
    if(value_type == 'reasons'):
        if(gender == 'm'):
            return (key > 0 or key <= 4)
        elif(gender == 'f'):
            return (key > 0 or key <= 5)
        else:
            return True
    elif(value_type == 'endings'):
        if(gender == 'm'):
            return (key > 0 or key <= 5)
        elif(gender == 'f'):
            return (key > 0 or key <= 2)
        else:
            return True
## Function addStandardReasons()
# This function will just add standard reasons (introductions to the reasons) for the correct gender
def addStandardReasons():
    if(gender == 'm'):
        mp3_file_list.append('m-r0-cannot_come_to_phone.mp3')
    elif(gender == 'f'):
        mp3_file_list.append('f-r0.1-unable_to_take_call.mp3')
        mp3_file_list.append('f-r0.2-she_is_busy.mp3')
## Function retrieveMedia(input_arg, type_arg)
# This function will add all appropriate mp3 files to the list for
# the numerical fields like reasons and endings
# @param input_arg the number input for the options to add
# @param type_arg the type of the arg, i.e. 'reasons' or 'endings'
def retrieveMedia(input_arg, type_arg):
    length = len(str(input_arg))
    integerArg = int(input_arg)

    type = str(type_arg)

    digits = [0,0,0,0,0]

    count = 5

    digits[4] = integerArg//10000
    digits[3] = (integerArg%10000)//1000
    digits[2] = (integerArg%1000)//100
    digits[1] = (integerArg%100)//10
    digits[0] = (integerArg%10)
    usedList = list() #keeps track of values so we can't use the same clip twice
    for i in range(length):
        value = digits[length-i-1]
        if( not (value in usedList) and keyIsValid(value,type)) :
            mp3_file_list.append(media_files[gender][type][1][value-1])
            usedList.append(value)
        else:
            raise Exception(str(type_arg) + ' #' + str(value) + ' ERROR')
            return

##Function getPhoneNumber(input_arg)
# Checks to see if the phone-number is in a valid form for entry and then adds
# the appropriate mp3 filenames to the list
def getPhoneNumber(input_arg):
    input = str(input_arg)
    tempList = list()
    composite = ''
    for i in range(len(input)):
        try:
            num = int(input[i])
            composite = composite + str(num)
            #make use only of the digits
            tempList.append(numeric_file_strings[num])
        except ValueError:
            #do nothing
            continue

    #create phoneNumber templates
    stringType1 = composite[:3]+'-'+composite[3:6]+'-'+composite[6:]
    stringType2 = '('+composite[:3]+') '+composite[3:6]+'-'+composite[6:]
    stringType3 = composite[:3]+'.'+composite[3:6]+'.'+composite[6:]
    stringType4 = composite[0:]

    #compared the entered data to the templates
    if(not (input == stringType1 or input == stringType2 or input == stringType3 or input == stringType4) ):
        raise Exception('Invalid Phone Number length')

    #if there wasn't an exception, append the strings
    for string in tempList:
        mp3_file_list.append(string)

## Function printContextualMenu(type_arg)
# This function will print a help menu for the correct type
# @param type_arg the type of the menu, i.e. 'reasons' or 'endings'
# @param the delimiter for each line
def printContextualMenu(type_arg, delim = ''):
    type = str(type_arg)
    val_list = media_files[gender][type][1];
    key_list = media_files[gender][type][0];

    for i in range(len(val_list)):
        print(str(delim)+'Option '+str(i+1)+' : '+key_list[i])

## Function that checks to see if a file is in one of the reserved filenames --
# one of the one's we'd want to download later
# @param arg the file we're going to check
def checkOutputFile(arg):
    file = str(arg)
    return not (file in numeric_file_strings or file in media_files['m']['reasons'][1] or file in media_files['m']['endings'][1]
       or file in media_files['f']['reasons'][1] or file in media_files['f']['endings'][1] or file in default_files)
       
## Function createMP3FileWithPrompts()
# Formats all of the options in the filename list in a walkthrough style
def createMP3FileWithPrompts():
    global mp3_file_list, outputFile, hasGender, hasPhoneNumber, hasReasons, hasEndings, hasOutputFile
    while(True):
        inputVal = raw_input('M or F: ')
        try:
            if(inputVal == ''):
                continue
            retrieveGender(inputVal)
            hasGender = True
            break
        except:
            print('\tError: Use correct gender')
            continue

    while(True):
        try:
            phoneNumber = raw_input('\nPhone Number : ')
            if(phoneNumber == ''):
                continue
            getPhoneNumber(phoneNumber)
            hasPhoneNumber = True
            break
        except:
            print('\tError: Enter correct phone Number in the following form:')
            composite = '1234567890'
            stringType1 = composite[:3]+'-'+composite[3:6]+'-'+composite[6:]
            stringType2 = '('+composite[:3]+') '+composite[3:6]+'-'+composite[6:]
            stringType3 = composite[:3]+'.'+composite[3:6]+'.'+composite[6:]
            stringType4 = composite[0:]
            print('\t\t'+stringType1)
            print('\t\t'+stringType2)
            print('\t\t'+stringType3)
            print('\t\t'+stringType4)
            continue

    #handle reasons
    addStandardReasons()
    print('')
    printContextualMenu('reasons')

    while(True):
        try:
            reasonKey = raw_input('\nWhat is your excuse? (no spaces for mult entries) ' )
            if(reasonKey == ''):
                continue
            retrieveMedia(reasonKey, 'reasons')
            hasReasons = True
            break
        except Exception as e:
            print('\tError: This is a reason issue: '+ str(e))
            continue

    print('')
    printContextualMenu('endings')

    #handle endings
    while(True):
        try:
            endingKey = raw_input('\nWhich ending? (no spaces for mult entries) ')
            if(endingKey == ''):
                continue
            retrieveMedia(endingKey, 'endings')
            hasEndings = True
            break
        except Exception as e:
            print('This is an ending issue: ' + str(e))
            continue

    #add default endings if applicable
    if(gender == 'm'):
        mp3_file_list.append('m-leave_a_message.mp3')
        mp3_file_list.append('m-youre_welcome.mp3')

## Function printCommandLineOptions()
# print the command-line options for the --help menu
def printCommandLineOptions():
    global gender
    print('Command Line options: ')
    print('\t-g\tmale or female (m/f)')
    print('\t-n\tphone number in one of the following formats: ')
    composite = '6969696969'
    stringType1 = composite[:3]+'-'+composite[3:6]+'-'+composite[6:]
    stringType2 = '('+composite[:3]+') '+composite[3:6]+'-'+composite[6:]
    stringType3 = composite[:3]+'.'+composite[3:6]+'.'+composite[6:]
    stringType4 = composite[0:]
    print('\t\t\t'+stringType1 + 'OR')
    print('\t\t\t'+stringType2 + 'OR')
    print('\t\t\t'+stringType3 + 'OR')
    print('\t\t\t'+stringType4 + 'OR')
    print('\t-r\treasons: pick any of the following options:')
    print('\t\t\tmale: ')
    gender = 'm'
    printContextualMenu('reasons', '\t\t\t\t')
    print('\t\t\tfemale: ')
    gender = 'f'
    printContextualMenu('reasons', '\t\t\t\t')
    print('\t-e\tendings: pick any ONE of the following options:')
    print('\t\t\tmale: ')
    gender = 'm'
    printContextualMenu('endings', '\t\t\t\t')
    print('\t\t\tfemale: ')
    gender = 'f'
    printContextualMenu('endings', '\t\t\t\t')
    print('\t-o\toutput filename')
    print('\n\t--Step\twalkthrough of this process')

#some globals for error-checking
hasGender = False
hasPhoneNumber = False
hasReasons = False
hasEndings = False
hasOutputFile = False

## Function handleCommandLineArgs()
# This function simply handles the commandline approach of the problem, and can start the walkthrough
def handleCommandLineArgs():
    global outputFile, helpMenu
    global hasGender, hasPhoneNumber, hasReasons, hasEndings, hasOutputFile
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'g:n:r:e:o:', ["Step","help"])
    except getopt.GetoptError as e:
        raise Exception('Invalid argument: ' + str(e))
    options, args = zip(*opts)
    if('--Step' in options):
        createMP3FileWithPrompts()
    elif('--help' in options):
        printCommandLineOptions()
        helpMenu = True
        return
    else:
        #because other data hinges on g, find it first
        if('-g' in options):
            for o, a in opts:
                if(o == '-g'):
                    try:
                        retrieveGender(a)
                        hasGender = True
                    except Exception as e:
                        raise e
        for o, a in opts:
            if(o == '-n'):
                try:
                    getPhoneNumber(a)
                    hasPhoneNumber = True
                except Exception as e:
                    raise e
            elif(o == '-r'):
                try:
                    retrieveMedia(a, 'reasons')
                    hasReasons = True
                except Exception as e:
                    raise e
            elif(o == '-e'):
                try:
                    retrieveMedia(a, 'endings')
                    hasEndings = True
                except Exception as e:
                    raise e
            elif(o == '-o'):
                outputFile = str(a)
                fileType = outputFile[len(outputFile)-4:]
                if(not fileType == '.mp3'):
                    outputFile = outputFile+'.mp3'
                hasOutputFile = True
    if(gender == 'm'):
        mp3_file_list.append('m-leave_a_message.mp3')
        mp3_file_list.append('m-youre_welcome.mp3')

##
# Main program
def main():
    global mp3_file_list, outputFile, helpMenu

    mp3_file_list = list()
    try:
        #use the commandline arguments
        handleCommandLineArgs()
    except Exception as e:
        print('Error, dumbass')
        print('\t'+ str(e.args[0]))
        print('\n--Step to step through step-by-step process or --help for help, obviously')
        return

    if(helpMenu):
        return
    #check OS
    dir = os.getcwd()
    #format file for correct OS
    for string in mp3_file_list:
        temp = string[:]
        temp = temp.replace(' ', '')[:-4]
        temp = temp.replace('_', ' ')
        if(string[0] >= '0' and string[0] <= '9'):
            print(temp)
        elif(string[4] == '-'):
            print(temp.replace('','')[5:])
        else:
            print(temp.replace('','')[2:])
    correct_out = raw_input('Is this correct? (y/n) ')
    if(correct_out == 'y'):
        if(outputFile == ''):
            while(True):
                outputFile = raw_input("\nOutfile Name? ")
                if(outputFile == ''):
                  continue
                fileType = outputFile[len(outputFile)-4:]
                if(not fileType == '.mp3'):
                    outputFile = outputFile+'.mp3'
                if(checkOutputFile(outputFile)):
                    hasOutputFile = True
                    break
                print('Try again, ugly')
                #format the output file to just have one .mp3 at the end
        filename = outputFile
        fileType = outputFile[len(outputFile)-4:]
        if(not fileType == '.mp3'):
            outputFile = outputFile+'.mp3'
            filename = filename+'.mp3'
        name = outputFile[:len(outputFile)-4]
        slash = '/'
        command = 'cat'
        commandOperator = ' > '
        delete = 'rm '
        if(platform.system() == 'Windows'):
            slash = '\\'
            command = 'copy /b '
            delete = 'DEL '
            commandOperator = ' '
        outputFile = str(dir)+str(slash)+str(outputFile)
        outputTextFile = str(dir) + str(slash) + str(name) + '.txt'
        #overwrite existing text file
        logfile = open(str(outputTextFile), 'w')
        logfile.write('')
        logfile.close()
        #output new outputTextFile
        logfile = open(str(outputTextFile), 'a')
        #command = 'copy ' + str(option) + 'b '+folderPath+'*.mp3 '+outputFile

        #write information to the textfile
        for string in mp3_file_list:
            logfile.write(str(string)+'\n')
            fragment_path = str(dir) + str(slash) + string
            if(platform.system() == 'Windows' and started):
                command = command + ' + ' + string
            else:
                command = command + ' ' + string
            frag_file = open(fragment_path, 'w')
            #get the necessary files from the internet
            urllib.urlretrieve('http://www-bcf.usc.edu/~chiso/itp125/project_version_1/'+str(string), fragment_path)
        file_temp = open(outputFile, 'w')
        #format command
        cmd = command + commandOperator + filename
        file_temp.close()
        os.system(cmd)

        deleted_list = list()
        #cleanup
        for string in mp3_file_list:
            fragment_path = str(dir) + str(slash) + string
            if(not fragment_path in deleted_list):
                deleted_list.append(fragment_path)
                os.system(delete + ' ' + fragment_path)
        logfile.close()
    else:
        main()

main()