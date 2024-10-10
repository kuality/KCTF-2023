#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup() {
    	setvbuf(stdin,0,2,0);
    	setvbuf(stdout,0,2,0);
    	setvbuf(stderr,0,2,0);
}

int main() 
{
    setup();
    char input[100];
    char flag[100];
    char request[] = "Please give me the flag\n"; 

    printf("what you want? : ");
    fgets(input, sizeof(input), stdin);

    if (strcmp(input, request) == 0) {
        FILE* file = fopen("/home/ctf/flag.txt", "r");
        if (file) {
            fgets(flag, sizeof(flag), file);
            fclose(file);
            printf("Flag : %s\n", flag);
        }
    } 
    else {
        printf("oh,,,,,,,, it's NOT what you want\n");
    }
    return 0;
}
