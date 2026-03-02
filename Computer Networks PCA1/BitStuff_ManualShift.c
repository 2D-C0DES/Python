#include <stdio.h>
#include <string.h>

#define MAX 1000

char DEFAULT_FLAG[] = "111110";

/* -------- Function to Count Maximum Consecutive 1s in Flag -------- */

int count_consecutive_ones(char flag[])
{
    int max_count = 0, current_count = 0;

    for (int i = 0; flag[i] != '\0'; i++)
    {
        if (flag[i] == '1')
        {
            current_count++;
            if (current_count > max_count)
                max_count = current_count;
        }
        else
        {
            current_count = 0;
        }
    }
    return max_count;
}

/* -------------------- BIT STUFFING -------------------- */

void bit_stuff(char data[], char flag[])
{
    int len = strlen(data);
    int count = 0;
    int limit = count_consecutive_ones(flag) - 1;

    printf("\n--- Bit Stuffing Process ---\n");

    for (int i = 0; i < len; i++)
    {

        if (data[i] == '1')
            count++;
        else
            count = 0;

        if (count == limit)
        {

            /* Shift right manually */
            for (int j = len; j > i + 1; j--)
                data[j] = data[j - 1];

            data[i + 1] = '0';
            len++;
            printf("Stuffed '0' at position %d\n", i + 1);

            count = 0;
            i++;
        }
    }

    printf("Length of the stuffed data is : %d", len);
}

/* -------------------- BIT DESTUFFING -------------------- */

void bit_destuff(char data[], char flag[])
{
    int len = strlen(data);
    int count = 0;
    int limit = count_consecutive_ones(flag) - 1;

    printf("\n--- De-Stuffing Process ---\n");

    for (int i = 0; i < len; i++)
    {

        if (data[i] == '1')
            count++;
        else
            count = 0;

        if (count == limit)
        {

            if (data[i + 1] == '0')
            {

                /* Shift left manually */
                for (int j = i + 1; j < len - 1; j++)
                    data[j] = data[j + 1];

                len--;
                data[len] = '\0';

                printf("Removed stuffed '0' at position %d\n", i + 1);

                count = 0;
            }
        }
    }
    printf("Length of the destuffed data is : %d", len);
}

/* -------------------- MAIN PROGRAM -------------------- */

int main()
{

    char data[MAX];
    char flag[MAX];
    int mode, choice;

    while (1)
    {

        printf("\n=========== MAIN MENU ===========\n");
        printf("1. Use Default Flag (111110)\n");
        printf("2. Use Custom Flag\n");
        printf("3. Exit\n");
        printf("Select Mode: ");
        scanf("%d", &mode);

        if (mode == 1)
        {
            strcpy(flag, DEFAULT_FLAG);
            printf("\nUsing Default Flag: %s\n", flag);
        }
        else if (mode == 2)
        {
            printf("Enter custom flag pattern: ");
            scanf("%s", flag);
            printf("\nUsing Custom Flag: %s\n", flag);
        }
        else if (mode == 3)
        {
            printf("Exiting Program...\n");
            break;
        }
        else
        {
            printf("Invalid Mode!\n");
            continue;
        }

        while (1)
        {

            printf("\n----- OPERATIONS MENU -----\n");
            printf("1. Perform Bit Stuffing\n");
            printf("2. Perform De-Stuffing\n");
            printf("3. Change Mode\n");
            printf("Enter choice: ");
            scanf("%d", &choice);

            if (choice == 1)
            {

                printf("Enter binary data: ");
                scanf("%s", data);

                bit_stuff(data, flag);

                printf("\nStuffed Data: %s\n", data);
            }

            else if (choice == 2)
            {

                bit_destuff(data, flag);

                printf("\nDe-Stuffed Data: %s\n", data);
            }

            else if (choice == 3)
            {
                break;
            }

            else
            {
                printf("Invalid choice!\n");
            }
        }
    }

    return 0;
}