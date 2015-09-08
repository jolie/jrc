"""
Usage: reconfigurator.py [<options>] <json input file> <target specification>
  Options:
    -o, --ofile: file where to save the output
    -d, --dot: dot file where to save the configuration computed by Zephyrus
    -v, --verbose
"""

import json
import re
from subprocess import Popen,PIPE
import sys, getopt
import os
import logging as log
import SpecificationGrammar.SpecTranslator as Spec

import settings
#import SpecificationGrammar.SpecTranslator as SpecTranslator

resouce_names = set([])


DEVNULL = open(os.devnull, 'wb')

#log.basicConfig(filename='example.log',level=log.DEBUG)
#log.basicConfig(level=log.DEBUG)

def usage():
  """Print usage"""
  print(__doc__)

def read_json(json_file): 
  json_data = open(json_file)
  data = json.load(json_data)
  json_data.close()
  return data

def generate_universe(data, universe_file):
  """Generate the universe file for Zephyrus"""

  service_names = set([])

  universe = {
    "implementation" : {},
    "component_types" : [],
    "version" : 1, 
    "repositories" : [
      {
        "packages": [
          { "name": "mbs_stub_package" }
        ], 
        "name": "mbs"
      }]
    }
   
  for i in data["services"]:

    service_name = settings.DEFAULT_SERVICE_NAME + settings.SEPARATOR + i["name"]
    service_names.add(service_name)
        
    init_state = {
        "provide" : {},
        "require" : {},
        "initial" : True,
        "name" : "Init", 
        "successors" : ["On"] }
               
    state = {
        "provide" : {},
        "require" : {},
        "successors" : [],
        "name" : "On" }

    # handle provides
    if int(i["provide"]) == -1:
      state["provide"][settings.INTERFACE_PREFIX + i["name"]] = "inf"
    else:
      state["provide"][settings.INTERFACE_PREFIX + i["name"]] =  i["provide"]
        
    # handles require ports
    for k in i["dependencies"].keys():
      state["require"][settings.INTERFACE_PREFIX + k] = i["dependencies"][k]
           
    # for zephyrus specification resources should start with lowercase letter  
    costs = {}
    for k in i["cost"].keys():
      costs[settings.RESOURCE_PREFIX + k] = i["cost"][k]
        
    universe["component_types"].append({ "states" : [ init_state, state ], "name" : service_name, "consume" : costs})
    universe["implementation"][service_name] = [ { "repository": "mbs", "package": "mbs_stub_package" } ]
  
  with open(universe_file, 'w') as fo:
    json.dump(universe, fo, indent=1)
    
  return service_names     


def process_location_file(data, out_file):
  """Process the input json generating the location file for Zephyrus.
  It changes the name of the resources"""
    
  res = set([])
  
  res_dict = {}
  res_cost = {}
  
  locs = { "version" : 1, "locations" : [], "components": []}
  for i in data["DC_description"]:
    res_dict[i["name"]] = {}
    for j in i["provide_resources"].keys():
      res.add(settings.RESOURCE_PREFIX + j)
      res_dict[i["name"]][settings.RESOURCE_PREFIX + j] = i["provide_resources"][j]
      
    res_cost[i["name"]] = i["cost"]
       
  for i in data["DC_availability"].keys():
    counter = 0
    for j in range(int(data["DC_availability"][i])):
      locs["locations"].append({ "name" : i + settings.SEPARATOR +  str(counter),
                         "repository" : "mbs",
                         "provide_resources" : res_dict[i],
                         "cost" : res_cost[i] })
      counter += 1

  for i in data["initial_configuration"]:
    locs["components"].append({
       "state": "On", 
       "type": settings.DEFAULT_SERVICE_NAME + settings.SEPARATOR + i["service"], 
       "name": i["id"], 
       "location": i["DC"] + settings.SEPARATOR + str(i["DC_number"])
      })
  
  log.debug("New location data")
  log.debug(locs)
       
  # write file
  with open(out_file, 'w') as fo:
    json.dump(locs, fo, indent=1) 
    
  return res
  

def generate_output(data, zephyrus, output_stream):
  """Generate the json output"""

  services = []
  counter = 0
  id_to_id = {}

  for i in zephyrus["components"]:
    service = {}
    service["service"] = i["type"].split(settings.SEPARATOR)[1]
    service["id"] = settings.DEFAULT_SERVICE_NAME + str(counter)
    id_to_id[i["name"]] = service["id"]
    counter += 1
    service["DC"] = i["location"].split(settings.SEPARATOR)[0]
    service["DC_number"] = int(i["location"].split(settings.SEPARATOR)[1])
    services.append(service)

  # rename services that already exists
  for i in services:
    for j in data["initial_configuration"]:
      if j["service"] == i["service"] and \
           j["DC"] == i["DC"] and \
           j["DC_number"] == i["DC_number"] :
        i["id"] = j["id"]
        id_to_id[i["id"]] = j["id"]
        del j
        break

  bindings = {}
  for i in zephyrus["bindings"]:
    port = i["port"].split(settings.INTERFACE_PREFIX)[1]
    requirer = id_to_id[i["requirer"]]
    if requirer not in bindings:
      bindings[requirer] = [ { port  : id_to_id[i["provider"]] } ]
    else:
      bindings[requirer].append( { port : id_to_id[i["provider"]] })

  for i in services:
    if i["id"] in bindings:
      service["dependencies"] = bindings[i["id"]]
    
  out = { "configuration" : services}
  output_stream.write(json.dumps(out,indent=1))
  output_stream.write('\n')  


def main(argv):
  """Main procedure ..."""   
  output_file = ""
  dot_file = ""
  
  try:
    opts, args = getopt.getopt(argv,"ho:vd:",["help","ofile=","verbose","dot="])
  except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(1)
  for opt, arg in opts:
    if opt == '-h':
      usage()
      sys.exit()
    elif opt in ("-o", "--ofile"):
      output_file = arg
    elif opt in ("-d", "--dot"):
      dot_file = arg
    elif opt in ("-v", "--verbose"):
      log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
      log.info("Verbose output.")
  
  if len(args) != 2:
    print "2 arguments are required"
    usage()
    sys.exit(1)
    
  input_file = args[0]
  target = args[1] 
  
  if input_file == "" or target == "":
    print "Input file not given. Please use -i, -d, -t options"
    usage()
    sys.exit(1)
  
  input_file = os.path.abspath(input_file)
  
  pid = str(os.getpgid(0))
  aeolus_universe = "/tmp/" + pid + "_universe.json"
  spec_file = "/tmp/" + pid + "_spec.spec"
  zephyrus_output = "/tmp/" + pid + "_zephyrus.json"
  zephyrus_output_opt = "/tmp/" + pid + "_zephyrus_opt.json"
  locations_file = "/tmp/" + pid + "_locations.json"

  script_directory = os.path.dirname(os.path.realpath(__file__))

  log.info("Parsing JSON file")
  data = read_json(input_file)
  log.debug("Internal json representation")
  log.debug(json.dumps(data, indent=1))
   
  log.info("Getting locations")
  resouce_names = process_location_file(data, locations_file)
  
  log.info("Generating universe file")
  service_names = generate_universe(data, aeolus_universe)
  
  log.info("Processing specification")
  try: 
    spec = Spec.translate_specification(target, resouce_names, service_names)
  except Spec.SpecificationParsingException as e:
    log.critical("Parsing of the specification failed: " + e.value)
    log.critical("Exiting")
    sys.exit(1)
    
  log.debug("Zephyrus specification:")
  log.debug(spec)
  with open(spec_file, 'w') as f:
    f.write(spec) 
  
  log.debug("---UNIVERSE---")
  log.debug(json.dumps(read_json(aeolus_universe),indent=1))
  
  log.info("Running Zephyrus")
  if dot_file == "":
    proc = Popen( [settings.ZEPHYRUS_COMMAND, "-u", aeolus_universe, "-ic", locations_file,
           "-spec", spec_file, "-out", "stateful-json-v1", zephyrus_output,
           "-settings", script_directory + "/zephyrus.settings"],
           cwd=script_directory, stdout=PIPE, stderr=PIPE )
  else:
    proc = Popen( [settings.ZEPHYRUS_COMMAND, "-u", aeolus_universe, "-ic", locations_file,
         "-spec", spec_file, "-out", "stateful-json-v1", zephyrus_output,
         "-out", "graph-deployment", dot_file,
         "-settings", script_directory + "/zephyrus.settings"],
         cwd=script_directory, stdout=PIPE, stderr=PIPE )
  
  out, err = proc.communicate()
  log.debug("Zephyrus stdout")
  log.debug(out)
  log.debug("Zephyrus stderr")
  log.debug(err)
    
  if proc.returncode == 14:
    log.critical("Zephyrus execution terminated with return code " +  str(proc.returncode))
    log.critical("Specification does not admit solutions")
    sys.exit(1)
  
  if proc.returncode != 0:
    log.critical("Zephyrus execution terminated with return code " +  str(proc.returncode))
    log.critical("Exiting")
    sys.exit(1)

  log.debug("---FINAL CONFIGURATION---")
  log.debug(json.dumps(read_json(zephyrus_output),indent=1))
  
  log.debug("---RUN BINDINGS OPTIMIZER---")
  proc = Popen( ["python", "bindings_opt.py", "-i", zephyrus_output,
                  "-o", zephyrus_output_opt], cwd=script_directory, stdout=DEVNULL )
  proc.wait()
  
  if proc.returncode != 0:
    log.critical("Bindings optimizer terminated with return code " +  str(proc.returncode))
    log.critical("Exiting")
    sys.exit(1)
  log.debug(json.dumps(read_json(zephyrus_output_opt),indent=1))

  log.info("Generate JSON output")
  if output_file == "":
    generate_output(data, read_json(zephyrus_output_opt), sys.stdout)
  else:
    log.info("Writing to " + output_file)
    output_stream = open(output_file, 'w')
    generate_output(data, read_json(zephyrus_output_opt), output_stream)
    output_stream.close()
      
  log.info("Removing temp files")
  os.remove(aeolus_universe)
  os.remove(zephyrus_output)
  os.remove(spec_file)
  os.remove(locations_file)
  os.remove(zephyrus_output_opt)
  log.info("Program Succesfully Ended")


if __name__ == "__main__":
  main(sys.argv[1:])
