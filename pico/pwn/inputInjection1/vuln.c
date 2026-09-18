#include <string.h>
#include <stdio.h>
#include <stdlib.h> 

void fun(char *name, char *cmd) {

int main() {
    char name[200];
    printf("What is your name?\n");
    fflush(stdout);


    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0;

    fun(name, "uname");
    return 0;
}

void fun(char *name, char *cmd) { // rdi, rsi
    char c[10];
    char buffer[10];

    strcpy(c, cmd); // rsi
    strcpy(buffer, name); // rdi

    printf("Goodbye, %s!\n", buffer);
    fflush(stdout);
    system(c);
}

