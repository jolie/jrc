include "console.iol"
include "exec.iol"
include "math.iol"
include "file.iol"

execution { concurrent }


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

inputPort ReconfiguratorService {
    Location: "socket://localhost:9001"
    Protocol: http 
    Interfaces: ReconfiguratorInterface
}


main {
	[ process( request )( response ) {
		// Save files
		random@Math()(num);
		spec_file = "/tmp/" + string(num) + ".spec";
		json_file = "/tmp/" + string(num) + ".json";
		write_file_request.content = request.specifications;
		write_file_request.filename = spec_file;
		writeFile@File(write_file_request)();
		write_file_request.content = request.context;
		write_file_request.filename = json_file;
		writeFile@File(write_file_request)();

		// Run command
		println@Console( "Running command for files " + json_file + " " + spec_file )();
		command_request = "python";
  	command_request.args[0] = "reconfigurator.py";
		command_request.args[1] = json_file;
		command_request.args[2] = spec_file;
		//command_request.workingDirectory = "/jrc";
  	exec@Exec( command_request )( output );
		println@Console( "exit code: " + string(output.exitCode) )();
		println@Console( "stderr: " + string(output.stderr) )();
  	response.configuration = string(output)
	} ] {nullProcess}
}
