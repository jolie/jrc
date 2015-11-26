include "console.iol"
include "file.iol"

type ProcessRequest: void {
  .specifications: string
  .context: string // in JSON format
}

type ProcessResponse: void {
  .configuration: string  //in JSON format
}

interface ReconfiguratorInterface {
RequestResponse:
  process( ProcessRequest )( ProcessResponse )
}

outputPort ReconfiguratorService {
    Location: "socket://localhost:9001"
    Protocol: http { .method = "get" } 
    Interfaces: ReconfiguratorInterface
}

main {
	
	readfile_request.filename = "infoworld.json";
	readFile@File(readfile_request)(request.context);

	readfile_request.filename = "infoworld1.spec";
	readFile@File(readfile_request)(request.specifications);
	
	process@ReconfiguratorService(request)(response);
	println@Console( "Specification sent. Final configuration:\n" + response.configuration )()
}
