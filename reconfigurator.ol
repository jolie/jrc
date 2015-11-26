include "console.iol"
include "exec.iol"
include "math.iol"
include "file.iol"

execution { concurrent }


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

inputPort ReconfiguratorService {
    Location: "socket://localhost:9001"
    Protocol: http 
    Interfaces: ReconfiguratorInterface
}


main {

	[ getId( request )( response ) {
		random@Math()(num);
		response = string(num)
	} ] {nullProcess}

	[ getConf( request )( response ) {
		spec_file = "/tmp/" + request.id + ".spec";
		json_file = "/tmp/" + request.id + ".json";
		write_file_request.content = request.spec;
		write_file_request.filename = spec_file;
		command_request = "python";
  	command_request.args = "reconfigurator.py " + json_file + " " + spec_file;
  	exec@Exec( command_request )( output );
  	response = output
	} ] {nullProcess}

	[ sendConf( request )( response ) {
		json_file = "/tmp/" + request.id + ".json";
		write_file_request.content = request.conf;
		write_file_request.filename = json_file;
		writeFile@File(write_file_request)();
		response = "Configuration received"
	} ] {nullProcess}  
}
