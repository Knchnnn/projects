#include <stdio.h>

int main() {
    FILE *fp;

    fp = fopen("data.txt", "w");  // open file in write mode

    fprintf(fp, "Hello File Handling!");

    fclose(fp);  // close file

    printf("Data written successfully");

    return 0;
}