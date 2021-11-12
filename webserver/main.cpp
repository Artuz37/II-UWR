#include "helper.hpp"
using namespace std;

	// 10 MB
char recv_buffer[BUFFER_SIZE+1];
char header_buffer[8192];
char endpoint[2048];
char domain[2048];  
char filepath[8192];
char* file_buffer;
char extension[100];
ssize_t file_size;
ssize_t header_size;
int ready;



// ./webserver port katalog
int main(int argc, char *argv[]) {
    
    if (argc!=3){
        printf("\nwrong number of arguments\n");
        exit(EXIT_FAILURE);
    }

    int port = atoi(argv[1]);
    char *pathname = argv[2];    

    struct stat info;

    if( stat( pathname, &info ) != 0 ){
        printf( "\ncannot access %s\n", pathname );
        exit(EXIT_FAILURE);
        }
    else if ( info.st_mode & S_IFREG ){
        printf("\n%s is not a directory", pathname);
        exit(EXIT_FAILURE);
    }

    if (65535 < port || port < 1){
        cout<<"wrong port\n";
        exit(EXIT_FAILURE);
    }

    auto TCP_server = TCP(port, pathname);
    
    for (;;){        
        TCP_server.accept_connection();
        ready = 1;
		while(ready>0){ 
            ready = TCP_server.is_ready_to_rcv();
            if (ready<=0)
                break; 
            ssize_t bytes_read = TCP_server.receive_to_buffer(recv_buffer);
            //if (bytes_read == 0)break;
            TCP_server.extract_data(recv_buffer, bytes_read, endpoint, domain);
            if (TCP_server.connection == 0)
                ready=0;
            if (TCP_server.status!=501){
                TCP_server.get_file_path_and_status(filepath, endpoint, domain);
            }        
            if (TCP_server.status == 200){
                TCP_server.get_file_extension(filepath, extension); 
                file_size = GetFileSize(filepath);
                file_buffer = (char*)malloc(file_size);  
                TCP_server.fill_content(file_buffer, filepath, file_size);
            }
            header_size = TCP_server.parse_header(header_buffer, extension, file_size, filepath);

            TCP_server.send_response(header_buffer, file_buffer, header_size, file_size);
        }
		if (close (TCP_server.connected_sockfd) < 0)
			ERROR("close error");
        
    }
    if (close(TCP_server.sockfd) < 0){
            ERROR("close error");
    }
    return 0;
}
