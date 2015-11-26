include "console.iol"
include "file.iol"

type ConfRequestType: void {
	.id: string
	.conf: string
}

type SpecRequestType: void {
	.id: string
	.spec: string	
}

type IdType: string

interface ReconfiguratorInterface {
	RequestResponse:
		getId( void )( IdType ),
		getConf( SpecRequestType ) ( string ),
		sendConf (ConfRequestType)( string )    	 
}

outputPort ReconfiguratorService {
    Location: "socket://localhost:9000"
    Protocol: http { .method = "get" } 
    Interfaces: ReconfiguratorInterface
}

main {
	getId@ReconfiguratorService() ( request.id );
	println@Console( "Received id: " + request.id )();

	readfile_request.filename = "infoworld.json";
	readFile@File(readfile_request)(request.conf);

	sendConf@ReconfiguratorService(request)(response);
	println@Console( "Configuration sent. Receive message: " + response )();

	undef( request.conf );
	readfile_request.filename = "infoworld1.spec";
	readFile@File(readfile_request)(request.spec);
	getConf@ReconfiguratorService(request)(response);
	println@Console( "Specification sent. Final configuration:\n" + response )()
}
