from nltk.chat.util import Chat

def main(inputData):

    #create pairs

    pairs =[
        ["my name is Budi", ["Halo Budi"]],
        ["how are you"], ["I am fine"]]
        ]

    chat = Chat(pairs)

    #get response in output variable

    outputData = chat.respond(inputData)

    #we will pass input data here and save out in "outputData" variable

    #finally return output data
    
    return ""+str(outputData)
