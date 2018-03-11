/* this programm VERY approximately measure 
 * execution time of other programm specified
 * by path.
 * It was written just to explore fork()
*/
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <time.h>
#include <sys/types.h>
#include <sys/wait.h>


void readCommandName(char *dst, size_t size) {
	printf("Input program path: "); fflush(stdout);
	fgets(dst, size, stdin);
	dst[strlen(dst)- 1] = '\0'; // removing \n at the end

}

int main(int argc, char **argv, char **envp) {
	char commandName[128];
	readCommandName(commandName, sizeof(commandName)/sizeof(char));
	time_t startTime = time(0);
	pid_t pid = fork();
	if(pid == -1) {
		fprintf(stderr, "Error during forking: %s\n", strerror(errno));
		return 1;
	} else if(pid == 0) { // <---- child code
		char *arguments[] = {commandName, NULL};
		if(execve(commandName, arguments, envp) == -1) {
			fprintf(stderr, "Can not execute programm. Error: %s\n", strerror(errno));
			return 1;
		}	
	}
	int status;
	if(waitpid(pid, &status, 0) == -1) {
		fprintf(stderr, "Unexpected error: %s\n", strerror(errno));
		return 1;
	}
	time_t endTime = time(0);
	status = WEXITSTATUS(status);
	if(status) {
		printf("WARNING: program exited with non-zero status: %d\n", status);
	} else 
		printf("Execution time: %lf milliseconds\n", difftime(endTime,startTime)*1000);
	return status;
}
