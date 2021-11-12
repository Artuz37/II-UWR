#include "helper.hpp"

using namespace std;

TCP::TCP(int port, char *path)
{
    this->sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (this->sockfd < 0)
        ERROR("socket error");

    struct sockaddr_in server_address;
    bzero(&server_address, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(this->sockfd, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
        ERROR("bind error");

    if (listen(this->sockfd, 64) < 0)
        ERROR("listen error");

    this->path = path;
}

void TCP::accept_connection()
{
    this->connected_sockfd = accept(this->sockfd, NULL, NULL);
    if (this->connected_sockfd < 0)
        ERROR("accept error");
    this->connection=1;
}

int TCP::is_ready_to_rcv(){
    int ready;
    struct timeval tv; tv.tv_sec = 1; tv.tv_usec = 0;
    fd_set descriptors;
	FD_ZERO(&descriptors);
	FD_SET(this->connected_sockfd, &descriptors);
    ready = select(this->connected_sockfd + 1, &descriptors, NULL, NULL, &tv);
    if (ready<0)
        ERROR("select error");
    return ready;
}

ssize_t TCP::receive_to_buffer(char* buffer)
{
    this->connection=0;
    this->status = 0;
    ssize_t bytes_read = recv(this->connected_sockfd, buffer, BUFFER_SIZE, 0);
    if (bytes_read < 0)
        ERROR("recv error");
    buffer[bytes_read] = '\0';
    return bytes_read;
}

void TCP::extract_data(char* buffer, ssize_t bytes_read, char* endpoint, char* domain)
{
    ssize_t point;
    string data(buffer, bytes_read);
    basic_string<char>::size_type get=data.find("GET"), http=data.find(" HTTP/1.1"),\
     host=data.find("Host: "), connection=data.find("Connection: ");
    if (get==string::npos||http==string::npos||host==string::npos||data.length()<CONNECTION_OFFSET-1){
        this->status = 501;
        return;
    }

    strcpy(endpoint, data.substr(4, http - HTTP_OFFSET).c_str());

    point = data.find(":", host + HOST_OFFSET);
    strcpy(domain, data.substr(host + HOST_OFFSET, point-host-HOST_OFFSET).c_str());

    point = data.substr(connection + CONNECTION_OFFSET).find("keep-alive");
    if (point < 0)this->connection=0;
    else this->connection=1;
}

void TCP::get_file_path_and_status(char* filepath, char* endpoint, char* domain)
{
    string data(endpoint, strlen(endpoint));
    int dots = data.find("..");
    if (dots>-1){
        this->status=403;
        return;
    }
    sprintf(filepath, "%s/%s%s", this->path, domain, endpoint);
    struct stat s;
    if( stat(filepath,&s) == 0 )
    {
        if( s.st_mode & S_IFDIR)
        {
            this->status = 301;
            sprintf(filepath, "/index.html");
        }
        else if( s.st_mode & S_IFREG ) this->status = 200;
    }
    else this->status=404;
}

void TCP::get_file_extension(char* filepath, char* extension)
{
    string data(filepath, strlen(filepath));
    int dot = data.rfind(".");
    if (data.substr(dot)==".txt") strcpy(extension, "text/plain;charset=utf-8");
    else if (data.substr(dot)==".html") strcpy(extension, "text/html;charset=utf-8");
    else if (data.substr(dot)==".css") strcpy(extension, "text/css;charset=utf-8");
    else if (data.substr(dot)==".jpg") strcpy(extension, "image/jpg");
    else if (data.substr(dot)==".jpeg") strcpy(extension, "image/jpeg");
    else if (data.substr(dot)==".png") strcpy(extension, "image/png");
    else if (data.substr(dot)==".pdf") strcpy(extension, "application/pdf");
    else strcpy(extension, "application/octet-stream");
}

void TCP::fill_content(char* file_buffer, char* filepath, size_t file_size){
    
    ifstream my_file;
    my_file.open(filepath);
    my_file.read(file_buffer, file_size);
    my_file.close();
}

ssize_t TCP::parse_header(char* header, char* content_type, ssize_t content_size, char* filepath)
{
    ssize_t header_size;
    string html;
    switch (this->status)
    {
    case 200:
        header_size = sprintf(header, "HTTP/1.1 %s\r\nContent-Length: %ld\r\nContent-Type: %s\r\n\r\n",\
         "200 OK", content_size, content_type);
        break;
    case 301:
        header_size = sprintf(header, "HTTP/1.1 %s\r\nLocation: %s\r\n\r\n",\
         "301 Moved Permanently", filepath);
        break;
    case 403:
        html = "<h1> 403 Forbidden </h1>";
        header_size = sprintf(header, "HTTP/1.1 %s\r\nContent-Length: %ld\r\nContent-Type: text/html\r\n\r\n%s", \
                                "403 Forbidden", html.size(), html.c_str());
        break;
    case 404:
        html = "<h1> 404 Not Found </h1>";
        header_size = sprintf(header, "HTTP/1.1 %s\r\nContent-Length: %ld\r\nContent-Type: text/html\r\n\r\n%s", \
                                "404 Not Found", html.size(), html.c_str());
        break;
    case 501:
        html = "<h1> 501 Not Implemented </h1>";
        header_size = sprintf(header, "HTTP/1.1 %s\r\nContent-Length: %ld\r\nContent-Type: text/html\r\n\r\n%s", \
                                "501 Not Implemented", html.size(), html.c_str());
        break; 
    }
    return header_size;
}



void TCP::send_response(char* header, char* file_buffer, ssize_t header_size, ssize_t file_size){
    ssize_t bytes_sent = send (this->connected_sockfd, header, header_size, 0);        
	if (bytes_sent < 0)
		ERROR("send error");
    if  (this->status == 200)
    {
        bytes_sent = send (this->connected_sockfd, file_buffer, file_size, 0); 
        free(file_buffer);       
            if (bytes_sent < 0)
                ERROR("send error");
    }
}

size_t GetFileSize(char* filename)
{
    struct stat stat_buf;
    int rc = stat(filename, &stat_buf);
    return rc == 0 ? stat_buf.st_size : -1;
}