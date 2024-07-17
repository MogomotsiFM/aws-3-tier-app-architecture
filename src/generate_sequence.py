import json

def handler(event, context):
  print(event)
  
  try:
      params = event["params"]
      
      start = int( params.get("start", 0) )
      stop = int( params.get("stop") )
      identifier = params.get("identifier")
      input_fragment = json.dumps( event["fragment"] )
      
      print("Debug: ", input_fragment)
      
      fragment = []
      for i in range(start, stop):
          output_frag = input_fragment.replace('${' + identifier + '}', str(i) )
          print("Debug: ", output_frag)
          
          fragment.append( json.loads(output_frag) )
      
      print("Output fragment: ", fragment)
      
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