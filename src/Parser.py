

def parseJoystick(input):
    try:
        key, value = input.split(":")
        # print("key: %s"%key)
        # print("value: %s"%value)
    except ValueError:
        print("ValueError unknown telegram")
        return None, None
        
    if key == "joystick":
        index_xval = value.find("xval=")
        index_sep = value.find("&")
        index_yval = value.find("yval=")
        index_end = len(value) + 1 

        xVal = value[index_xval+5:index_sep]
        yVal = value[index_yval+5:index_end]
        return int(xVal), int(yVal)
    else:
        return None, None