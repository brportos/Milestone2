#include "codexion.h"

int display_error(char  *string, char *details, t_data *data)
{
    if (data != NULL)
        free_momory(data);
    fprintf(stderr, "\033[31mError\033[0m: %s", string);
    if (details != NULL)
        fprintf(stderr, "%s", details);
    fprintf(stderr, "\n");
    return (1);
}

void    display_log(int i, char *dongle_id, char *action, t_data *data)
{
    long long time;

    (void)dongle_id;
    pthread_mutex_lock(&data->mutex_print);
    time = get_time_ms() - data->start_time;
    if (strcmp(action, "takedongle") == 0)
        printf("%lld %d has taken a dongle\n", time, i);
    else if (strcmp(action, "compile") == 0)
        printf("%lld %d is compiling\n", time, i);
    else if (strcmp(action, "debug") == 0)
        printf("%lld %d is debugging\n", time, i);
    else if (strcmp(action, "refactor") == 0)
        printf("%lld %d is refactoring\n", time, i);
    else if(strcmp(action, "burns_out") == 0)
        printf("%lld %d burned out\n", time, i);
    pthread_mutex_unlock(&data->mutex_print);

}
