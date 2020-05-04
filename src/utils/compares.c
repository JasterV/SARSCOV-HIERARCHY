#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int max(int i, int e);
int min(int i, int e);

int compares(char rna1[80],
             char rna2[80])
{
    int rn1_len = strlen(rna1);
    int rn2_len = strlen(rna2);
    int max_len = max(rn1_len, rn2_len);
    int min_len = min(rn1_len, rn2_len);
    int matches = 0;
    for (int i = 0; i < min_len; i++)
    {
        char symbol1 = rna1[i];
        char symbol2 = rna2[i];
            if (symbol1 == symbol2 || symbol1 == 'N' || symbol2 == 'N')
            {
                matches += 1;
            }
    }
    return matches / max(rn1_len, rn2_len);
}

int max(int elem1, int elem2)
{
    return (elem1 + elem2 + abs(elem1 - elem2)) / 2;
}


int min(int elem1, int elem2)
{
    return elem1 < elem2 ? elem1 : elem2;
}