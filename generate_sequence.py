import json
import reduce

def replacePlaceholder(data, placeholder, sequence):
    if not isinstance(data, (dict, list)):
        if data == placeholder:
            return sequence
        return data

    for item in data:
        print("Recursive function call:  ", item)
    
        if isinstance(item , dict):
            for key, value in item.items():
                print("Dict: ", value)
                if value == placeholder:
                    item[key] = sequence
                    return data
                elif isinstance(value, (dict, list)):
                    item[key] = replacePlaceholder(value, placeholder, sequence)

        elif isinstance(item , list):
            for idx, value in enumerate(item):
                print("List: ", value)
                if value == placeholder:
                    item[idx] = sequence
                    return data
                elif isinstance(value, (dict, list)):
                    item[idx] = replacePlaceholder(value, placeholder, sequence)

        elif isinstance(data, dict) and isinstance(data[item], (dict, list)):
            data[item] = replacePlaceholder(data[item], placeholder, sequence)

        elif item == placeholder:
            idx = data.index(item)
            data[idx] = sequence
            return data
    
    return data
                

def handler(event, context):
    print(event)
    
    try:
        params = event["params"]

        start = int(params.get("start", 0))
        
        stop = params.get("stop")
        identifier = params.get("identifier")
        if stop is None and identifier is None:
            print("Debug: ", json.dumps(event["fragment"]))
            print("Debug: ", "Both stop and identifier macro parameters are not given.", end=' ')
            print("As a result, we assume that there is nothing to do.")
            
            return {
                "requestId": event["requestId"],
                "status": "success",
                "fragment": event["fragment"]
            }
        elif identifier is None:
            data = event["fragment"]
            
            print("Debug: ", data)
            string_frag = json.dumps(data)
            
            placeholder = "$$Placeholder$$"
            if string_frag.find(placeholder) >= 0 :
                # We assume you want to generate a range of integers.
                sequence = [str(i) for i in range( int(stop) )]
                
                
                data = replacePlaceholder(data, placeholder, sequence)
                print("Debug: ", data)
                
                return {
                    "requestId": event["requestId"],
                    "status": "success",
                    "fragement": data
                }
            else:
                raise Exception("You should specify a stop parameter and either a placeholder or non-empty fragment.")
        elif stop is None:
            raise Exception("The stop parameter must be specified in the GenerateSequence AWS CF macro")

        stop = int(stop)
        
        input_fragment = json.dumps( event["fragment"] )
        print("Debug: ", input_fragment)

        fragment = []
        for i in range(start, stop):
            # The identifier is part of a string so there are dermacation markers for readability
            output_frag = input_fragment.replace('${' + identifier + '}', str(i) )
            # The identifier is standing on its own and dermacation is optional.
            output_frag = output_frag.replace(identifier, str(i))

            print("Debug: ", output_frag)
            
            fragment.append(json.loads(output_frag))
            
        print("Output fragment: ", json.dumps(fragment))
        
        return {
            "requestId": event["requestId"],
            "status": "success",
            "fragment": fragment
        }
    except Exception as e:
        response = {
            "requestId": event["requestId"],
            "status": "failure",
            "fragment": event["fragment"],
            "errorMessage": e.__str__()
        }

        return response
