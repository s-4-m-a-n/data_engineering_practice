import collections



#helper function
def compareList(l1, l2):
	"""
	  compare two lists and return true if they contain the same elements 
	"""
	
  if len(l1) != len(l2):
      return False;
  
  l1.sort()
  l2.sort()
  if l1 != l2:
    return False

  return True




#helper function 
def dataTypeMapper(x):
	""" return the variation of datatype to type type
	"""
  if x in ["int","Int","integer","Integer",int]:
      return int
  elif x in ["str","Str","string","String",str]:
      return str
  elif x in ["bool","Bool","boolean","Boolean",bool]:
      return bool
  elif x in ["float","Float",float]:
      return float
  else: 
      return "undefined type"
  


#helper function
def returnValue(value,msg,showError):
  if showError:
    return msg
  else :
    return value


#------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------
#main function 

def validator(obj : dict , restriction : dict , strict= True , showErrorMsg = False) : #obj to be verified , restriction defines schema, and strict define whether string validation or loose (string validation means no extra field than specified in the restriction)
   #------------------------------------------------------------------
   #fetching required keys
   req_key_list = list(restriction.keys())

   # comparing whether the obj has all the required keys or not
   if strict:
     isEqual = compareList(list(obj.keys()), req_key_list)
     if not isEqual:
        return returnValue(False,"number of required field not matched",showErrorMsg) #number of required field not matched
    #--------------------------------------------------------------------

     #comparing each key and associated property
     for item in obj:
        objValue = obj[item]

        #datatype of the value
        oType = type(objValue)
        rType = dataTypeMapper(restriction[item]["type"])
        if rType == "undefined type":
            return returnValue(False,"undefined value in the schema",showErrorMsg)

        #checking datatype
        if oType != rType:
            return returnValue(False,"datatype not matched",showErrorMsg)   

        if rType in [int,float]:
          minValue , maxValue = restriction[item]["range"]

          #if value out of give range for the particular key value
          if objValue < minValue or objValue > maxValue:
              return returnValue(False,"value out of range",showErrorMsg) 
 
        
   return True

