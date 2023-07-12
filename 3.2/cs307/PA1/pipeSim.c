#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(int argc, char **argv){
    int fd[2];
    pid_t cpid, cpid2; 

    char *man_args[] = {"man", "ls", NULL};
    char *grep_args[] = {"grep", "-A 1", "^[[:space:]]*-s", NULL};

    int pipes[4];
    pipe(pipes);

    printf("I'm a SHELL process, with PID: %d - Main command is: man ls | grep -A 1 '^[[space:]]*-s'\n", getpid());
    
    if(pipe(fd) < 0){
        perror("pipe");
        exit(1);
    }
    cpid = fork();

    if(cpid < 0){
        perror("Fork");
        exit(1);
    }
    else if(cpid == 0){ //child process
        printf("I'm a MAN process, with PID: %d - My command is: ls\n", getpid());
        dup2(pipes[1], 1);
        close(pipes[0]);
        close(pipes[1]);
        execvp(*man_args, man_args);
    }
    else{
        cpid2 = fork();

        if(cpid2 < 0){
            perror("pipe");
            exit(1);
        }
        else if(cpid2 == 0){
            printf("I'm a GREP process, with PID: %d - My command is: -A 1 ^[[:space:]]*-s\n", getpid());
            int new_fd = open("output.txt", O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);
            if (dup2(new_fd, STDOUT_FILENO) < 0){
                perror("dup2");
                _exit(1);
            }
            dup2(pipes[0], 0);
            close(pipes[0]);
            close(pipes[1]);
            execvp(*grep_args, grep_args);
        }
        else{
            close(pipes[0]);
            close(pipes[1]);
            waitpid(cpid2, NULL, 0);
            waitpid(cpid, NULL, 0);
            printf("I'm a SHELL process, with PID: %d - execution is completed, you can find the results in output.txt\n", getpid());
        }
    }

    
    
}