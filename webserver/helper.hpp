#include <arpa/inet.h>
#include <errno.h>
#include <netinet/ip.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <bits/stdc++.h>
#include <list>
#include <sys/types.h>
#include <sys/stat.h>
#include <fstream>
#include<string>
#include<iostream>
#include<filesystem>


#define BUFFER_SIZE 10000000

#define HTTP_OFFSET 4
#define HOST_OFFSET 6
#define CONNECTION_OFFSET 11



#define ERROR(str)                                         \
    {                                                      \
        fprintf(stderr, "%s: %s\n", str, strerror(errno)); \
        exit(EXIT_FAILURE);                                \
    }

using namespace std;

class TCP
{
public:
 
    char *path;
    int sockfd;
    int connected_sockfd;
    int ready;
    int status;
    int connection;
    int content_size;

    TCP(int port, char *path);

    void accept_connection();
    int is_ready_to_rcv();
    ssize_t receive_to_buffer(char* buffer);

    void extract_data(char* buffer, ssize_t bytes_read, char* endpoint, char* domain);
    void get_file_path_and_status(char* filepath, char* endpoint, char* domain);
    void get_file_extension(char* filepath, char* extension);

    ssize_t parse_header(char* header, char* content_type, ssize_t content_size, char* filepath);
    void fill_content(char* file_buffer, char* filepath, size_t file_size);
    void send_response(char* header, char* file_buffer, ssize_t header_size, ssize_t file_size);

};
size_t GetFileSize(char* filename);
